import os
import re
import time
import shutil
import zipfile
import io

from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
from docx import Document

# Fly.io writable directory
UPLOAD_FOLDER = "/data/uploads"

# Ensure upload directory exists (Fly mounts /data as persistent storage)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"html", "zip"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

EXPECTED_BANNER_SIZES = [
    (300, 250), (160, 600), (728, 90), (320, 50),
    (970, 250), (300, 50)
]

MAX_FILE_SIZE_KB = 150
ANIMATION_MAX_DURATION = 15
MAX_LOOP_COUNT = 3
ANIMATION_WARNING_THRESHOLD = 14.8

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------------------------------
# AUTO CLEANUP OF OLD UPLOADS
# -------------------------------------------------------
def cleanup_old_uploads(max_age_hours=6):
    now = time.time()
    max_age_seconds = max_age_hours * 3600

    for item in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, item)
        try:
            mtime = os.path.getmtime(path)
        except FileNotFoundError:
            continue

        if now - mtime > max_age_seconds:
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)
            print(f"[CLEANUP] Deleted old upload: {path}")


# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_zip(file_path):
    extracted_folder = os.path.join(
        UPLOAD_FOLDER, os.path.splitext(os.path.basename(file_path))[0]
    )
    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extracted_folder)
    except zipfile.BadZipFile:
        return None
    return extracted_folder


def extract_ad_size_from_css(css_file_path):
    if not os.path.exists(css_file_path):
        return None, None
    try:
        with open(css_file_path, "r", encoding="utf-8", errors="replace") as file:
            css_content = file.read()

        w = re.search(r"width\s*:\s*(\d+)px", css_content)
        h = re.search(r"height\s*:\s*(\d+)px", css_content)
        if w and h:
            return int(w.group(1)), int(h.group(1))
    except:
        pass

    return None, None


def check_border_in_css(css_content):
    return bool(re.search(r"border\s*:\s*1px\s+solid", css_content, re.IGNORECASE))


def extract_size_from_inline(style):
    w = re.search(r"width\s*:\s*(\d+)px", style)
    h = re.search(r"height\s*:\s*(\d+)px", style)
    return (int(w.group(1)), int(h.group(1))) if w and h else (None, None)


# -------------------------------------------------------
#  HTML VALIDATION (UPGRADED)
# -------------------------------------------------------
def validate_html(file_path):
    results = {
        "warnings": [],
        "errors": [],
        "banner_size": None,
        "border": "❌ Missing 1px border",
        "used_meta_tag": False,
        "size_source": "Unknown"
    }

    if not os.path.exists(file_path):
        results["errors"].append(f"File not found: {file_path}")
        return results

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        soup = BeautifulSoup(f, "html.parser")

    base_path = os.path.dirname(file_path)
    missing_assets = []
    border_found = False
    border_source = None

    css_width = css_height = None
    html_width = html_height = None

    # ------------------------ CSS Parsing ------------------------
    css_files = [
        link.get("href") for link in soup.find_all("link", rel="stylesheet") if link.get("href")
    ]

    for css_file in css_files:
        css_path = os.path.join(base_path, css_file)
        if not os.path.exists(css_path):
            continue

        with open(css_path, "r", encoding="utf-8", errors="replace") as f:
            css_text = f.read()

        if check_border_in_css(css_text):
            border_found = True
            border_source = "CSS"

        w, h = extract_ad_size_from_css(css_path)
        if w and h:
            css_width, css_height = w, h
            results["size_source"] = "CSS"

    # ------------------------ Inline border ------------------------
    for tag in soup.find_all(True):
        style = tag.get("style", "")
        if "border" in style and "1px" in style and "solid" in style:
            border_found = True
            border_source = "Inline Style"

    # ------------------------ Inline size detection ------------------------
    for tag in soup.find_all(["div", "body"]):
        if "style" in tag.attrs:
            w, h = extract_size_from_inline(tag["style"])
            if w and h:
                html_width, html_height = w, h
                results["size_source"] = "Inline Style"
                break

    # ------------------------ .adSize ------------------------
    size_div = soup.find(attrs={"class": "adSize"})
    if size_div:
        if "style" in size_div.attrs:
            w, h = extract_size_from_inline(size_div["style"])
            if w and h:
                html_width, html_height = w, h
                results["size_source"] = ".adSize Inline"

    # ------------------------ META TAG ------------------------
    meta = soup.find("meta", {"name": "ad.size"})
    if meta and "content" in meta.attrs:
        match = re.search(r"width=(\d+),\s*height=(\d+)", meta["content"])
        if match:
            html_width = int(match.group(1))
            html_height = int(match.group(2))
            results["used_meta_tag"] = True
            results["size_source"] = "META ad.size"

    # ------------------------ SVG border ------------------------
    for rect in soup.find_all("rect"):
        stroke = rect.get("stroke")
        stroke_w = rect.get("stroke-width")
        try:
            if stroke and float(stroke_w) == 1:
                border_found = True
                border_source = "SVG Border"
        except:
            pass

    # ------------------------ SVG Click detection ------------------------
    for svg in soup.find_all("svg"):
        if svg.get("onclick"):
            results["warnings"].append("SVG click handler detected.")

        for el in svg.find_all(True):
            if el.get("id") and el.get("id").lower().startswith("click"):
                results["warnings"].append("SVG clickable element detected.")

            classes = el.get("class") or []
            if any("click" in c.lower() for c in classes):
                results["warnings"].append("SVG clickable class detected.")

            if el.get("onclick"):
                results["warnings"].append("SVG nested onclick click detected.")

    # ------------------------ Final size ------------------------
    bw = css_width or html_width
    bh = css_height or html_height

    if bw and bh:
        results["banner_size"] = f"{bw}x{bh}"
        if (bw, bh) not in EXPECTED_BANNER_SIZES:
            results["errors"].append(f"Invalid banner size: {bw}x{bh}")
    else:
        results["warnings"].append("⚠️ Could not determine banner size.")

    # ------------------------ Final Border ------------------------
    if border_found:
        results["border"] = f"✅ 1px border present ({border_source})"
    else:
        results["border"] = "❌ Missing 1px border"

    # ------------------------ Missing Assets ------------------------
    for tag in soup.find_all(["img", "script", "link"]):
        src = tag.get("src") or tag.get("href")
        if not src:
            continue
        if src.startswith(("http://", "https://", "data:")):
            continue

        asset_path = os.path.join(base_path, src.lstrip("/"))
        if not os.path.exists(asset_path):
            missing_assets.append(src)

    if missing_assets:
        results["errors"].append(f"Missing assets: {missing_assets}")

    # ------------------------ Basic Click Area ------------------------
    clickable = (
        soup.find(id="designContainer")
        or soup.find(id="clickTagMain")
        or soup.find(id="clickLayer")
        or soup.find(id="clickable")
        or soup.find(attrs={"class": "clickTag"})
        or soup.find(attrs={"class": "clickable"})
    )

    if not clickable:
        results["warnings"].append(
            "No clickable area detected (no HTML click layer or JS click handler found)."
        )

    return results


# -------------------------------------------------------
# JS VALIDATION (UPGRADED)
# -------------------------------------------------------
def validate_js(file_path):
    results = {"warnings": [], "errors": [], "duration": 0, "isi_duration": 0}

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            js = f.read()
    except:
        results["errors"].append("Error reading JS file.")
        return results

    js = re.sub(r"//.*", "", js)

    # ------------------------ JS-click detection ------------------------
    click_patterns = [
        r"\.addEventListener\(['\"]click['\"]",
        r"window\.onclick",
        r"document\.onclick",
        r"onclick\s*=",
        r"Enabler\.exit",
        r"exit\(",
        r"clickTag",
    ]
    js_click_found = any(re.search(p, js) for p in click_patterns)
    if js_click_found:
        results["warnings"].append("JS-only click handler detected.")

    # ------------------------ Canvas Border ------------------------
    canvas_patterns = [
        r"strokeRect\s*\(",
        r"lineWidth\s*=\s*1",
        r"strokeStyle\s*=\s*['\"]#?000",
    ]
    for p in canvas_patterns:
        if re.search(p, js):
            results["warnings"].append("Canvas border detected via JS.")
            break

    # ------------------------ Animation Duration ------------------------
    delays = [float(d) for d in re.findall(r"delayedCall\(\s*(\d+\.?\d*)", js)]
    frames = [float(d) for d in re.findall(r"frameDelay\s*=\s*(\d+\.?\d*)", js)]
    animation_duration = sum(delays) or sum(frames)

    isi_scroll = 0
    if "scrollTo" in js or "ISIscroll" in js:
        m = re.search(r"scrollSpeed\s*=\s*(\d+\.?\d*)", js)
        isi_scroll = float(m.group(1)) if m else 10.0

    total = animation_duration + isi_scroll

    results["duration"] = round(animation_duration, 1)
    results["isi_duration"] = round(isi_scroll, 1)

    if total > ANIMATION_MAX_DURATION:
        results["errors"].append(f"Animation exceeds limit: {total:.1f}s")
    elif total >= ANIMATION_WARNING_THRESHOLD:
        results["warnings"].append(f"Animation approaching limit: {total:.1f}s")

    # ------------------------ Loop Count ------------------------
    loops = re.findall(r"repeat\s*:\s*(\d+|Infinity|-1)", js)
    for loop in loops:
        if loop in ("Infinity", "-1") or (loop.isdigit() and int(loop) > MAX_LOOP_COUNT):
            results["errors"].append(f"Loop count exceeds limit: {loop}")

    return results


# -------------------------------------------------------
# Preview Route
# -------------------------------------------------------
@app.route("/preview/<path:folder>/<filename>")
def preview_banner(folder, filename):
    if "__MACOSX" in folder or filename.startswith("."):
        return "Invalid preview request", 404

    folder_path = os.path.join(UPLOAD_FOLDER, folder)
    full = os.path.join(folder_path, filename)

    if not os.path.exists(full):
        return "Not found", 404

    return send_from_directory(folder_path, filename)


# -------------------------------------------------------
# Index Route
# -------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------------------------------
# Validation Endpoint (main)
# -------------------------------------------------------
@app.route("/validate", methods=["POST"])
def validate_file():
    cleanup_old_uploads()  # Auto cleanup

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    file_size_kb = os.path.getsize(file_path) / 1024
    preview_links = []
    validation = {"html": {}, "js": {}}
    durations = {"animation": 0.0, "isi": 0.0, "total": 0.0}

    # ------------------------ ZIP Handling ------------------------
    if filename.endswith(".zip"):
        extracted = extract_zip(file_path)
        if not extracted:
            return jsonify({"error": "Invalid ZIP file"}), 400

        html_files, js_files = [], []

        for root, _, files in os.walk(extracted):
            for f in files:
                fp = os.path.join(root, f)
                if f.endswith(".html") and "__MACOSX" not in root:
                    html_files.append(fp)
                elif f.endswith(".js") and "__MACOSX" not in root:
                    js_files.append(fp)

        if not html_files:
            return jsonify({"error": "No HTML file in ZIP"}), 400

        for html in html_files:
            html_name = os.path.basename(html)
            validation["html"][html_name] = validate_html(html)

            rel_folder = os.path.relpath(os.path.dirname(html), UPLOAD_FOLDER)
            preview_links.append(f"{request.host_url}preview/{rel_folder}/{html_name}")

        for js in js_files:
            js_name = os.path.basename(js)
            res = validate_js(js)
            validation["js"][js_name] = res
            durations["animation"] += res["duration"]
            durations["isi"] += res["isi_duration"]

    # ------------------------ Single HTML Upload ------------------------
    elif filename.endswith(".html"):
        validation["html"][filename] = validate_html(file_path)
        preview_links.append(f"{request.host_url}preview/{filename}")

    durations["animation"] = round(durations["animation"], 1)
    durations["isi"] = round(durations["isi"], 1)
    durations["total"] = durations["animation"] + durations["isi"]

    return jsonify({
        "validation_results": validation,
        "previews": preview_links,
        "file_size_kb": round(file_size_kb, 2),
        "durations": durations
    })


# -------------------------------------------------------
# Word Report Endpoint
# -------------------------------------------------------
@app.route("/word-report", methods=["POST"])
def word_report():
    """
    Expect JSON payload like:
    {
      "file_name": "...",
      "file_size_kb": 123.45,
      "validation_results": {...},
      "durations": {...}
    }
    """
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "No data provided"}), 400

    file_name = payload.get("file_name", "Unknown file")
    size_kb = payload.get("file_size_kb")
    validation = payload.get("validation_results", {})
    durations = payload.get("durations", {})

    html_results = validation.get("html", {}) or {}
    js_results = validation.get("js", {}) or {}

    # ---- Summary calculations (same logic as UI) ----
    missing_assets = any(
        any("Missing assets" in e for e in (res.get("errors") or []))
        for res in html_results.values()
    )
    banner_sizes = [
        res.get("banner_size") for res in html_results.values()
        if res.get("banner_size")
    ]
    first_html = next(iter(html_results.values()), None)

    loop_issue = any(
        any("Loop count exceeds" in e for e in (res.get("errors") or []))
        for res in js_results.values()
    )

    clickable_warning = any(
        any("No clickable area" in w for w in (res.get("warnings") or []))
        for res in html_results.values()
    )

    # ---- Build DOCX ----
    doc = Document()
    doc.add_heading("HTML5 Ad Validator Report", level=1)

    p = doc.add_paragraph()
    p.add_run("File: ").bold = True
    p.add_run(file_name)

    if size_kb is not None:
        p = doc.add_paragraph()
        p.add_run("File Size: ").bold = True
        p.add_run(f"{size_kb} KB")

    # Summary lines
    doc.add_paragraph(
        "Assets Check: " +
        ("✅ All assets present" if not missing_assets else "❌ Missing assets")
    )

    if banner_sizes:
        doc.add_paragraph("Banner Size(s): " + ", ".join(banner_sizes))

    if first_html:
        doc.add_paragraph("Border Check: " + first_html.get("border", ""))

    doc.add_paragraph(
        "HTML Validation: " +
        ("✅ Checked" if html_results else "❌ Not found")
    )

    doc.add_paragraph(
        "Loop Count: " +
        ("✅ Within limit" if not loop_issue else "❌ Loop count exceeds limit")
    )

    doc.add_paragraph(
        "Clickable Area: " +
        ("HTML/JS click detected" if not clickable_warning
         else "No clickable area detected")
    )

    doc.add_paragraph(
        f"Animation Duration: {durations.get('animation', 0)}s"
    )
    doc.add_paragraph(
        f"ISI Scroll Duration: {durations.get('isi', 0)}s"
    )
    doc.add_paragraph(
        f"Total Estimated Duration: {durations.get('total', 0)}s"
    )

    # ---- Detailed sections ----
    if html_results:
        doc.add_heading("HTML Details", level=2)
        for name, res in html_results.items():
            doc.add_heading(name, level=3)
            if res.get("banner_size"):
                doc.add_paragraph(f"Banner Size: {res['banner_size']}")
            doc.add_paragraph(f"Border: {res.get('border', '')}")
            if res.get("errors"):
                doc.add_paragraph("Errors:")
                for err in res["errors"]:
                    doc.add_paragraph(err, style="List Bullet")
            if res.get("warnings"):
                doc.add_paragraph("Warnings:")
                for warn in res["warnings"]:
                    doc.add_paragraph(warn, style="List Bullet")

    if js_results:
        doc.add_heading("JS Details", level=2)
        for name, res in js_results.items():
            doc.add_heading(name, level=3)
            doc.add_paragraph(
                f"Animation Duration: {res.get('duration', 0)}s"
            )
            doc.add_paragraph(
                f"ISI Scroll Duration: {res.get('isi_duration', 0)}s"
            )
            if res.get("errors"):
                doc.add_paragraph("Errors:")
                for err in res["errors"]:
                    doc.add_paragraph(err, style="List Bullet")
            if res.get("warnings"):
                doc.add_paragraph("Warnings:")
                for warn in res["warnings"]:
                    doc.add_paragraph(warn, style="List Bullet")

    # ---- Return as download ----
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)

    safe_name = os.path.splitext(file_name)[0] or "ad_validation_report"

    return send_file(
        buf,
        as_attachment=True,
        download_name=f"{safe_name}.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


# -------------------------------------------------------
# Run Server
# -------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

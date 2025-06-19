import os
import re
import zipfile
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
from flask import request

# Flask Configuration
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"html", "zip"}
EXPECTED_BANNER_SIZES = [(300, 250), (160, 600), (728, 90), (320, 50), (970, 250), (300, 50)]
MAX_FILE_SIZE_KB = 150
ANIMATION_MAX_DURATION = 15
MAX_LOOP_COUNT = 3
ANIMATION_WARNING_THRESHOLD = 14.8

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_zip(file_path):
    extracted_folder = os.path.join(UPLOAD_FOLDER, os.path.splitext(os.path.basename(file_path))[0])
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

        width_match = re.search(r"width\s*:\s*(\d+)px", css_content)
        height_match = re.search(r"height\s*:\s*(\d+)px", css_content)

        if width_match and height_match:
            return int(width_match.group(1)), int(height_match.group(1))
    except Exception as e:
        print(f"[ERROR] Error reading CSS file: {e}")
    return None, None

def check_border_in_css(css_content):
    return bool(re.search(r"border\s*:\s*1px\s+solid", css_content, re.IGNORECASE))

def validate_html(file_path):
    results = {"warnings": [], "errors": [], "banner_size": None, "border": "\u274c Missing 1px border"}
    if not os.path.exists(file_path):
        results["errors"].append(f"File {file_path} does not exist.")
        return results

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        soup = BeautifulSoup(file, "html.parser")

    base_path = os.path.dirname(file_path)
    missing_assets = []
    border_found = False

    css_files = [tag["href"] for tag in soup.find_all("link", {"rel": "stylesheet"}) if "href" in tag.attrs]

    css_width, css_height = None, None
    html_width, html_height = None, None

    for css_file in css_files:
        css_file_path = os.path.join(base_path, css_file)
        if not os.path.exists(css_file_path):
            continue
        with open(css_file_path, "r", encoding="utf-8", errors="replace") as f:
            css_content = f.read()
        if not css_width or not css_height:
            w, h = extract_ad_size_from_css(css_file_path)
            if w and h:
                css_width, css_height = w, h
        if check_border_in_css(css_content):
            border_found = True

    size_div = soup.find(attrs={"class": "adSize"})
    if size_div and "style" in size_div.attrs:
        style = size_div["style"]
        width_match = re.search(r"width\s*:\s*(\d+)px", style)
        height_match = re.search(r"height\s*:\s*(\d+)px", style)
        if width_match and height_match:
            html_width = int(width_match.group(1))
            html_height = int(height_match.group(1))

    banner_width = css_width or html_width
    banner_height = css_height or html_height

    if css_width and html_width and (css_width != html_width or css_height != html_height):
        results["warnings"].append(
            f"\u26a0\ufe0f Size mismatch: CSS says {css_width}x{css_height}, HTML inline style says {html_width}x{html_height}"
        )

    if border_found:
        results["border"] = "\u2705 1px border present"
    if banner_width and banner_height:
        results["banner_size"] = f"{banner_width}x{banner_height}"
        if (banner_width, banner_height) not in EXPECTED_BANNER_SIZES:
            results["errors"].append(
                f"Invalid banner size: {banner_width}x{banner_height}. Expected sizes: {EXPECTED_BANNER_SIZES}"
            )
    else:
        results["warnings"].append("\u26a0\ufe0f Could not determine banner size from CSS or HTML inline styles.")

    for tag in soup.find_all(["img", "script", "link"]):
        src = tag.get("src") or tag.get("href")
        if tag.name in ["script", "style"] and not src:
            continue
        if not src:
            results["warnings"].append(f"\u26a0\ufe0f Missing `src` or `href` attribute in <{tag.name}> tag.")
            continue
        if src.startswith("data:"):
            continue
        if not src.startswith(("http://", "https://")):
            asset_path = os.path.abspath(os.path.join(base_path, src.lstrip("/")))
            if not os.path.exists(asset_path):
                missing_assets.append(src)

    if missing_assets:
        results["errors"].append(f"Missing assets: {missing_assets}")

    return results

def validate_js(file_path):
    results = {"warnings": [], "errors": [], "duration": 0, "isi_duration": 0}
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            js_code = file.read()
    except Exception as e:
        results["errors"].append(f"Error reading JavaScript file {file_path}: {str(e)}")
        return results

    js_code = re.sub(r'//.*', '', js_code)

    frame_delays = sum([float(d) for d in re.findall(r"frameDelay\s*=\s*(\d+\.?\d*)", js_code)])
    delay_calls = sum([float(d) for d in re.findall(r"delayedCall\s*\(\s*(\d+\.?\d*)", js_code)])
    durations = sum([float(d) for d in re.findall(r"duration\s*:\s*(\d+\.?\d*)", js_code)])

    animation_duration = frame_delays + delay_calls + durations

    isi_scroll = 0.0
    isi_scroll_found = bool(re.search(r"scrollTo\s*:\s*\{[^}]*y\s*:", js_code)) or "ISIscroll" in js_code
    if isi_scroll_found:
        match = re.search(r"scrollSpeed\s*=\s*(\d+(\.\d+)?)", js_code)
        if match:
            isi_scroll = float(match.group(1))
        elif "scrollSpeed" in js_code and "creative.isi_height" in js_code:
            isi_scroll = 10.0

    total_duration = animation_duration + isi_scroll
    results["duration"] = round(animation_duration, 1)
    results["isi_duration"] = round(isi_scroll, 1)

    if total_duration > ANIMATION_MAX_DURATION:
        results["errors"].append(
            f"Estimated total animation duration exceeds {ANIMATION_MAX_DURATION}s: {total_duration:.1f}s"
        )
    elif total_duration >= ANIMATION_WARNING_THRESHOLD:
        results["warnings"].append(
            f"Estimated total animation duration approaching limit: {total_duration:.1f}s"
        )

    loops = re.findall(r"repeat\s*:\s*(\d+|Infinity|-1)", js_code)
    for loop in loops:
        if loop in ("Infinity", "-1") or (loop.isdigit() and int(loop) > MAX_LOOP_COUNT):
            results["errors"].append(f"Animation loop count exceeds {MAX_LOOP_COUNT}: {loop}")

    if "mainExit" not in js_code and "clickTag" not in js_code:
        results["warnings"].append("⚠️ No click tracking detected (missing 'mainExit' or 'clickTag').")

    return results





@app.route("/preview/<path:folder>/<filename>")
def preview_banner(folder, filename):
    if "__MACOSX" in folder or filename.startswith("."):
        return "Invalid preview request", 404
    folder_path = os.path.join(UPLOAD_FOLDER, folder)
    full_path = os.path.join(folder_path, filename)
    print(f"[INFO] Requested preview: {full_path}")
    if not os.path.exists(full_path):
        print("[ERROR] File not found:", full_path)
        return "File not found", 404
    return send_from_directory(folder_path, filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validate", methods=["POST"])
def validate_file():
    print("[INFO] Received a file upload request...")
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    file_size_kb = os.path.getsize(file_path) / 1024
    print(f"[INFO] Uploaded file size: {file_size_kb:.2f} KB")

    preview_links = []
    validation_results = {"html": {}, "js": {}}
    durations = {"animation": 0.0, "isi": 0.0, "total": 0.0}

    if filename.endswith(".zip"):
        extracted_folder = extract_zip(file_path)
        if not extracted_folder:
            return jsonify({"error": "Invalid ZIP file."}), 400
        html_files = []
        js_files = []
        for root, _, files in os.walk(extracted_folder):
            for file in files:
                if file.endswith(".html") and "__MACOSX" not in root:
                    html_path = os.path.join(root, file)
                    html_files.append(html_path)
                elif file.endswith(".js") and "__MACOSX" not in root:
                    js_files.append(os.path.join(root, file))
        if not html_files:
            return jsonify({"error": "No HTML file found in ZIP."}), 400
        for html_file in html_files:
         validation_results["html"][os.path.basename(html_file)] = validate_html(html_file)
         preview_folder = os.path.relpath(os.path.dirname(html_file), UPLOAD_FOLDER)
         relative_html_path = os.path.relpath(html_file, os.path.join(UPLOAD_FOLDER, preview_folder))
         url_base = request.host_url.replace("http://", "https://")
         preview_links.append(f"{url_base}preview/{preview_folder}/{relative_html_path}")

 
        for js_file in js_files:
            js_result = validate_js(js_file)
            validation_results["js"][os.path.basename(js_file)] = js_result
            durations["animation"] += js_result["duration"]
            durations["isi"] += js_result["isi_duration"]
    elif filename.endswith(".html"):
     validation_results["html"][filename] = validate_html(file_path)
     url_base = request.host_url.replace("http://", "https://")
     preview_links.append(f"{url_base}preview/{filename}")

    durations["animation"] = round(durations["animation"], 1)
    durations["isi"] = round(durations["isi"], 1)
    durations["total"] = round(durations["animation"] + durations["isi"], 1)

    return jsonify({
        "validation_results": validation_results,
        "previews": preview_links,
        "file_size_kb": round(file_size_kb, 2),
        "durations": durations
    })
#@app.route("/")
#def home():
    #return "Hello from HTML5 Ad Validator!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

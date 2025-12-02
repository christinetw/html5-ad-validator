🚀 HTML5 Ad Validator
Automated QA Tool for HTML5, Display, Dynamic & Video Banners





The HTML5 Ad Validator is an automated QA tool built to inspect ZIP or HTML banner files for:

Banner size & dimension validation

Asset completeness

ClickTag functionality

Animation duration limits

Loop count rules

Required 1px border

Missing assets

ISI scroll time

Multi-banner ZIP validation

Creatopy / Google / Sizmek compatible ads

Thumbnail preview of banners (scaled automatically)

Designed originally for professional digital advertising workflows (TD, Rogers, Pfizer, Citibank, etc.), this validator helps QA teams catch common errors instantly.

🔥 Features
✔️ HTML Validation

Detects invalid or missing HTML elements

Supports Creatopy-generated ads

Accepts both ZIPs and individual HTML files

✔️ Banner Size Detection

Automatically checks banner dimensions from:

CSS

Inline styles

.adSize DIV

<meta name="ad.size"> (Google)

SVG canvas root

✔️ Border Detection

Confirms presence of a required 1px border via:

CSS border

Inline style

Canvas API

SVG stroke

✔️ Missing Assets Detection

Flags any referenced images, scripts, or CSS not included in the ZIP.

✔️ ClickTag Detection

Detects:

HTML click layers (clickTagMain, clickLayer, clickable, etc.)

JS click handlers

Creatopy clickTag injection

SVG click events

✔️ Animation Rules

Max animation duration: 15s

Warning at 14.8s

Loop count max: 3

Detects GSAP delayedCall, frameDelay, repeat, ISI scroll, etc.

✔️ Batch Validation

Upload a single ZIP containing many ZIPs
→ Each banner validated individually
→ Side-by-side preview grid

✔️ Preview Grid with Auto-Scaling

Each banner is displayed in an <iframe> scaled according to its size:

300×250

160×600

728×90

970×250

320×50

etc.

Perfect for reviewing all deliverables at once.

📂 File Structure
html5-ad-validator/
│
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── uploads/          (auto-generated)
├── Dockerfile
├── fly.toml
└── README.md

🛠 Installation (Local)
1. Clone the repository
git clone https://github.com/christinetw/html5-ad-validator.git
cd html5-ad-validator

2. Create virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS

3. Install dependencies
pip3 install -r requirements.txt

4. Run locally
python3 app.py

5. Open in browser
http://127.0.0.1:8080


You should also see:

Running on http://192.168.xx.xx:8080


Meaning you can use the tool on your iPhone/iPad connected to the same Wi-Fi.

☁️ Deploying to Fly.io (Production)
1. Log in
flyctl auth login

2. Create the app
flyctl launch

3. Deploy
flyctl deploy

4. Open live validator
flyctl open

🧪 How to Use
✔ Upload Options:

One ZIP containing one banner

One ZIP containing many ZIPs

Single HTML files

The validator will automatically generate:

Banner frames

HTML report

JS report

Highlighted warnings/errors

Auto-scaled previews

Optional Word/PDF export (coming soon)

📸 Screenshot (replace with your own)

Add your own screenshots here. Best practice:

Preview grid

Results panel

Word/PDF export

ClickTag detection

Example:

![PreviewGrid](docs/preview-grid.png)
![Validation](docs/validation-results.png)

🧩 Roadmap
v2.0 (Coming Soon)

🟦 Word (.docx) full report export

📸 Auto-thumbnail screenshot per banner

🔄 Drag-and-drop multi-ZIP uploader

🎨 Better UI + dark mode

📊 CSV/Excel export

🤖 Auto-AI “what’s wrong with this ad?” suggestions

❤️ Credits

Created by Christine Lo
Digital QA Engineer / Automation Developer
Publicis Groupe

If you're using this tool at work, feel free to ⭐ star the repo!

📬 Support

If you need help improving the validator or adding new features, open an Issue or DM me.
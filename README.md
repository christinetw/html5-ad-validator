# HTML5 Ad Validator 🧪

This tool checks HTML5 banner ad files to ensure they follow industry best practices and are safe to use in campaigns.

## 📦 What's Included

- `app.py` — Flask server (backend)
- `templates/index.html` — Frontend UI for uploading and previewing
- `uploads/` — Temporary directory for uploaded files (created automatically)

## 🚀 What This Tool Does

This validator checks:

- ✅ Correct banner sizes (e.g., 300x250, 728x90)
- ✅ File weight (e.g., 150kb)
- ✅ All assets included (images, scripts, etc.)
- ✅ Animation time and loop count limits
- ✅ Presence of click tracking (`clickTag` or `mainExit`)
- ✅ Visual previews of banners

## 🧠 How It Works

1. Upload a ZIP or HTML file.
2. The app unpacks and analyzes the contents.
3. It checks:
   - Valid banner size from CSS
   - All required files (images, JS, etc.)
   - Animation rules (≤15s, ≤3 loops)
   - Click tracking tag
4. Results are shown in a detailed UI with:
   - ✅ Pass
   - ⚠️ Warnings
   - 🛑 Errors
5. If available, banners are previewed inline via iframe.

## 🛠 How to Run Locally

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/html5-ad-validator.git
   cd html5-ad-validator
   ```

2. **Install dependencies**  
   ```bash
   pip install flask
   ```

3. **Run the Flask server**  
   ```bash
   python3 app.py
   ```

4. **Open in your browser**  
   Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🌐 Share on Local Network

To make it accessible to others on the same Wi-Fi:

```bash
python app.py --host=0.0.0.0 --port=5000
```

Others can access it via:
```
http://your-local-ip:5000
```

---

## ✅ Example Errors This Tool Catches

- "your banner is 728x100 but it should be 728x90."
- "Missing file: logo.png"
- "Animation duration exceeds 15s limit"
- "Loop count exceeds allowed maximum"


---

## 📄 License

MIT — free to use and modify. Contributions welcome!

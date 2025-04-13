
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validate", methods=["POST"])
def validate_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    file_size_kb = os.path.getsize(file_path) / 1024

    # Dummy validation results
    return jsonify({
        "file_size_kb": round(file_size_kb, 2),
        "validation_results": {
            "html": {
                file.filename: {
                    "banner_size": "300x250",
                    "warnings": [],
                    "errors": []
                }
            },
            "js": {}
        },
        "previews": []
    })

if __name__ == "__main__":
    app.run(debug=True)

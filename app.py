# app.py
from flask import Flask, render_template, jsonify, request
import os
from werkzeug.utils import secure_filename
from utils.processor import process_file

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "success", "message": "Backend is running perfectly."})

@app.route('/api/evaluate', methods=['POST'])
def evaluate_content():
    extracted_text = ""
    source_type = ""

    # Check if a file was uploaded
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file
            extracted_text = process_file(filepath)
            source_type = "File Upload"
            
            # Delete the file after processing to save space
            os.remove(filepath)
        else:
            return jsonify({"status": "error", "message": "Unsupported file format. Please upload PDF, DOCX, or TXT."})

    # Check if raw text was pasted
    elif 'text' in request.form and request.form['text'].strip() != "":
        extracted_text = request.form['text']
        source_type = "Pasted Text"
        
    else:
        return jsonify({"status": "error", "message": "No content provided. Please upload a file or paste text."})

    # Error handling if text extraction failed
    if not extracted_text:
        return jsonify({"status": "error", "message": "Could not extract text. The file might be empty or corrupted."})

    return jsonify({
        "status": "success",
        "message": "Text processed successfully",
        "source": source_type,
        "extracted_characters": len(extracted_text),
        "preview": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
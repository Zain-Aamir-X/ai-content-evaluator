from flask import Flask, render_template, jsonify, request
import os
from werkzeug.utils import secure_filename

# Import our custom modules (make sure these files exist!)
from utils.processor import process_file, mock_evaluate_text
from models import db, Content, EvaluationReport

app = Flask(__name__)

# ==========================================
# 1. Configuration Settings
# ==========================================
# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

# Database Configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================================
# 2. Database Initialization
# ==========================================
db.init_app(app)

# Create the database tables within the application context
with app.app_context():
    db.create_all()

# ==========================================
# 3. Helper Functions
# ==========================================
def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==========================================
# 4. Routes / API Endpoints
# ==========================================

@app.route('/')
def home():
    """Renders the main frontend UI."""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple endpoint to test if backend is running."""
    return jsonify({"status": "success", "message": "Backend is running perfectly."})

@app.route('/api/evaluate', methods=['POST'])
def evaluate_content():
    """
    Main evaluation pipeline:
    1. Extracts text from file or form data.
    2. Runs Mock ML evaluation.
    3. Saves to SQLite Database.
    4. Returns JSON to frontend.
    """
    extracted_text = ""
    source_type = ""

    # --- STEP A: Extract Text ---
    # Check if a file was uploaded
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file using utils/processor.py
            extracted_text = process_file(filepath)
            source_type = "File Upload"
            
            # Delete the file after processing to save disk space
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

    # --- STEP B: Get Mock ML Results ---
    # (On Day 5, this will be replaced by your actual ML models)
    ml_results = mock_evaluate_text(extracted_text)

    # --- STEP C: Save to Database ---
    try:
        # 1. Save the raw content
        new_content = Content(text_data=extracted_text, source_type=source_type)
        db.session.add(new_content)
        db.session.commit()

        # 2. Save the evaluation report linked to the content
        new_report = EvaluationReport(
            content_id=new_content.id,
            linguistic_label=ml_results['linguistic']['label'],
            cognitive_label=ml_results['cognitive']['label'],
            socio_emotional_label=ml_results['socio_emotional']['label'],
            moral_label=ml_results['moral']['label'],
            
            linguistic_feedback=ml_results['linguistic']['feedback'],
            cognitive_feedback=ml_results['cognitive']['feedback'],
            socio_emotional_feedback=ml_results['socio_emotional']['feedback'],
            moral_feedback=ml_results['moral']['feedback']
        )
        db.session.add(new_report)
        db.session.commit()

        # --- STEP D: Return JSON to Frontend ---
        return jsonify({
            "status": "success",
            "message": "Evaluation complete",
            "report_id": new_report.id,
            "results": ml_results
        })

    except Exception as e:
        # If the database crashes, rollback and inform the user
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Database error: {str(e)}"})

# ==========================================
# 5. Run the App
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
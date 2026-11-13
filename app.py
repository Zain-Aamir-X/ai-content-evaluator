# app.py
from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# 1. Route for the Frontend UI
@app.route('/')
def home():
    return render_template('index.html')

# 2. Health Check API Endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Backend is running perfectly."
    })

# 3. Placeholder for the Evaluation Endpoint
@app.route('/api/evaluate', methods=['POST'])
def evaluate_content():
    return jsonify({
        "status": "error",
        "message": "Evaluation pipeline not connected yet. Check back on Day 5!"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
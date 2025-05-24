from flask import Flask, request, jsonify
from flask_cors import CORS
from services.ats_analyzer import ATSAnalyzer
from services.resume_tailor import ResumeTailor
import os

app = Flask(__name__)
CORS(app)

# Initialize services
ats_analyzer = ATSAnalyzer()
resume_tailor = ResumeTailor()

@app.route('/api/resume/analyze', methods=['POST'])
def analyze_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Save the file temporarily
        temp_path = os.path.join('/tmp', file.filename)
        file.save(temp_path)
        
        # Analyze the resume
        score, recommendations = ats_analyzer.analyze(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            'score': score,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/resume/tailor', methods=['POST'])
def tailor_resume():
    data = request.json
    if not data or 'resume' not in data or 'job_description' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        tailored_resume = resume_tailor.tailor_resume(
            data['resume'],
            data['job_description']
        )
        return jsonify({'tailored_resume': tailored_resume})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
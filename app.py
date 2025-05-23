from flask import Flask, request, jsonify
from flask_cors import CORS
from ats_analyzer import ATSAnalyzer

app = Flask(__name__)
CORS(app)

ats_analyzer = ATSAnalyzer()

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Get file extension
    file_type = file.filename.split('.')[-1].lower()
    if file_type not in ['pdf', 'doc', 'docx']:
        return jsonify({'error': 'Unsupported file type'}), 400
    
    try:
        # Read file content
        file_content = file.read()
        
        # Analyze resume
        result = ats_analyzer.analyze_resume(file_content, file_type)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
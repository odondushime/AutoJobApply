from flask import Blueprint, request, jsonify
from ..services.resume_tailor import ResumeTailor
from ..services.ats_analyzer import ATSAnalyzer

resume_bp = Blueprint('resume', __name__)
resume_tailor = ResumeTailor()
ats_analyzer = ATSAnalyzer()

@resume_bp.route('/analyze', methods=['POST'])
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

@resume_bp.route('/tailor', methods=['POST'])
def tailor_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    if 'job_description' not in request.form:
        return jsonify({'error': 'No job description provided'}), 400
    
    file = request.files['file']
    job_description = request.form['job_description']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Get file extension
    file_type = file.filename.split('.')[-1].lower()
    if file_type not in ['pdf', 'doc', 'docx']:
        return jsonify({'error': 'Unsupported file type'}), 400
    
    try:
        # Read file content
        file_content = file.read()
        
        # Extract text based on file type
        if file_type == 'pdf':
            resume_text = ats_analyzer.extract_text_from_pdf(file_content)
        else:  # doc or docx
            resume_text = ats_analyzer.extract_text_from_docx(file_content)
        
        # Tailor resume
        optimized_resume, analysis = resume_tailor.get_optimized_resume(resume_text, job_description)
        
        return jsonify({
            'analysis': analysis,
            'optimized_resume': optimized_resume
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
# AutoJobApply

A modern web application that helps job seekers optimize their resumes for ATS (Applicant Tracking Systems) and tailor them to specific job descriptions.

## Features

- **ATS Analysis**: Get your resume analyzed for ATS compatibility
- **Resume Tailoring**: Automatically customize your resume for specific job descriptions
- **Smart Recommendations**: Receive actionable suggestions to improve your resume
- **Modern UI**: Beautiful, responsive interface with real-time feedback

## Tech Stack

### Frontend

- React with TypeScript
- Tailwind CSS for styling
- Framer Motion for animations
- Vite for build tooling

### Backend

- Flask (Python)
- PyPDF2 for PDF processing
- python-docx for DOCX processing

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/AutoJobApply.git
cd AutoJobApply
```

2. Set up the backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

3. Set up the frontend:

```bash
cd frontend
npm install
npm run dev
```

4. Open http://localhost:5173 in your browser

## Usage

1. Upload your resume (PDF or DOCX format)
2. Get instant ATS compatibility analysis
3. Enter a job description to get a tailored version of your resume
4. Follow the recommendations to improve your resume

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

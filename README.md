# AutoJobApply

A modern web application that automates job applications across multiple job boards and provides ATS resume analysis. Built with React, TypeScript, Flask, and Selenium.

## Features

- 🔍 **Job Search**: Search for jobs across multiple job boards with advanced filters
- 🤖 **Automated Applications**: Apply to jobs with a single click
- 📊 **Dashboard**: Track your application progress and statistics
- ⚙️ **Settings Management**: Configure your credentials and documents
- 🔒 **Secure**: Credentials and sensitive data are stored securely
- 🌐 **Modern UI**: Beautiful and responsive interface built with React and Tailwind CSS
- 📝 **ATS Resume Analysis**: Get instant feedback on your resume's ATS compatibility

## Tech Stack

### Frontend

- React 18
- TypeScript
- Tailwind CSS
- Vite
- React Router
- Axios

### Backend

- Flask
- Python 3.11+
- Selenium
- PyPDF2
- python-docx

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Chrome browser
- ChromeDriver (automatically installed by the application)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/odondushime/AutoJobApply.git
cd AutoJobApply
```

2. Set up the backend:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:

```bash
cd frontend
npm install
```

4. Create a `.env` file in the root directory:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
RESUME_PATH=/path/to/your/resume.pdf
COVER_LETTER_PATH=/path/to/your/cover_letter.pdf
```

## Running the Application

1. Start the backend server:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

2. Start the frontend development server:

```bash
cd frontend
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## Usage

1. **ATS Resume Analysis**

   - Upload your resume (PDF or DOCX)
   - Get instant ATS compatibility score
   - Receive specific recommendations for improvement
   - Track your resume's performance

2. **Dashboard**

   - View application statistics
   - Track recent applications
   - Monitor success rates

3. **Job Search**

   - Enter keywords and location
   - Filter by job board, date, and more
   - Save interesting jobs for later

4. **Settings**
   - Configure job board credentials
   - Upload resume and cover letter
   - Set application preferences

## Project Structure

```
AutoJobApply/
├── backend/
│   ├── ats_analyzer.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── app.py
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

- Credentials are stored securely using environment variables
- No sensitive data is stored in the database
- HTTPS is enforced in production
- Regular security updates and dependency checks

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- Selenium WebDriver for browser automation
- Flask for the backend framework
- React and Tailwind CSS for the frontend
- All contributors and users of the project

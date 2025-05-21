# AutoJobApply

A modern web application for automating job applications across multiple job boards.

## Features

- Beautiful, responsive UI built with React and Tailwind CSS
- Automated job search and application process
- Support for multiple job boards (LinkedIn, Indeed, Glassdoor)
- Secure credential management
- Real-time application tracking
- Customizable cover letter generation

## Tech Stack

### Frontend

- React with TypeScript
- Vite for fast development and building
- Tailwind CSS for styling
- React Query for data fetching
- React Router for navigation
- Headless UI for accessible components
- Heroicons for beautiful icons

To run:
cd frontend
npm install
npm run dev

### Backend

- FastAPI for high-performance API
- Pydantic for data validation
- Selenium for web automation
- Python for backend logic

To run:
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Chrome browser (for Selenium)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/AutoJobApply.git
cd AutoJobApply
```

2. Set up the frontend:

```bash
cd frontend
npm install
npm run dev
```

3. Set up the backend:

```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

4. Configure your settings:

- Copy `.env.example` to `.env` in the backend directory
- Update the environment variables with your credentials

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Set up your profile and credentials in the Settings page
3. Use the Job Search page to find and apply to jobs
4. Track your applications in the Dashboard

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

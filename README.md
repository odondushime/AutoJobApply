# AutoJobApply

Automate your job search and application process across multiple job boards and direct company sites using Selenium and OpenAI.

## Features

- Automated job search and application on major job boards (Indeed, LinkedIn, WellFound, ZipRecruiter, Welcome to the Jungle, BuiltIn, RepVue, Hired, Lever, Greenhouse, and direct company sites)
- Resume and cover letter upload (cover letter can be generated with OpenAI API)
- Modular, extensible codebase for adding new job boards
- Configurable job search preferences (keywords, salary, remote/hybrid, etc.)
- Application logging and status tracking
- Secure handling of credentials (via `.env`)

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/AutoJobApply.git
   cd AutoJobApply
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Add your resume:**
   - Place your resume as `resume.pdf` in the `resumes/` folder.
5. **Configure your job search:**
   - Edit `config.json` to set your job preferences, credentials, and enabled job boards.
6. **Set up environment variables:**
   - Create a `.env` file in the project root with your sensitive credentials (see below).

### Example `.env` file

```
OPENAI_API_KEY=your_openai_api_key
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password
# Add other credentials as needed
```

**Never commit your `.env` file or sensitive data to GitHub!**

## Usage

Run the main script:

```bash
python job_scraper.py
```

- The script will search and apply for jobs based on your configuration.
- Manual intervention may be required for CAPTCHAs or SSO logins.
- Applications are logged in `applications_db.csv`.

## Adding/Removing Job Boards

- Enable or disable job boards in `config.json` under the `enabled_job_boards` section.
- To add a new board, create a new class in `job_boards/` following the base class pattern.

## Security

- Store all sensitive credentials in `.env`.
- `.gitignore` is set up to exclude `.env`, logs, and other sensitive files.

## Contributing

Contributions are welcome! If you have ideas for new job boards, features, or improvements, feel free to open an issue or submit a pull request.

**Want to add your favorite job board or improve the automation? Fork this repo and send a PR!**

## License

MIT License

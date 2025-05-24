from flask import Flask
from flask_cors import CORS
from backend.api.resume import resume_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(resume_bp, url_prefix='/api/resume')

if __name__ == '__main__':
    app.run(debug=True) 
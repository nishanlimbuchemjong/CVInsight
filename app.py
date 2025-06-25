# from flask import Flask, request
# from werkzeug.utils import secure_filename
# import os
# from drive_upload import upload_to_drive


# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/upload', methods=['GET','POST'])
# def upload_resume():
#     if request.method == 'POST':
#         # Use .get() to avoid KeyError if file missing
#         file = request.files.get('resume')
#         if not file:
#             return "No file part named 'resume' found in the request", 400
        
#         filename = secure_filename(file.filename)
#         if filename == '':
#             return "No selected file", 400
        
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(filepath)
        
#         # Here, call your upload_to_drive function...
#         # file_id = upload_to_drive(filepath, filename)

#         return f"File {filename} saved and ready to upload."
    
#     # For GET request, show upload form
#     return '''
#     <h2>Upload Resume</h2>
#     <form method="POST" enctype="multipart/form-data">
#         <input type="file" name="resume" required>
#         <input type="submit" value="Upload">
#     </form>
#     '''
    

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

from models import db, Resume
from drive_upload import upload_to_drive
from resume_parser import extract_text, extract_details
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Create uploads folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost/cvinsight_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')
    if not file:
        return "No file uploaded.", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        drive_link = upload_to_drive(filepath, filename)
    except Exception as e:
        return f"Error uploading to Google Drive: {e}"

    text = extract_text(filepath)
    info = extract_details(text)

    resume = Resume(
        name=info.get('name'),
        email=info.get('email'),
        phone=info.get('phone'),
        skills=info.get('skills'),
        filename=filename,
        drive_link=drive_link
    )
    db.session.add(resume)
    db.session.commit()

    return render_template('result.html', resume=resume)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

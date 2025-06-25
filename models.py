from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    skills = db.Column(db.Text)
    drive_link = db.Column(db.String(300))
    filename = db.Column(db.String(100))

    def __repr__(self):
        return f'<Resume {self.name}>'

# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class Resume(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(200))
#     text = db.Column(db.Text)
#     uploaded_at = db.Column(db.DateTime, server_default=db.func.now())

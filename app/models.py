from datetime import datetime
import hashlib
from flask_login import UserMixin
from . import db, login_manager


# ----------------------------
# Login Loader
# ----------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------------------
# Association Table
# ----------------------------
project_skills = db.Table(
    "project_skills",
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
    db.Column("skill_id", db.Integer, db.ForeignKey("skill.id"), primary_key=True),
)


# ----------------------------
# User Model
# ----------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Identity
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    mobile = db.Column(db.String(20))
    headline = db.Column(db.String(200))
    introduction = db.Column(db.Text)
    location = db.Column(db.String(100))

    profile_photo = db.Column(db.String(300))  # stored image path

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    skills = db.relationship(
        "Skill",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Skill.display_order",
    )

    projects = db.relationship(
        "Project",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Project.created_at.desc()",
    )

    education = db.relationship(
        "Education",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Education.start_year.desc()",
    )

    social_links = db.relationship(
        "SocialLink",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    experiences = db.relationship(
        "Experience",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Experience.start_date.desc()",
    )

    certifications = db.relationship(
        "Certification",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User {self.username}>"

    # ----------------------------
    # Profile Image (Gravatar fallback)
    # ----------------------------
    def get_profile_image(self):
        if self.profile_photo:
            return self.profile_photo

        email_hash = hashlib.md5(self.email.lower().encode()).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s=200&d=identicon"


# ----------------------------
# Skill Model
# ----------------------------
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    level = db.Column(db.Integer)
    icon_class = db.Column(db.String(100))

    display_order = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Skill {self.name}>"


# ----------------------------
# Project Model
# ----------------------------
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    github_link = db.Column(db.String(300))
    live_link = db.Column(db.String(300))

    featured = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    skills = db.relationship(
        "Skill",
        secondary=project_skills,
        backref=db.backref("projects", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<Project {self.name}>"


# ----------------------------
# Education Model
# ----------------------------
class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    degree = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)

    start_year = db.Column(db.String(10))
    end_year = db.Column(db.String(10))
    description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Education {self.degree}>"


# ----------------------------
# Social Links
# ----------------------------
class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    platform = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    icon_class = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SocialLink {self.platform}>"


# ----------------------------
# Experience Model
# ----------------------------
class Experience(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    company = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(200), nullable=False)

    location = db.Column(db.String(200))

    start_date = db.Column(db.String(20))

    end_date = db.Column(db.String(20))

    description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Experience {self.company}>"


# ----------------------------
# Certification Model
# ----------------------------
class Certification(db.Model):

    __tablename__ = "certifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)

    organization = db.Column(db.String(200))

    issue_date = db.Column(db.Date)

    credential_url = db.Column(db.String(300))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Certification {self.title}>"

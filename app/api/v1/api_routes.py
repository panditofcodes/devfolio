from flask import Blueprint, jsonify
from ...models import (
    User,
    Skill,
    Project,
    Education,
    SocialLink,
    Experience,
    Certification,
)

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


# -----------------------------------
# Helpers
# -----------------------------------


def get_user(username):
    return User.query.filter_by(username=username).first_or_404()


def serialize_date(value):
    if not value:
        return None
    return value.strftime("%Y-%m-%d") if hasattr(value, "strftime") else str(value)


# -----------------------------------
# API Root
# -----------------------------------


@api_bp.route("/")
def api_home():

    return jsonify(
        {
            "service": "Portfolio API",
            "version": "v1",
            "endpoints": {
                "portfolio": "/api/v1/u/<username>/portfolio",
                "skills": "/api/v1/u/<username>/skills",
                "projects": "/api/v1/u/<username>/projects",
                "education": "/api/v1/u/<username>/education",
                "experience": "/api/v1/u/<username>/experience",
                "certifications": "/api/v1/u/<username>/certifications",
                "social": "/api/v1/u/<username>/social",
            },
        }
    )


# -----------------------------------
# Full Portfolio
# -----------------------------------


@api_bp.route("/u/<username>/portfolio")
def portfolio(username):

    user = get_user(username)

    profile = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "headline": user.headline,
        "introduction": user.introduction,
        "location": user.location,
        "email": user.email,
        "mobile": user.mobile,
        "profile_photo": user.get_profile_image(),
    }

    skills = [
        {
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "level": s.level,
            "icon": s.icon_class,
        }
        for s in Skill.query.filter_by(user_id=user.id)
    ]

    projects = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "github": p.github_link,
            "live": p.live_link,
            "featured": p.featured,
            "skills": [skill.name for skill in p.skills],
        }
        for p in Project.query.filter_by(user_id=user.id)
    ]

    experience = [
        {
            "id": e.id,
            "company": e.company,
            "role": e.role,
            "location": e.location,
            "start_date": serialize_date(e.start_date),
            "end_date": serialize_date(e.end_date),
            "description": e.description,
        }
        for e in Experience.query.filter_by(user_id=user.id).order_by(
            Experience.start_date.desc()
        )
    ]

    education = [
        {
            "id": e.id,
            "degree": e.degree,
            "institution": e.institution,
            "start_year": e.start_year,
            "end_year": e.end_year,
            "description": e.description,
        }
        for e in Education.query.filter_by(user_id=user.id)
    ]

    certifications = [
        {
            "id": c.id,
            "title": c.title,
            "organization": c.organization,
            "issue_date": serialize_date(c.issue_date),
            "credential_url": c.credential_url,
        }
        for c in Certification.query.filter_by(user_id=user.id).order_by(
            Certification.issue_date.desc()
        )
    ]

    social_links = [
        {
            "platform": s.platform,
            "url": s.url,
            "icon": s.icon_class,
        }
        for s in SocialLink.query.filter_by(user_id=user.id)
    ]

    return jsonify(
        {
            "profile": profile,
            "skills": skills,
            "projects": projects,
            "experience": experience,
            "education": education,
            "certifications": certifications,
            "social_links": social_links,
        }
    )


# -----------------------------------
# Skills
# -----------------------------------


@api_bp.route("/u/<username>/skills")
def skills(username):

    user = get_user(username)

    data = [
        {
            "name": s.name,
            "category": s.category,
            "level": s.level,
            "icon": s.icon_class,
        }
        for s in Skill.query.filter_by(user_id=user.id)
    ]

    return jsonify(data)


# -----------------------------------
# Projects
# -----------------------------------


@api_bp.route("/u/<username>/projects")
def projects(username):

    user = get_user(username)

    data = [
        {
            "name": p.name,
            "description": p.description,
            "github": p.github_link,
            "live": p.live_link,
            "featured": p.featured,
            "skills": [s.name for s in p.skills],
        }
        for p in Project.query.filter_by(user_id=user.id)
    ]

    return jsonify(data)


# -----------------------------------
# Education
# -----------------------------------


@api_bp.route("/u/<username>/education")
def education(username):

    user = get_user(username)

    data = [
        {
            "degree": e.degree,
            "institution": e.institution,
            "start_year": e.start_year,
            "end_year": e.end_year,
            "description": e.description,
        }
        for e in Education.query.filter_by(user_id=user.id)
    ]

    return jsonify(data)


# -----------------------------------
# Social Links
# -----------------------------------


@api_bp.route("/u/<username>/social")
def social(username):

    user = get_user(username)

    data = [
        {
            "platform": s.platform,
            "url": s.url,
            "icon": s.icon_class,
        }
        for s in SocialLink.query.filter_by(user_id=user.id)
    ]

    return jsonify(data)

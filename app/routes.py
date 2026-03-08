from flask import Blueprint, jsonify
from .models import Skill, Project, User

api_bp = Blueprint("api", __name__)


@api_bp.route("/skills")
def get_skills():
    skills = Skill.query.order_by(Skill.display_order).all()

    return jsonify([
        {
            "id": skill.id,
            "name": skill.name,
            "category": skill.category,
            "level": skill.level,
            "icon": skill.icon_class
        }
        for skill in skills
    ])
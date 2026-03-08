from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from wtforms import form
from .forms import (
    LoginForm,
    SkillForm,
    ProjectForm,
    ProfileForm,
    EducationForm,
    SocialLinkForm,
    ExperienceForm,
    CertificationForm,
)
from .models import (
    Experience,
    User,
    Skill,
    Project,
    Education,
    SocialLink,
    Certification,
)
from . import db
import os
from flask import request

admin_bp = Blueprint("admin", __name__)


# ==================================
# AUTH
# ==================================


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


# ==================================
# DASHBOARD
# ==================================


@admin_bp.route("/dashboard")
@login_required
def dashboard():

    skills_count = Skill.query.filter_by(user_id=current_user.id).count()
    projects_count = Project.query.filter_by(user_id=current_user.id).count()
    education_count = Education.query.filter_by(user_id=current_user.id).count()
    social_count = SocialLink.query.filter_by(user_id=current_user.id).count()

    return render_template(
        "admin/dashboard.html",
        skills_count=skills_count,
        projects_count=projects_count,
        education_count=education_count,
        social_count=social_count,
    )


# ==================================
# PROFILE
# ==================================


@admin_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user
    form = ProfileForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.mobile = form.mobile.data
        user.headline = form.headline.data
        user.introduction = form.introduction.data
        user.location = form.location.data

        if form.profile_photo.data:
            filename = secure_filename(form.profile_photo.data.filename)
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            form.profile_photo.data.save(filepath)
            user.profile_photo = f"/static/uploads/{filename}"

        db.session.commit()
        flash("Profile updated successfully", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/profile_form.html", form=form, user=user)


# ==================================
# SKILLS
# ==================================


@admin_bp.route("/skills")
@login_required
def skills_list():
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    return render_template("admin/skills_list.html", skills=skills)


@admin_bp.route("/skills/new", methods=["GET", "POST"])
@login_required
def skill_create():
    form = SkillForm()

    if form.validate_on_submit():
        skill = Skill(
            user_id=current_user.id,
            name=form.name.data,
            category=form.category.data,
            level=form.level.data,
            icon_class=form.icon_class.data,
        )
        db.session.add(skill)
        db.session.commit()
        flash("Skill created successfully", "success")
        return redirect(url_for("admin.skills_list"))

    return render_template("admin/skill_form.html", form=form)


@admin_bp.route("/skills/<int:id>/edit", methods=["GET", "POST"])
@login_required
def skill_edit(id):
    skill = Skill.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = SkillForm(obj=skill)

    if form.validate_on_submit():
        skill.name = form.name.data
        skill.category = form.category.data
        skill.level = form.level.data
        skill.icon_class = form.icon_class.data

        db.session.commit()
        flash("Skill updated successfully", "success")
        return redirect(url_for("admin.skills_list"))

    return render_template("admin/skill_form.html", form=form)


@admin_bp.route("/skills/<int:id>/delete", methods=["POST"])
@login_required
def skill_delete(id):
    skill = Skill.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(skill)
    db.session.commit()
    flash("Skill deleted", "warning")
    return redirect(url_for("admin.skills_list"))


# ==================================
# PROJECTS
# ==================================


@admin_bp.route("/projects")
@login_required
def projects_list():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template("admin/projects_list.html", projects=projects)


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def project_create():
    form = ProjectForm()
    form.skills.choices = [
        (s.id, s.name) for s in Skill.query.filter_by(user_id=current_user.id).all()
    ]

    if form.validate_on_submit():
        project = Project(
            user_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            github_link=form.github_link.data,
            live_link=form.live_link.data,
        )

        selected_skills = Skill.query.filter(
            Skill.id.in_(form.skills.data), Skill.user_id == current_user.id
        ).all()

        project.skills = selected_skills

        db.session.add(project)
        db.session.commit()
        flash("Project created successfully", "success")
        return redirect(url_for("admin.projects_list"))

    return render_template("admin/project_form.html", form=form)


@admin_bp.route("/projects/<int:id>/edit", methods=["GET", "POST"])
@login_required
def project_edit(id):
    project = Project.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = ProjectForm(obj=project)

    form.skills.choices = [
        (s.id, s.name) for s in Skill.query.filter_by(user_id=current_user.id).all()
    ]

    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.github_link = form.github_link.data
        project.live_link = form.live_link.data

        selected_skills = Skill.query.filter(
            Skill.id.in_(form.skills.data), Skill.user_id == current_user.id
        ).all()

        project.skills = selected_skills

        db.session.commit()
        flash("Project updated successfully", "success")
        return redirect(url_for("admin.projects_list"))

    form.skills.data = [s.id for s in project.skills]

    return render_template("admin/project_form.html", form=form)


@admin_bp.route("/projects/<int:id>/delete", methods=["POST"])
@login_required
def project_delete(id):
    project = Project.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted", "warning")
    return redirect(url_for("admin.projects_list"))


# ==================================
# EDUCATION
# ==================================


@admin_bp.route("/education")
@login_required
def education_list():
    education = Education.query.filter_by(user_id=current_user.id).all()
    return render_template("admin/education_list.html", education=education)


@admin_bp.route("/education/new", methods=["GET", "POST"])
@login_required
def education_create():
    form = EducationForm()

    if form.validate_on_submit():
        edu = Education(
            user_id=current_user.id,
            degree=form.degree.data,
            institution=form.institution.data,
            start_year=form.start_year.data,
            end_year=form.end_year.data,
            description=form.description.data,
        )
        db.session.add(edu)
        db.session.commit()
        flash("Education added", "success")
        return redirect(url_for("admin.education_list"))

    return render_template("admin/education_form.html", form=form)


@admin_bp.route("/education/<int:id>/edit", methods=["GET", "POST"])
@login_required
def education_edit(id):
    edu = Education.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = EducationForm(obj=edu)

    if form.validate_on_submit():
        edu.degree = form.degree.data
        edu.institution = form.institution.data
        edu.start_year = form.start_year.data
        edu.end_year = form.end_year.data
        edu.description = form.description.data

        db.session.commit()
        flash("Education updated", "success")
        return redirect(url_for("admin.education_list"))

    return render_template("admin/education_form.html", form=form)


@admin_bp.route("/education/<int:id>/delete", methods=["POST"])
@login_required
def education_delete(id):
    edu = Education.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(edu)
    db.session.commit()
    flash("Education deleted", "warning")
    return redirect(url_for("admin.education_list"))


# ==================================
# SOCIAL LINKS
# ==================================


@admin_bp.route("/social")
@login_required
def social_list():
    links = SocialLink.query.filter_by(user_id=current_user.id).all()
    return render_template("admin/social_list.html", links=links)


@admin_bp.route("/social/new", methods=["GET", "POST"])
@login_required
def social_create():
    form = SocialLinkForm()

    if form.validate_on_submit():
        link = SocialLink(
            user_id=current_user.id,
            platform=form.platform.data,
            url=form.url.data,
            icon_class=form.icon_class.data,
        )
        db.session.add(link)
        db.session.commit()
        flash("Social link added", "success")
        return redirect(url_for("admin.social_list"))

    return render_template("admin/social_form.html", form=form)


@admin_bp.route("/social/<int:id>/edit", methods=["GET", "POST"])
@login_required
def social_edit(id):
    link = SocialLink.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = SocialLinkForm(obj=link)

    if form.validate_on_submit():
        link.platform = form.platform.data
        link.url = form.url.data
        link.icon_class = form.icon_class.data

        db.session.commit()
        flash("Social link updated", "success")
        return redirect(url_for("admin.social_list"))

    return render_template("admin/social_form.html", form=form)


@admin_bp.route("/social/<int:id>/delete", methods=["POST"])
@login_required
def social_delete(id):
    link = SocialLink.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(link)
    db.session.commit()
    flash("Social link deleted", "warning")
    return redirect(url_for("admin.social_list"))


# =========================
# EXPERIENCE
# =========================


@admin_bp.route("/experience")
@login_required
def experience_list():

    experiences = Experience.query.all()

    return render_template("admin/experience_list.html", experiences=experiences)


@admin_bp.route("/experience/new", methods=["GET", "POST"])
@login_required
def experience_create():

    form = ExperienceForm()

    if form.validate_on_submit():

        print("FORM VALIDATED")

        exp = Experience(
            user_id=current_user.id,
            company=form.company.data,
            role=form.role.data,
            location=form.location.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data,
        )

        db.session.add(exp)
        db.session.commit()

        print("DATA SAVED")

        return redirect(url_for("admin.experience_list"))

    else:
        print(form.errors)

    return render_template("admin/experience_form.html", form=form)


@admin_bp.route("/experience/<int:id>/delete", methods=["POST"])
@login_required
def experience_delete(id):

    exp = Experience.query.get_or_404(id)

    db.session.delete(exp)
    db.session.commit()

    flash("Experience deleted", "danger")

    return redirect(url_for("admin.experience_list"))


@admin_bp.route("/experience/<int:id>/edit", methods=["GET", "POST"])
@login_required
def experience_edit(id):

    experience = Experience.query.get_or_404(id)
    form = ExperienceForm()

    if form.validate_on_submit():

        experience.company = form.company.data
        experience.role = form.role.data
        experience.location = form.location.data
        experience.start_date = form.start_date.data
        experience.end_date = form.end_date.data
        experience.description = form.description.data

        db.session.commit()

        flash("Experience updated successfully")
        return redirect(url_for("admin.experience_list"))

    # PRELOAD DATA
    if request.method == "GET":

        form.company.data = experience.company
        form.role.data = experience.role
        form.location.data = experience.location

        form.start_date.data = datetime.strptime(
            experience.start_date, "%Y-%m-%d"
        ).date()

        if experience.end_date:
            form.end_date.data = datetime.strptime(
                experience.end_date, "%Y-%m-%d"
            ).date()

        form.description.data = experience.description

    return render_template("admin/experience_form.html", form=form, edit=True)


# =========================
# CERTIFICATIONS
# =========================


@admin_bp.route("/certifications")
@login_required
def certification_list():

    certifications = Certification.query.all()

    return render_template(
        "admin/certification_list.html", certifications=certifications
    )


@admin_bp.route("/certifications/new", methods=["GET", "POST"])
@login_required
def certification_create():

    form = CertificationForm()

    if form.validate_on_submit():

        cert = Certification(
            user_id=current_user.id,
            title=form.title.data,
            organization=form.organization.data,
            issue_date=form.issue_date.data,
            credential_url=form.credential_url.data,
        )

        db.session.add(cert)
        db.session.commit()

        flash("Certification added successfully", "success")

        return redirect(url_for("admin.certification_list"))

    return render_template("admin/certification_form.html", form=form)

@admin_bp.route("/certifications/<int:id>/edit", methods=["GET", "POST"])
@login_required
def certification_edit(id):

    cert = Certification.query.get_or_404(id)

    form = CertificationForm(obj=cert)

    if form.validate_on_submit():

        cert.title = form.title.data
        cert.organization = form.organization.data
        cert.issue_date = form.issue_date.data
        cert.credential_url = form.credential_url.data

        db.session.commit()

        flash("Certification updated successfully", "success")

        return redirect(url_for("admin.certification_list"))

    return render_template(
        "admin/certification_form.html",
        form=form,
        edit=True
    )

@admin_bp.route("/certifications/<int:id>/delete", methods=["POST"])
@login_required
def certification_delete(id):

    cert = Certification.query.get_or_404(id)

    db.session.delete(cert)
    db.session.commit()

    flash("Certification deleted", "danger")

    return redirect(url_for("admin.certification_list"))

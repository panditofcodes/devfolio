from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    DateField,
    SelectField,
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    SelectMultipleField,
    TextAreaField,
    FileField,
)
from wtforms.validators import DataRequired, Optional, Email, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf.file import FileAllowed


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SkillForm(FlaskForm):
    name = StringField("Skill Name", validators=[DataRequired()])
    category = StringField("Category", validators=[Optional()])
    level = SelectField(
        "Level",
        choices=[
            (1, "Beginner"),
            (2, "Basic"),
            (3, "Intermediate"),
            (4, "Advanced"),
            (5, "Expert"),
        ],
        coerce=int,
    )
    icon_class = StringField("Icon Class", validators=[Optional()])
    submit = SubmitField("Save")


class ProjectForm(FlaskForm):

    name = StringField("Project Name", validators=[DataRequired()])

    description = TextAreaField("Description")

    github_link = StringField("Github Link")

    live_link = StringField("Live Demo")

    featured = BooleanField("Featured")

    skills = SelectMultipleField("Skills", coerce=int)

    submit = SubmitField("Save")


class ProfileForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])

    mobile = StringField("Mobile")
    headline = StringField("Headline")

    introduction = TextAreaField("Introduction")

    location = StringField("Location")

    profile_photo = FileField("Profile Photo")

    submit = SubmitField("Save")


class EducationForm(FlaskForm):
    degree = StringField("Degree", validators=[DataRequired()])
    institution = StringField("Institution", validators=[DataRequired()])
    start_year = StringField("Start Year")
    end_year = StringField("End Year")
    description = TextAreaField("Description")

    submit = SubmitField("Save")


class SocialLinkForm(FlaskForm):
    platform = StringField("Platform", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired()])
    icon_class = StringField("Icon Class")

    submit = SubmitField("Save")


from wtforms import DateField
from wtforms.validators import Optional


class ExperienceForm(FlaskForm):

    company = StringField("Company", validators=[DataRequired()])
    role = StringField("Role", validators=[DataRequired()])
    location = StringField("Location")

    start_date = DateField(
        "Start Date",
        format="%Y-%m-%d",
        render_kw={"type": "date", "class": "form-control"},
    )

    end_date = DateField(
        "End Date",
        format="%Y-%m-%d",
        validators=[Optional()],  # 👈 THIS FIX
        render_kw={"type": "date", "class": "form-control"},
    )

    description = TextAreaField("Description")

    submit = SubmitField("Save Experience")


class CertificationForm(FlaskForm):

    title = StringField("Certification Title", validators=[DataRequired()])

    organization = StringField("Organization")

    issue_date = DateField("Issue Date", format="%Y-%m-%d")

    credential_url = StringField("Credential URL")

    submit = SubmitField("Save")

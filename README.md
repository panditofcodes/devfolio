# DevFolio

DevFolio is a backend API service for powering a developer portfolio.
It provides structured APIs to fetch portfolio information such as projects, skills, experience, education, certifications, and social links.

This project is designed to serve as the backend for a dynamic developer portfolio website.

---

## Features

* Portfolio API endpoint
* Projects management
* Skills management
* Experience records
* Education records
* Certifications
* Social links
* Structured API responses
* Versioned API endpoints

---

## Tech Stack

* Python
* Flask
* SQLAlchemy
* Flask-Migrate
* REST API architecture

---

## Project Structure

```
devfolio/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── skill.py
│   │   ├── education.py
│   │   ├── experience.py
│   │   ├── certification.py
│   │   └── social_link.py
│   │
│   └── __init__.py
│
├── migrations/
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

## API Example

Fetch portfolio data for a user:

```
GET /api/v1/u/<username>
```

Example:

```
GET /api/v1/u/piyush
```

Response:

```
{
  "user": {},
  "skills": [],
  "projects": [],
  "experience": [],
  "education": [],
  "certifications": [],
  "social_links": []
}
```

---

## Installation

Clone the repository:

```
git clone https://github.com/panditofcodes/devfolio.git
cd devfolio
```

Create virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Create environment file:

```
cp .env.example .env
```

Run migrations:

```
flask db upgrade
```

Start server:

```
flask run
```

---

## Environment Variables

Example `.env` file:

```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///devfolio.db
FLASK_ENV=development
```

---

## Versioning

The project follows semantic versioning.

Example releases:

```
v1.0 – Initial API
v1.1 – API improvements
v2.0 – CMS support
```

---

## Git Workflow

Branches used in the project:

```
main      → stable production code
develop   → active development
feature/* → new features
```

Workflow:

```
feature → develop → main → release tag
```

---

## License

This project is licensed under the MIT License.

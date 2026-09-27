<!--
  TechBlog — Flask Blog Project with Admin Panel
  Author   : ZERO (Sobhan) — https://github.com/zeroux-dev — https://zeroux-dev.github.io
  Telegram : @fesqhli  (https://t.me/fesqhli)
  License  : MIT — keep this notice when you use or copy this code
-->

<h1 align="center">TechBlog — Flask Blog Project with Admin Panel</h1>
<h3 align="center">Python · Flask · PostgreSQL · SQLAlchemy · Bootstrap 5 · RTL / Persian</h3>

<p align="center">
  Built by <a href="https://zeroux-dev.github.io"><b>ZERO (Sobhan)</b></a> —
  a complete, production-style <b>Flask blog</b> with user accounts, image uploads, likes, comments,
  comment reports, search, categories, dark mode and a full <b>admin dashboard</b>.
</p>

<p align="center">
  <a href="https://zeroux-dev.github.io/flask-tech-blog/"><img src="https://img.shields.io/badge/🚀_Live_Demo-open-6D5DFC?style=for-the-badge" alt="Live demo" /></a>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/Bootstrap_5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" alt="MIT" />
</p>

<p align="center">
  <a href="https://zeroux-dev.github.io/flask-tech-blog/">
    <img src="./demo/covers/flask.jpg" alt="TechBlog Flask blog project by ZERO (Sobhan)" width="85%" />
  </a>
</p>

---

## 📑 Table of Contents

- [Live Demo](#-live-demo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Requirements](#-requirements)
- [Installation (step by step)](#-installation-step-by-step)
- [Configuration](#-configuration)
- [Running the Project](#-running-the-project)
- [Routes / Pages](#-routes--pages)
- [Database Models](#-database-models)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [توضیحات کامل فارسی](#-توضیحات-کامل-فارسی)
- [Author](#-author)
- [License](#-license)

---

## 🚀 Live Demo

👉 **[zeroux-dev.github.io/flask-tech-blog](https://zeroux-dev.github.io/flask-tech-blog/)**

The demo is a static preview rendered from the real Jinja templates with sample data
(so you can click through the home page, posts and the admin panel). Forms are disabled in the demo —
run the project locally to use every feature.

| Page | Demo link |
|---|---|
| Home | [index.html](https://zeroux-dev.github.io/flask-tech-blog/index.html) |
| Post + comments | [read-1.html](https://zeroux-dev.github.io/flask-tech-blog/read-1.html) |
| Admin dashboard | [admin-dashboard.html](https://zeroux-dev.github.io/flask-tech-blog/admin-dashboard.html) |
| User management | [admin-users.html](https://zeroux-dev.github.io/flask-tech-blog/admin-users.html) |
| Categories | [admin-categories.html](https://zeroux-dev.github.io/flask-tech-blog/admin-categories.html) |
| Login / Register | [login.html](https://zeroux-dev.github.io/flask-tech-blog/login.html) · [register.html](https://zeroux-dev.github.io/flask-tech-blog/register.html) |

---

## ✨ Features

**Readers**
- Modern RTL (Persian) layout with a hero section and post cards
- Full-text search in titles and content, category filter
- Reading-time estimate and view counter on every post
- Like posts and comments, dark / light theme (saved in the browser)

**Writers**
- Sign up with username, email, phone, gender and profile picture
- Create, edit and delete posts with a cover image and category
- Comment on posts, delete your own comments, report abusive comments

**Admin (`/admin/dashboard`)**
- Live stats: users, posts, comments, total views, reports, categories + Chart.js chart
- User list and user detail page, one-click **random temporary password**
- Rename or merge categories, moderate reported comments
- Admin can edit / delete any post or comment

**Security**
- Passwords hashed with **scrypt** (Werkzeug)
- Secret key and database URL read from environment variables
- Image-only uploads (png, jpg, jpeg, gif, webp) with a 5 MB limit and safe file names
- Database initialised with a CLI command — no public "reset" URL

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Web framework | Flask 3, Jinja2 |
| Auth | Flask-Login, Werkzeug scrypt hashing |
| ORM / DB | Flask-SQLAlchemy, **PostgreSQL** (psycopg2) — or SQLite for quick local runs |
| Frontend | Bootstrap 5, Font Awesome, Bootstrap Icons, Chart.js, Vazirmatn font, custom CSS |

---

## 📋 Requirements

- **Python 3.10 or newer** — check with `python --version`
- **pip** and **venv** (included with Python)
- **PostgreSQL 13+** *(optional — without it the app uses a local SQLite file)*
- Git *(optional, to clone the repo)*

---

## ⚙ Installation (step by step)

### 1. Get the code

```bash
git clone https://github.com/zeroux-dev/flask-tech-blog.git
cd flask-tech-blog
```

Or click **Code → Download ZIP** on GitHub and extract it.

### 2. Create and activate a virtual environment

```bash
# Windows (PowerShell / CMD)
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Create a PostgreSQL database

```sql
-- in psql or pgAdmin
CREATE DATABASE tech_blog;
CREATE USER blog_user WITH PASSWORD 'strong-password';
GRANT ALL PRIVILEGES ON DATABASE tech_blog TO blog_user;
```

Skip this step to use SQLite (a `tech_blog.db` file is created automatically).

---

## 🔧 Configuration

All settings come from environment variables (see [`.env.example`](.env.example)):

| Variable | Required | Example | Description |
|---|---|---|---|
| `SECRET_KEY` | ✅ | `a-long-random-string` | Signs sessions and cookies |
| `DATABASE_URL` | ➖ | `postgresql://blog_user:strong-password@localhost:5432/tech_blog` | Default: local SQLite file |
| `ADMIN_PASSWORD` | ➖ | `choose-a-strong-one` | Used by `init-db`; if missing you are prompted |
| `FLASK_DEBUG` | ➖ | `1` | Debug mode for development only |

```bash
# Windows (PowerShell)
$env:SECRET_KEY="change-me"
$env:DATABASE_URL="postgresql://blog_user:strong-password@localhost:5432/tech_blog"

# macOS / Linux
export SECRET_KEY=change-me
export DATABASE_URL=postgresql://blog_user:strong-password@localhost:5432/tech_blog
```

---

## ▶ Running the Project

```bash
# 1) create the tables and the "admin" account (asks for a password)
flask --app app init-db

# 2) start the development server
flask --app app run
```

Open **http://127.0.0.1:5000** → register a normal user, or log in as **admin** with the password you chose
and open **http://127.0.0.1:5000/admin/dashboard**.

> You can also run `python app.py` — it starts on port **5009**.

---

## 🧭 Routes / Pages

| Method | URL | Description | Access |
|---|---|---|---|
| GET | `/` | Home: latest posts, `?q=` search, `?category=` filter | Everyone |
| GET/POST | `/read/<id>` | Post page + comments | Everyone (comment: logged in) |
| GET/POST | `/register` | Sign up | Guests |
| GET/POST | `/login` · GET `/logout` | Sign in / out | — |
| GET/POST | `/post/new` | Write a post | Logged in |
| GET/POST | `/post/<id>/update` | Edit a post | Author / admin |
| POST | `/post/<id>/delete` | Delete a post | Author / admin |
| GET | `/post/<id>/like` · `/comment/<id>/like` | Like / unlike | Logged in |
| POST | `/comment/<id>/delete` · `/comment/<id>/report` | Delete / report comment | Logged in |
| GET | `/admin/dashboard` · `/admin/users` · `/admin/user/<id>` | Admin panel | Admin |
| POST | `/admin/user/<id>/reset_pass` | Generate a temporary password | Admin |
| GET/POST | `/admin/categories` · `/admin/category/rename` · `/admin/category/delete` | Manage categories | Admin |

---

## 🗄 Database Models

| Model | Main fields |
|---|---|
| `User` | username, password (hash), email, phone, gender, profile_pic, join_date, last_login |
| `Post` | title, content, category, image_file, views, date_posted, author |
| `Comment` | body, date_posted, author, post |
| `PostLike` / `CommentLike` | user ↔ post / comment |
| `CommentReport` | reason, reporter, comment, date_reported |

---

## 📂 Project Structure

```
flask-tech-blog/
├── app.py               # routes, auth, admin panel, CLI command (init-db)
├── models.py            # SQLAlchemy models
├── config.py            # settings from environment variables
├── requirements.txt
├── .env.example         # sample configuration
├── templates/           # Jinja2 templates (blog + admin)
├── static/
│   ├── style.css        # custom RTL / dark-mode styles
│   └── uploads/         # user uploads (git-ignored)
├── demo/
│   ├── build_demo.py    # builds the static live demo
│   └── covers/          # demo images
├── .github/workflows/   # CI: builds & deploys the live demo
└── docs/                # generated demo (built by CI, not committed)
```

---

## 🔍 How It Works

- **Authentication** — Flask-Login keeps the session; passwords are stored as scrypt hashes.
- **Posts** — cover images are validated, renamed with a timestamp and saved in `static/uploads/`.
- **Views & reading time** — every GET on a post increases `views`; reading time = words ÷ 200.
- **Likes** — toggled per user (like / unlike) for posts and comments.
- **Reports** — users report comments with a reason; the admin sees them on the dashboard and can delete the comment or dismiss the report.
- **Admin** — the account named `admin` gets the dashboard, user management and category tools.
- **Live demo** — `python demo/build_demo.py` renders the real templates with sample data into `docs/`.

---

## ☁ Deployment

```bash
pip install gunicorn
gunicorn -w 3 -b 0.0.0.0:8000 app:app
```

Put Nginx (or Cloudflare) in front, set `SECRET_KEY` and `DATABASE_URL` on the server, run
`flask --app app init-db` once, and keep `FLASK_DEBUG` off. Works on any VPS, Render, Railway or Liara.

---

## 🩺 Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: flask_sqlalchemy` | Activate the venv, then `pip install -r requirements.txt` |
| `psycopg2` fails to install | Use Python 3.10–3.12, or remove `DATABASE_URL` to run on SQLite |
| `could not connect to server` | Start PostgreSQL and check user / password / database in `DATABASE_URL` |
| `no such table` | Run `flask --app app init-db` |
| Can't open `/admin/dashboard` | Log in with the **admin** account created by `init-db` |
| Upload ignored | Only png / jpg / jpeg / gif / webp up to 5 MB are accepted |

---

## 🇮🇷 توضیحات کامل فارسی

**تک‌بلاگ** یک **پروژه وبلاگ کامل با پایتون فلسک (Flask)** و پایگاه داده **PostgreSQL** است که توسط
**ZERO (سبحان)** طراحی و توسعه داده شده است.

**امکانات:** ثبت‌نام و ورود کاربران با عکس پروفایل، نوشتن و ویرایش پست با تصویر و دسته‌بندی، لایک پست و کامنت،
گزارش تخلف کامنت، جستجو، زمان مطالعه و شمارش بازدید، حالت تاریک و روشن، و **پنل مدیریت** کامل با آمار، نمودار،
مدیریت کاربران، ساخت رمز موقت و مدیریت دسته‌بندی‌ها.

**نصب و اجرا:**

1. پایتون ۳.۱۰ یا بالاتر را نصب کنید.
2. پروژه را دانلود کنید و در پوشه‌ی آن یک محیط مجازی بسازید: `python -m venv venv` و بعد `venv\Scripts\activate`
3. کتابخانه‌ها را نصب کنید: `pip install -r requirements.txt`
4. (اختیاری) در PostgreSQL دیتابیس `tech_blog` را بسازید و آدرس آن را در `DATABASE_URL` قرار دهید؛ بدون آن پروژه با SQLite اجرا می‌شود.
5. یک `SECRET_KEY` تنظیم کنید.
6. جداول و کاربر ادمین را بسازید: `flask --app app init-db`
7. اجرا: `flask --app app run` و باز کردن آدرس `http://127.0.0.1:5000`

🔗 **دموی زنده:** [zeroux-dev.github.io/flask-tech-blog](https://zeroux-dev.github.io/flask-tech-blog/) ·
🌐 **سایت شخصی:** [zeroux-dev.github.io](https://zeroux-dev.github.io) ·
💬 **تلگرام:** [@fesqhli](https://t.me/fesqhli)

---

## 👤 Author

**ZERO (Sobhan)** — UI/UX Designer · Web Developer · WordPress · SEO · Unity · Telegram Bots

<p>
  <a href="https://zeroux-dev.github.io"><img src="https://img.shields.io/badge/Website-zeroux--dev.github.io-6D5DFC?style=for-the-badge" alt="Website" /></a>
  <a href="https://github.com/zeroux-dev"><img src="https://img.shields.io/badge/GitHub-zeroux--dev-181717?style=for-the-badge&logo=github" alt="GitHub" /></a>
  <a href="https://t.me/fesqhli"><img src="https://img.shields.io/badge/Telegram-@fesqhli-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" /></a>
</p>

Need a website, Flask app, WordPress store or Telegram bot? Message me on Telegram.
⭐ If this project helped you, please give it a star.

## 📄 License

[MIT](LICENSE) © 2025-2026 **ZERO (Sobhan)** — you may use and modify this code, but you **must keep the
copyright notice and credit the author**.

# ============================================================
#  TechBlog — Flask Blog & Admin Panel
#  Author   : ZERO (Sobhan) — https://github.com/zeroux-dev
#  Telegram : @fesqhli  (https://t.me/fesqhli)
#  License  : MIT — keep this notice when you use or copy this code
#  Copyright (c) 2025-2026 ZERO (Sobhan)
# ============================================================
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database: set DATABASE_URL for PostgreSQL, e.g.
#   postgresql://USER:PASSWORD@localhost:5432/tech_blog
# If not set, a local SQLite file is used (great for quick demos).
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'tech_blog.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Never commit a real secret key — set SECRET_KEY in your environment.
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-change-me')

# Uploads
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

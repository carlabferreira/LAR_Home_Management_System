"""Extensões do Flask criadas sem o app (evita importações circulares)."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

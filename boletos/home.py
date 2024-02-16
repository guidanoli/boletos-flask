from flask import Blueprint, request, redirect, url_for, flash, render_template

from boletos.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    db = get_db()
    services = db.execute('SELECT * FROM service ORDER BY name').fetchall()
    return render_template('home.html', services=services)

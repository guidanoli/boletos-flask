from datetime import datetime

from flask import Blueprint, render_template, request, redirect, session, url_for

from app.db import get_services

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    services = get_services()
    kwargs = {}
    kwargs['services'] = services
    kwargs['show_inactive'] = session.get('show_inactive')
    return render_template('index.html', **kwargs)


@bp.route('/inactive/show')
def show_inactive():
    session['show_inactive'] = True
    return redirect(url_for('index'))


@bp.route('/inactive/hide')
def hide_inactive():
    session.pop('show_inactive', None)
    return redirect(url_for('index'))

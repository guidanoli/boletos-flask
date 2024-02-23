import calendar
from datetime import datetime

from flask import Blueprint, render_template, request

from app.db import get_services

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    services = get_services()
    kwargs = {}
    kwargs['services'] = services
    return render_template('index.html', **kwargs)

import calendar
from datetime import datetime

from flask import Blueprint, render_template

from app.db import get_services

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    services = get_services()
    kwargs = {}
    kwargs['services'] = services
    kwargs['month_name'] = calendar.month_name
    kwargs['now'] = datetime.now()
    return render_template('home.html', **kwargs)

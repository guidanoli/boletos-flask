from datetime import datetime

from flask import Blueprint, request, redirect, url_for, flash, render_template

from boletos.db import get_services

bp = Blueprint('home', __name__)


def plural(n):
    if n == 1:
        return n, ''
    else:
        return n, 's'

@bp.route('/')
def index():
    services = get_services()

    kwargs = {}
    kwargs['services'] = services
    return render_template('home.html', **kwargs)

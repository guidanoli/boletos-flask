from datetime import datetime

from flask import Blueprint, request, redirect, url_for, flash, render_template

from boletos.db import get_services

bp = Blueprint('home', __name__)


def plural(n):
    if n == 1:
        return n, ''
    else:
        return n, 's'


def fmtdelta(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    if days > 0:
        return '{} dia{}'.format(*plural(days))
    else:
        if hours > 0:
            return '{} hora{}'.format(*plural(hours))
        else:
            if minutes > 0:
                return '{} minuto{}'.format(*plural(minutes))
            else:
                return '{} segundo{}'.format(*plural(seconds))

@bp.route('/')
def index():
    services = get_services()

    kwargs = {}
    kwargs['services'] = services
    kwargs['curr_ts'] = datetime.now().timestamp()
    kwargs['fmtdelta'] = fmtdelta
    return render_template('home.html', **kwargs)

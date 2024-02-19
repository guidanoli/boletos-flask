from datetime import datetime

from flask import Blueprint, request, redirect, url_for, flash, render_template

from boletos.db import get_services
import boletos.utils as u

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    services = get_services()

    kwargs = {}
    kwargs['services'] = services
    kwargs['u'] = u
    return render_template('home.html', **kwargs)

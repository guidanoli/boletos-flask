from flask import Blueprint, render_template

from app.db import get_service

bp = Blueprint('payment', __name__)


@bp.route('/<int:service_id>/payment/new')
def new(service_id):
    service = get_service(service_id)
    kwargs = {}
    kwargs['service'] = service
    return render_template('service/payment/new.html', **kwargs)

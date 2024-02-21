from flask import Blueprint, render_template

bp = Blueprint('payment', __name__)


@bp.route('/<int:service_id>/payment/new')
def new():
    return render_template('service/payment/new.html')

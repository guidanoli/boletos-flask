from datetime import date
import math

from flask import Blueprint, render_template, request, redirect, session, url_for

from app.db import get_services, get_last_payments_for
from app.time import estimate_next_payment_date

bp = Blueprint('index', __name__)


def days_until_estimated_payment_date(service, today):
    service_id = service['service_id']
    last_payments = get_last_payments_for(service_id)
    estimated_payment_date = estimate_next_payment_date(service, last_payments)
    if estimated_payment_date:
        delta = estimated_payment_date - today
        return delta.days


def unpaid_service_key(unpaid_service):
    if unpaid_service['days'] is not None:
        return (unpaid_service['days'], unpaid_service['service']['name'])
    else:
        return (-math.inf, unpaid_service['service']['name'])


def format_unpaid_service_message(unpaid_service):
    days = unpaid_service['days']
    if days is not None:
        if days > 0:
            if days == 1:
                return 'tomorrow'
            else:
                return f'in {days} days'
        elif days < 0:
            if days == -1:
                return 'yesterday'
            else:
                return f'{-days} days ago'
        else:
            return 'today'


def is_message_urgent(unpaid_service):
    days = unpaid_service['days']
    if days is not None:
        return days <= 0
    else:
        return False


def format_unpaid_service(unpaid_service):
    return {
        'service': unpaid_service['service'],
        'message': format_unpaid_service_message(unpaid_service),
        'is_message_urgent': is_message_urgent(unpaid_service),
    }


@bp.route('/')
def index():
    unpaid_services = []
    paid_services = []
    inactive_services = []
    today = date.today()

    for service in get_services():
        if not service['active']:
            inactive_services.append(service)
        elif not service['paid']:
            days = days_until_estimated_payment_date(service, today)
            unpaid_services.append({
                'service': service,
                'days': days,
            })
        else:
            paid_services.append(service)

    unpaid_services = sorted(unpaid_services, key=unpaid_service_key)
    unpaid_services = list(map(format_unpaid_service, unpaid_services))

    kwargs = {}
    kwargs['unpaid_services'] = unpaid_services
    kwargs['paid_services'] = paid_services
    kwargs['inactive_services'] = inactive_services
    return render_template('index.html', **kwargs)

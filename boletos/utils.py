from datetime import datetime
from dateutil.relativedelta import relativedelta


def fmtdate(ts):
    return datetime.fromtimestamp(ts).strftime('%d/%m/%Y')


def fmttime(ts):
    return datetime.fromtimestamp(ts).strftime('%Hh%M')


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


def fmtamount(a):
    return 'R$ {:.2f}'.format(a)


def get_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()


def get_delta(frequency):
    if frequency == 'monthly':
        return relativedelta(months=1)
    elif frequency == 'yearly':
        return relativedelta(years=1)
    else:
        raise ValueError('unknown frequency')


def next_expiry_ts_estimation(max_paid_expiry_ts, frequency):
    date = datetime.fromtimestamp(max_paid_expiry_ts)
    delta = get_delta(frequency)
    return (date + delta).timestamp()

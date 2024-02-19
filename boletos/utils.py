from datetime import datetime


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

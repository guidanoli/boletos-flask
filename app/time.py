from datetime import date, timedelta


def to_date(payment):
    if payment['day']:
        return date(payment['year'], payment['month'], payment['day'])


def start_of_year(d):
    return d.replace(month=1, day=1)


def start_of_following_year(d):
    return date(d.year + 1, 1, 1)


def time_since_start_of_year(d):
    return d - start_of_year(d)


def start_of_month(d):
    return d.replace(day=1)


def start_of_following_month(d):
    if d.month == 12:
        return start_of_following_year(d)
    else:
        return date(d.year, d.month + 1, 1)


def time_since_start_of_month(d):
    return d - start_of_month(d)


def is_not_none(o):
    return o is not None


def estimate_next_payment_date(service, last_payments):
    if not last_payments:
        return None
    else:
        last_payment_dates = list(filter(is_not_none, map(to_date, last_payments)))
        if not last_payment_dates:
            return None

        last_payment_date = max(last_payment_dates)
        match service['frequency']:
            case 'y':
                deltas = list(map(time_since_start_of_year, last_payment_dates))
                avg_delta = sum(deltas, timedelta(0)) / len(deltas)
                return start_of_following_year(last_payment_date) + avg_delta
            case 'm':
                deltas = list(map(time_since_start_of_month, last_payment_dates))
                avg_delta = sum(deltas, timedelta(0)) / len(deltas)
                return start_of_following_month(last_payment_date) + avg_delta
            case _:
                raise ValueError('unknown frequency')

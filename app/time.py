def get_next_payment(service, last_payment):
    if not last_payment:
        return None
    else:
        frequency = service['frequency']
        year = last_payment['year']
        month = last_payment['month']
        if frequency == 'y':
            return {
                'year': year + 1,
                'month': month,
            }
        elif frequency == 'm':
            return {
                'year': year + month // 12,
                'month': 1 + month % 12,
            }
        else:
            raise ValueError('unknown frequency')

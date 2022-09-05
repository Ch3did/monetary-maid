import arrow


def is_name_valid(name):
    if str(name):
        return True
    return False


def is_amount_valid(amount):
    if amount.isnumeric():
        return amount
    return False


def is_date_valid(start_date, end_date):
    try:
        start_date = arrow.get(start_date).format("YYYY-MM-DD")
        end_date = arrow.get(end_date).format("YYYY-MM-DD")
    except Exception as e:
        return False
    finally:
        if start_date < end_date:
            return [start_date, end_date]
        return False


def is_payment_day_valid(payment_day):
    if payment_day.isnumeric() and int(payment_day) <= 31:
        return payment_day
    return False


# TODO: add an error msg for every validator

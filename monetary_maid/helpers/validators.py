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


class ATMValidatorException(Exception):
    def __init__(
        self,
        message=None,
        establishment=None,
        details=None,
        geolocation=None,
        can_retry=True,
        retries=0,
    ):
        self.message = message
        self.establishment = establishment
        self.details = details
        self.geolocation = geolocation
        self.can_retry = can_retry
        if retries >= 1:
            self.can_retry = False

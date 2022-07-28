"""File criado para guardar código legado
"""
import arrow

Wallet = "sla"


def _validate_date(self):
    """Validava se já existia alguma wallet para o mês

    Returns:
        _type_: _description_
    """
    if last_date := self.conn.query(Wallet.date).order_by(Wallet.date.desc()).first():
        if arrow.get(last_date[0]).strftime("%m-%Y") == arrow.now().strftime("%m-%Y"):
            return False
    return True

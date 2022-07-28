import arrow
import click

from monetary_maid.view import MonetaryView

# TODO: Toda vez que descomento o import da classe da view o click começa a
# apresentar comportamentos estranhos... Será que é pelo click ser escrito em funcional?
# Validar isso.


# Groups
@click.group("get", help="Monetary Get: Get some info in the wallet")
def mget():
    ...


@click.group("put", help="Monetary Put: Put some info in wallet")
def mput():
    ...


@mget.command("debit", help="Get debits info")
def get_debits():
    # mv = MonetaryView()
    click.echo("debits")


@mget.command("wallet", help="Get wallet info")
@click.option("--period", "-p", help="Get info for a period", type=click.DateTime())
def get_wallet(period):
    # mv = MonetaryView()
    if not period:
        period = arrow.now()
    click.echo(period)

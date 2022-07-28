import arrow
import click

from monetary_maid.view import MonetaryView

mv = MonetaryView()

# Groups
@click.group("mget", help="Monetary Get: Get some info in the wallet")
def mget():
    ...


@click.group("mput", help="Monetary Put: Put some info in wallet")
def mput():
    ...


@mget.command("debit", help="Get debits info")
def get_debits():
    click.echo("debits")


@mget.command("wallet", help="Get wallet info")
@click.option("--period", "-p", help="Get info for a period", type=click.DateTime())
def get_wallet(period):
    click.echo(period.strftime("%m-%Y"))
    if not period:
        period = arrow.now().format("MM-YYYY")

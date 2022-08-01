import arrow
import click

from monetary_maid.view import (
    get_debits_info,
    get_wallet_info,
    register_debit,
    register_month_salary,
)

# Groups
# @click.group("config", help="Configure your wallet")
# def config():
#     ...


@click.group("get", help="Monetary Get: Get some info in the wallet")
def mget():
    ...


@click.group("put", help="Monetary Put: Put some info in wallet")
def mput():
    ...


@mget.command("debit", help="Get debits info")
def get_debits():
    get_debits_info()


@mget.command("wallet", help="Get wallet info")
@click.option("--period", "-p", help="Get info for a period", type=click.DateTime())
def get_wallet(period):
    if not period:
        period = arrow.now()
    get_wallet_info()


@mput.command("wallet", help="Register your new wallet")
def put_wallet():
    register_month_salary()


@mput.command("debit", help="Register a new debit")
def put_debit():
    register_debit()

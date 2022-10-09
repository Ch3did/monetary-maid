import arrow
import click

from src.views.atm import (
    get_establishment,
    update_establishment,
    update_nubank_statment,
)
from src.views.config import migrate

# from src.views.wallet import (
#     get_debits_info,
#     get_wallet_info,
#     register_debit,
#     register_month_salary,
# )


# Get data
@click.group("get", help="Monetary Get: Get some info in the wallet")
def mget():
    ...


# Input data
@click.group("put", help="Monetary Put: Put some info in wallet")
def mput():
    ...


# Update data
@click.group("up", help="Monetary Update: Update some info on wallet")
def mup():
    ...


# Configuration
@click.group("confg", help="Monetary Update: Update some info on wallet")
def mconf():
    ...


# GET


@mget.command("debit", help="Get debits info")
def get_debits():
    # get_debits_info()
    pass


@mget.command("wallet", help="Get wallet info")
@click.option("--period", "-p", help="Get info for a period", type=click.DateTime())
def get_wallet(period):
    # get_wallet_info(period)
    pass


# TODO: ajustar lógica para busca de dados e busca de estabelecimentos
# @mget.command("atm", help="Get wallet info")
# @click.option("--name", "-n", required=True)
# @click.option("--default", "-d",  is_flag=True)
# @click.option("--period", "-p", help="Get info for a period", default=arrow.now())
# def get_wallet(name, period, default):
#     # if
#     get_establishment(name, period, default)


# PUT


@mput.command("wallet", help="Register your new wallet")
def put_wallet():
    # register_month_salary()
    pass


@mput.command("debit", help="Register a new debit")
def put_debit():
    # register_debit()
    pass


# UPDATE


@mup.command("nubank", help="Update Nubank Statment")
def update_nu():
    update_nubank_statment()


@mup.command("stab", help="Update Establishment Details and Location")
def update_estab():
    update_establishment()


# CONFIGURATION


@mconf.command("migrate", help="Run migrations")
def run_migrations():
    migrate()

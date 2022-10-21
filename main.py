import arrow
import click

from src.views.categories import create_category_view
from src.views.config import run_migrate_view
from src.views.establishment import (
    get_establishment_info_view,
    get_establishment_spend_view,
    update_establishment_view,
)
from src.views.statment import update_nubank_statment_view

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


@mget.command("estab", help="Get establishment info")
@click.argument("name")
def get_establishment_info(name):
    get_establishment_info_view(str(name))


@mget.command("spend", help="Get wallet info")
@click.argument("name")
@click.option(
    "--period",
    "-p",
    help="Get info for a period",
    default=str(arrow.now().format(f"YYYY-MM-01")),
)
def get_establishment_spend(name, period):
    period = arrow.get(period).format(f"YYYY-MM-DD")
    get_establishment_spend_view(name, period)


# PUT


@mput.command("category", help="Register a new Category")
def create_category():
    create_category_view()

    # @mput.command("debit", help="Register a new debit")
    # def put_debit():
    #     # register_debit()
    pass


# UPDATE


@mup.command("nubank", help="Update Nubank Statment")
def update_nubank_statment():
    update_nubank_statment_view()


@mup.command("stab", help="Update Establishment Details and Location")
def update_establishment():
    update_establishment_view()


# CONFIGURATION


@mconf.command("migrate", help="Run migrations")
def run_migrations():
    run_migrate_view()

import arrow
import click

from src.views.categories import (
    create_category_view,
    get_categories_list_view,
    get_category_by_id_view,
)
from src.views.config import run_migrate_view
from src.views.debit import (
    get_debit_by_id_view,
    list_debit_from_period_view,
    update_bank_statment_view,
    update_debit_category_view,
)
from src.views.homescreen import make_homescreen


# Get data
@click.group("get", help="Monetary Get: Get some info")
def mget():
    ...


# Input data
@click.group("put", help="Monetary Put: Put some info")
def mput():
    ...


# Update data
@click.group("up", help="Monetary Update: Update some info")
def mup():
    ...


# Configuration
@click.group("confg", help="Monetary Config: Run configurations")
def mconf():
    ...


# @click.group("olar", )
@click.command("home", help="Print the home screen")
@click.option("-t", help="Specifies a type of search from Categories", default=1)
def home(t):
    make_homescreen(t)


#     ___     ___     ___     ___     ___     ___     ___     ___     ___
# GET Debits


@mget.command("dlist", help="Get the debit list")
@click.option(
    "--period",
    "-p",
    help="Get info for a period",
    default=str(arrow.now().format(f"YYYY-MM-01")),
)
def get_debit_list(period):
    list_debit_from_period_view(period)


@mget.command("debit", help="Get an especific debit by ID")
@click.argument("id")
def get_debit_by_id(id):
    get_debit_by_id_view(id)


# GET Category


@mget.command("categories", help="Get categories list")
@click.option("-inv", help="#DESCUBRA", default=False)
def get_category_info(inv):
    get_categories_list_view(inv)


@mget.command("category", help="Get an especific category by ID")
@click.argument("id")
def get_category_info(id):
    get_category_by_id_view(id)


# PUT


@mput.command("category", help="Register a new category")
def create_category():
    create_category_view()


# UPDATE


@mup.command("bank", help="Update Bank's Debits")
def update_nubank_statment():
    update_bank_statment_view()


@mup.command("debit", help="Update an debit's category relation")
@click.argument("id")
def update_debit_category(id):
    update_debit_category_view(id)


# CONFIGURATION


@mconf.command("migrate", help="Run migrations")
def run_migrations():
    run_migrate_view()

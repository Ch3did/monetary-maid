import arrow
import click

from src.views.categories import create_category_view, get_categories_info_view
from src.views.config import run_migrate_view
from src.views.debit import list_debit_from_period_view, update_nubank_statment_view


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


#     ___     ___     ___     ___     ___     ___     ___     ___     ___
# GET


@mget.command("category", help="Get Category info")
@click.option("--name", default=False)
@click.option("--name", "-n", help="Specifies a Category", default="all")
def get_category_info(name):
    get_categories_info_view(str(name))


@mget.command("dlist", help="Get the debit list")
@click.option(
    "--period",
    "-p",
    help="Get info for a period",
    default=str(arrow.now().format(f"YYYY-MM-01")),
)
def get_debit_list(period):
    list_debit_from_period_view(period)


# PUT


@mput.command("category", help="Register a new Category")
def create_category():
    create_category_view()


# UPDATE


@mup.command("nubank", help="Update Nubank Statment")
def update_nubank_statment():
    update_nubank_statment_view()


@mup.command("category", help="Update Category Details and Location")
def update_Category():
    # update_category_view()
    pass


# CONFIGURATION


@mconf.command("migrate", help="Run migrations")
def run_migrations():
    run_migrate_view()

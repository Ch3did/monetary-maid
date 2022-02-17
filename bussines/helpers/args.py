import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-g",
    "--get",
    action="store_true",
    required=False,
    help="Get your last wallet",
)
parser.add_argument(
    "-p",
    "--period",
    type=str,
    nargs="+",
    required=False,
    help="Use for get especific register",
)
parser.add_argument(
    "-r",
    "--register",
    type=int,
    nargs="+",
    required=False,
    help="Register your wallet",
)
parser.add_argument(
    "-d",
    "--debits",
    action="store_true",
    required=False,
    help="Get your debits",
)

def get_args():
    return vars(parser.parse_args())


# TODO: Parsear argumento para busca específica de carteira

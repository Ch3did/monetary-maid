import os


# TODO: Pegar nome da função e tratar pra printar antes de cada execussão do clean output (vide create_category_view)
# TODO: ALTERAR O CLEANOUTPUT PRA LIMPAR E SANATIZAR OS DADOS A SEREM USADOS DENTRO DAS VIEWS
def clean_output(func):
    os.system("clear")

    def decorator(*args):
        func(*args)
        input("Press Enter to continue...")
        os.system("clear")
        return

    return decorator

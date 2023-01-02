import os


def clean_output(func):
    os.system("clear")

    def decorator(*args):
        func(*args)
        input("Press Enter to continue...")
        os.system("clear")
        return

    return decorator

import os


def clean_output(func):
    os.system("clear")

    def decorator():
        func()
        input("Press Enter to continue...")
        os.system("clear")
        return

    return decorator

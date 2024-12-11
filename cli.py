
from src.taskscript import configure_application,main_menu
from src.utils import clear_terminal,has_configured,linebreak


def main():

    clear_terminal()

    linebreak()

    if has_configured():
        main_menu()
    else:
        configure_application()

    

    


if __name__== "__main__":
    main()

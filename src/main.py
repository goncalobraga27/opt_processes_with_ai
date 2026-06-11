from menu import Menu
from business_logic import BusinessLogic

def main():
    m = Menu()
    business_logic = BusinessLogic()

    option = m.print_menu()
    business_logic.choose_execution_flow(int(option))

if __name__ == "__main__":
    main()
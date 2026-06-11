import base64
import os
from pydoc import text
from menu import Menu

class BusinessLogic:
    def __init__(self):
        self.menu = Menu()
        self.path_to_users_data = "../data/users_data.csv"
        os.makedirs(os.path.dirname(self.path_to_users_data), exist_ok=True)
    
    def encrypt(self, text):
        return base64.b64encode(text.encode()).decode()
    
    def decrypt(self, text):
        return base64.b64decode(text.encode()).decode()
    
    def authenticate_user(self, username, password):
        if not os.path.exists(self.path_to_users_data):
            return None

        with open(self.path_to_users_data, "r", encoding="utf-8") as file:
            lines = file.readlines()[1:] 

            for line in lines:
                stored_user, stored_pass = line.strip().split(",")

                dec_user = self.decrypt(stored_user)
                dec_pass = self.decrypt(stored_pass)

                if dec_user == username and dec_pass == password:
                    
                    return True

        return None

    def choose_execution_flow(self, option):
        if option == 1:
            username, password = self.menu.print_open_session()
            if self.authenticate_user(username, password):
                self.menu.print_client_menu()
            else:
                self.menu.print_error_authentication()
    
        elif option == 2:
            username, password = self.menu.print_open_session()
            if self.authenticate_user(username, password):
                self.menu.print_supplier_menu()
            else:
                self.menu.print_error_authentication()

        elif option == 3:
            print("Erro")
        elif option == 4:
            username, password = self.menu.print_create_account()
            enc_username = self.encrypt(username)
            enc_password = self.encrypt(password)
            with open(self.path_to_users_data, "a", encoding="utf-8") as file:
                file.write(f"{enc_username},{enc_password}\n")            
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")
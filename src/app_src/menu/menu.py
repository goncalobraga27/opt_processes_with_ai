
class Menu:
    def print_menu(self):
        print("Seja bem-vindo à otimização de processos com IA!\n" \
        "ATENÇÃO, ISTO É APENAS UMA SIMULAÇÃO, NÃO REPRESENTA UM PRODUTO REAL.\n" \
        "Por favor, selecione uma opção:")
        print("1. Se for cliente, prima 1.")
        print("2. Se for fornecedor, prima 2.")
        print("3. Se for utilizador da ferramente, prima 3.")
        print("4. Se ainda não tem conta, criar conta.")
        option = input("Opção: ")
        return option
    
    def print_client_menu(self):
        print("Menu específico do cliente:")
        print("1. Criar pedido")
        print("2. Ver informações disponíveis sobre o pedido")
        print("3. Sair")
        option = input("Opção: ")
        return option

    def print_supplier_menu(self):
        print("Menu específico do fornecedor:")
        print("1. Criar fatura")
        print("2. Sair")
        option = input("Opção: ")
        return option
    
    def print_user_menu(self):
        print("Menu específico do utilizador da ferramenta:")
        print("1. Ver pedidos criados/atualizados")
        print("2. Ver faturas criadas")
        print("4. Visualizar insights sobre os pedidos")
        print("5. Visualizar insights sobre as faturas")
        print("6. Sair")
        option = input("Opção: ")
        return option

    def print_create_account(self):
        username = input("Insira o nome de utilizador: ")
        password = input("Insira a palavra-passe: ")
        return username,password
    
    def print_open_session(self):
        username = input("Insira o nome de utilizador: ")
        password = input("Insira a palavra-passe: ")
        return username,password
    
    def print_error_authentication(self):
        print("Autenticação mal-sucedida!")

    def print_add_request_menu(self):
        request_name = input("Insira o nome do pedido: ")
        request_description = input("Insira a descrição do pedido: ")
        print(f"Pedido '{request_name}' criado com sucesso!")
        return request_name, request_description
    
    def print_view_request_info_menu(self):
        invoice_date = input("Insira a data da fatura (DD/MM/AAAA): ")
        invoice_reference = input("Insira a referência da fatura: ")
        invoice_category = input("Insira a categoria da fatura: ")
        invoice_payment_method = input("Insira o método de pagamento da fatura: ")
        invoice_amount = input("Insira o valor da fatura: ")
        print(f"Fatura '{invoice_reference}' criada com sucesso!")
        return invoice_date, invoice_reference, invoice_category, invoice_payment_method, invoice_amount

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
    
    def print_manager_menu(self):
        print("1. Ver pedidos criados")
        print("2. Atualizar o estado de um pedido")
        print("3. Ver insights sobre as faturas registadas na plataforma")
        print("4. Sair")
        return input("Opção: ")
    
    def show_request_data(self, request_data_list):
        if not request_data_list:
            print("Sem pedidos.")
            return

        # cabeçalho
        headers = ["Nome", "Descrição", "Cliente", "Estado"]

        # largura das colunas
        col_widths = [20, 30, 15, 15]

        def format_row(row):
            return (
                f"{row[0][:20]:<20} "
                f"{row[1][:30]:<30} "
                f"{row[2][:15]:<15} "
                f"{row[3]:<15}"
            )

        print("\n" + "-" * 85)
        print(f"{headers[0]:<20} {headers[1]:<30} {headers[2]:<15} {headers[3]:<15}")
        print("-" * 85)

        for req in request_data_list:
            print(format_row([
                req.get("nome", ""),
                req.get("descricao", ""),
                req.get("cliente", ""),
                req.get("estado", "PENDENTE")
            ]))

        print("-" * 85)
    
    def show_requests_for_update(self, request_data):
        if not request_data:
            print("Não existem pedidos.")
            return None, None

        print("\n===== PEDIDOS =====\n")

        for i, req in enumerate(request_data, start=1):
            print(f"{i}. {req['nome']} | {req['cliente']} | {req.get('estado', 'PENDENTE')}")

        print("\n0. Cancelar")

        try:
            choice = int(input("\nEscolhe o pedido a atualizar: "))

            if choice == 0:
                return None, None

            if choice < 1 or choice > len(request_data):
                print("Opção inválida.")
                return None, None

            new_state = input("Novo estado do pedido: ").strip()

            return choice - 1, new_state

        except ValueError:
            print("Input inválido.")
            return None, None
        
    def print_request_evolution_for_user(self,history):
        if not history:
            print("Não existem evoluções.")

        print("\n===== ATUALIZAÇÕES =====\n")

        for i, req in enumerate(history, start=1):
            print(f"{i}. {req['data']} | {req['nome']} | {req['descricao']} | {req['estado']} | {req['cliente']}")
    
    def print_insights_menu(self):
        print("1. Ver faturas com dados anómalos.")
        print("2. Prever o valor da próxima fatura.")
        option = input("Opção: ")
        return int(option)
    
    def print_invoice_predictor_inputs(self):
        invoice_date = input("Insira a data de previsão (dd/mm/yyyy): ")
        invoice_category = input("Insira a categoria da fatura: ")
        invoice_payment_method = input("Insira o método de pagamento: ")
        username = input("Insira o nome de utilizador: ")
        return invoice_date,invoice_category,invoice_payment_method,username

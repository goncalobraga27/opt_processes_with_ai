import base64
import os
from pydoc import text
from menu import Menu
import csv
import pandas as pd
from ai_models import AnomalyDetector, ForecastPredictor, InvoicePredictor

class BusinessLogic:
    def __init__(self):
        self.menu = Menu()
        self.path_to_users_data = "../data/users_data.csv"
        self.path_to_request_data = "../data/request_data.csv"
        self.path_to_invoices_data = "../data/invoices_data.csv"
        os.makedirs(os.path.dirname(self.path_to_users_data), exist_ok=True)
        os.makedirs(os.path.dirname(self.path_to_request_data), exist_ok=True)
        os.makedirs(os.path.dirname(self.path_to_invoices_data), exist_ok=True)

    def encrypt(self, text):
        return base64.b64encode(text.encode()).decode()
    
    def decrypt(self, text):
        return base64.b64decode(text.encode()).decode()
    
    def authenticate_user(self, username, password):
        if not os.path.exists(self.path_to_users_data):
            return None
        

        with open(self.path_to_users_data, "r", encoding="utf-8") as file:
            lines = file.readlines() 
            for line in lines:
                stored_user, stored_pass = line.strip().split(",")

                dec_user = self.decrypt(stored_user)
                dec_pass = self.decrypt(stored_pass)


                if dec_user == username and dec_pass == password:
                    
                    return True

        return None
    
    def write_request_data(self, request_name, request_description, username):
        if not os.path.exists(self.path_to_request_data):
            with open(self.path_to_request_data, "w", encoding="utf-8") as file:
                file.write("request_name,request_description,username\n")

        with open(self.path_to_request_data, "a", encoding="utf-8") as file:
            file.write(f"{request_name},{request_description},{username}\n")
    
    def read_request_data(self, path):
        requests_list = []

        if not os.path.exists(path):
            return requests_list

        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                if not row:
                    continue

                nome = row[0].strip() if len(row) > 0 else ""
                descricao = row[1].strip() if len(row) > 1 else ""
                cliente = row[2].strip() if len(row) > 2 else ""

                # estado opcional
                estado = row[3].strip() if len(row) > 3 else "PENDENTE"

                requests_list.append({
                    "nome": nome,
                    "descricao": descricao,
                    "cliente": cliente,
                    "estado": estado
                })

        return requests_list

    def write_invoice_data(self, invoice_date, invoice_reference, invoice_category,
                       invoice_payment_method, invoice_amount, username):

        if not os.path.exists(self.path_to_invoices_data):
            with open(self.path_to_invoices_data, "w", encoding="utf-8") as file:
                file.write("invoice_date,invoice_reference,invoice_category,invoice_payment_method,invoice_amount,username\n")

        with open(self.path_to_invoices_data, "a", encoding="utf-8") as file:
            file.write(f"{invoice_date},{invoice_reference},{invoice_category},{invoice_payment_method},{invoice_amount},{username}\n")

    def choose_execution_flow(self, option):
        if option == 1:
            username, password = self.menu.print_open_session()
            if self.authenticate_user(username, password):
                option = self.menu.print_client_menu()
                self.choose_execution_flow_user(int(option), username)
            else:
                self.menu.print_error_authentication()
    
        elif option == 2:
            username, password = self.menu.print_open_session()
            if self.authenticate_user(username, password):
                option = self.menu.print_supplier_menu()
                self.choose_execution_flow_supplier(int(option), username)
            else:
                self.menu.print_error_authentication()

        elif option == 3:
            username, password = self.menu.print_open_session()
            if self.authenticate_user(username, password):
                option = self.menu.print_manager_menu()
                self.choose_execution_flow_manager(int(option),username)

        elif option == 4:
            username, password = self.menu.print_create_account()
            enc_username = self.encrypt(username)
            enc_password = self.encrypt(password)
            with open(self.path_to_users_data, "a", encoding="utf-8") as file:
                file.write(f"{enc_username},{enc_password}\n")        

        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")
    
    def choose_execution_flow_user(self, option, username):
        history_for_user_request = self.read_history_made_by_agent(username, "../data/agent_backup.csv")
        if option == 1:
            request_name, request_description = self.menu.print_add_request_menu()
            self.write_request_data(request_name, request_description, username)
        elif option == 2:
            self.menu.print_request_evolution_for_user(history_for_user_request)
        else:
            return 

    def choose_execution_flow_supplier(self, option, username):
        if option == 1:
            invoice_date, invoice_reference, invoice_category, invoice_payment_method, invoice_amount = self.menu.print_view_request_info_menu()
            self.write_invoice_data(invoice_date, invoice_reference, invoice_category, invoice_payment_method, invoice_amount, username)
        elif option == 2:
            return
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")

    def choose_execution_flow_manager(self,option, username):
        request_data = self.read_request_data(self.path_to_request_data)
        if option == 1:
            self.menu.show_request_data(request_data)
        elif option == 2: 
            request_number,new_request_state = self.menu.show_requests_for_update(request_data)
            self.update_request_status(request_number,new_request_state)
        elif option == 3:
            option = self.menu.print_insights_menu()
            self.execute_models(option)
    
    def execute_models(self, option):
        if option == 1: 
            # Carregar CSV
            df = pd.read_csv(self.path_to_invoices_data)

            # Treinar
            detector = AnomalyDetector(contamination=0.02)
            detector.fit(df)

            # Detetar anomalias para todas as faturas
            predictions = detector.predict(df)

            df_view = predictions.copy()

            df_view["invoice_amount"] = df_view["invoice_amount"].apply(lambda x: f"{x:,.0f} €")
            df_view["score"] = df_view["score"].round(3)

            df_view["prediction"] = df_view["prediction"].map({
                1: "🟢 Normal",
                -1: "🔴 Anómala"
            })

            cols = [
                "invoice_date",
                "invoice_reference",
                "invoice_category",
                "invoice_amount",
                "prediction",
                "status",
                "score"
            ]

            print(df_view[cols].to_string(index=False))
        elif option == 2: 
            invoice_date,invoice_category,invoice_payment_method,username = self.menu.print_invoice_predictor_inputs()
            # 2. Criar payload para o modelo
            invoice = {
                "invoice_date": invoice_date,
                "invoice_category": invoice_category,
                "invoice_payment_method": invoice_payment_method,
                "username": username
            }

            if not hasattr(self, "invoice_model"):
                # ideal: carregar modelo treinado
                try:
                    self.invoice_model = InvoicePredictor.load("invoice_model.joblib")
                except:
                    # fallback (se ainda não tiveres modelo guardado)
                    df = pd.read_csv(self.path_to_invoices_data)
                    self.invoice_model = InvoicePredictor()
                    self.invoice_model.fit(df)

            # 4. Fazer previsão
            prediction = self.invoice_model.predict(invoice)

            # 5. Output bonito
            print("\n==============================")
            print("💰 PREVISÃO DE FATURA")
            print("==============================")
            print(f"📅 Data: {invoice_date}")
            print(f"📂 Categoria: {invoice_category}")
            print(f"💳 Pagamento: {invoice_payment_method}")
            print(f"👤 Utilizador: {username}")
            print("------------------------------")
            print(f"👉 Valor previsto: {prediction:,.2f} €")
            print("==============================\n")
        elif option == 3:
            # 1. Ler dados
            df = pd.read_csv(self.path_to_invoices_data)

            # 2. Garantir que o modelo existe
            if not hasattr(self, "forecast_model"):
                self.forecast_model = ForecastPredictor(n_lags=12)

            # 3. Treinar se ainda não estiver treinado
            if not self.forecast_model.fitted:
                self.forecast_model.fit(df)

            # 4. Fazer previsão
            preds = self.forecast_model.forecast(12)

            # 5. Criar calendário mensal
            months = pd.date_range(
                start=pd.Timestamp.today().replace(day=1),
                periods=12,
                freq="ME"
            )

            # 6. Criar output bonito
            result = pd.DataFrame({
                "month": months,
                "forecast_invoice_value": preds
            })

            result["forecast_invoice_value"] = result["forecast_invoice_value"].round(2)

            df = result.copy()
            # 1. Remover hora do timestamp (ficar só mês)
            df["month"] = pd.to_datetime(df["month"]).dt.strftime("%Y-%m")
            # 2. Remover notação científica e formatar moeda
            df["forecast_invoice_value"] = df["forecast_invoice_value"].apply(lambda x: f"{x:,.2f} €")

            print("\n" + "=" * 60)
            print("📈 PREVISÃO DO VALOR TOTAL DAS FATURAS")
            print("=" * 60)
            print("Com base no histórico de faturação, o modelo estima os")
            print("seguintes valores para os próximos 12 meses:\n")

            for _, row in df.iterrows():
                print(f"📅 {row['month']:<7}  ➜  💰 {row['forecast_invoice_value']}")

            print("\n" + "-" * 60)
            print("ℹ️  Estes valores são estimativas produzidas pelo modelo")
            print("   de Machine Learning e devem ser utilizados como apoio")
            print("   à tomada de decisão.")
            print("=" * 60)
            
    def update_request_status(self, request_number, new_request_state):
        path = self.path_to_request_data

        if request_number is None or new_request_state is None:
            return

        with open(path, "r", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        if request_number < 0 or request_number >= len(rows):
            print("Pedido inválido.")
            return

        # garantir coluna estado
        while len(rows[request_number]) < 4:
            rows[request_number].append("PENDENTE")

        # tentar interpretar estado como número
        finalizado = False

        try:
            if isinstance(new_request_state, str):
                value = int(new_request_state.strip())
            else:
                value = int(new_request_state)

            if value > 5:
                final_state = "FINALIZADO"
                finalizado = True
            else:
                final_state = str(value)

        except:
            final_state = str(new_request_state)

        rows[request_number][3] = final_state

        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        if finalizado:
            print("✔ Processo finalizado automaticamente (estado > 5).")
        else:
            print(f"✔ Estado atualizado para: {final_state}")

    def read_history_made_by_agent(self,username,file_path):
        history_list = []
        if not os.path.exists(file_path):
            return history_list

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    continue

                data = row[0].strip() if len(row) > 0 else ""
                name = row[1].strip() if len(row) > 0 else ""
                descricao = row[2].strip() if len(row) > 1 else ""
                state = row[3].strip() if len(row) > 1 else ""
                cliente = row[4].strip() if len(row) > 2 else ""

                if cliente == username:
                    history_list.append({
                        "nome": name,
                        "descricao": descricao,
                        "cliente": cliente,
                        "estado": state,
                        "data": data,
                    })

        return history_list
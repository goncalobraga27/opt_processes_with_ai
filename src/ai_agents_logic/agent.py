import csv
import time
from datetime import datetime


class RequestWatcherAgent:

    def __init__(self, request_file_path, log_file_path):
        self.request_file_path = request_file_path
        self.log_file_path = log_file_path

        # memória persistente em runtime
        self.last_state = {}

        # carregar estado inicial
        self.load_initial_state()

    # -------------------------
    # carregar estado inicial
    # -------------------------
    def load_initial_state(self):
        try:
            with open(self.request_file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)

                for idx, row in enumerate(reader):
                    if not row:
                        continue

                    estado = row[3] if len(row) > 3 else "PENDENTE"

                    self.last_state[idx] = {
                        "nome": row[0],
                        "descricao": row[1],
                        "cliente": row[2],
                        "estado": estado
                    }

            print("🧠 Estado inicial carregado.")

        except FileNotFoundError:
            print("⚠️ Ficheiro de requests não encontrado.")

    # -------------------------
    # ler requests atuais
    # -------------------------
    def read_requests(self):
        current = {}

        try:
            with open(self.request_file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)

                for idx, row in enumerate(reader):
                    if not row:
                        continue

                    estado = row[3] if len(row) > 3 else "PENDENTE"

                    current[idx] = {
                        "nome": row[0],
                        "descricao": row[1],
                        "cliente": row[2],
                        "estado": estado
                    }

        except FileNotFoundError:
            pass

        return current

    # -------------------------
    # log de alterações
    # -------------------------
    def write_log(self, req):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                req["nome"],
                req["descricao"],
                req["estado"],
                req["cliente"]
            ])

    # -------------------------
    # verificar mudanças
    # -------------------------
    def check_changes(self):
        current = self.read_requests()

        for idx, new_req in current.items():

            old_req = self.last_state.get(idx)

            # novo pedido
            if old_req is None:
                self.last_state[idx] = new_req
                continue

            # mudança de estado
            if old_req["estado"] != new_req["estado"]:
                print(f"🔔 Mudança: {new_req['nome']} -> {new_req['estado']}")
                self.write_log(new_req)

            self.last_state[idx] = new_req

    # -------------------------
    # loop principal
    # -------------------------
    def start(self):
        print("🤖 Agente ativo com persistência...")

        while True:
            print("[AGENT] A sensorizar a ferramenta ...")
            self.check_changes()
            time.sleep(2)
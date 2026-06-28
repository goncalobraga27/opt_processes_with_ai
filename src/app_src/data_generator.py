import random
from datetime import datetime, timedelta

import pandas as pd


class InvoiceDataGenerator:

    def __init__(self):

        self.categories = [
            "cars",
            "alimentacao",
            "saude",
            "tecnologia",
            "educacao",
            "viagens",
            "lazer",
            "casa"
        ]

        self.payment_methods = [
            "PT50123456789",
            "PT50987654321",
            "PT50444555666",
            "4553363636",
            "MBWAY",
            "PAYPAL",
            "VISA",
            "MASTERCARD"
        ]

        self.users = [
            "goncalo",
            "ana",
            "joao",
            "maria",
            "pedro",
            "rita",
            "miguel",
            "sofia"
        ]

    def random_date(self, start, end):

        delta = end - start

        random_days = random.randint(0, delta.days)

        return start + timedelta(days=random_days)

    def random_amount(self, category):

        ranges = {
            "alimentacao": (20, 300),
            "cars": (5000, 500000),
            "saude": (30, 2000),
            "tecnologia": (100, 6000),
            "educacao": (50, 2500),
            "viagens": (200, 8000),
            "lazer": (20, 1000),
            "casa": (100, 10000)
        }

        minimum, maximum = ranges[category]

        value = random.uniform(minimum, maximum)

        # 2% de probabilidade de gerar uma anomalia
        if random.random() < 0.02:
            value *= random.randint(10, 50)

        return round(value, 2)

    def generate(self, n_rows=1000):

        start = datetime(2023, 1, 1)
        end = datetime(2026, 12, 31)

        invoices = []

        for i in range(1, n_rows + 1):

            date = self.random_date(start, end)

            category = random.choice(self.categories)

            invoice = {
                "invoice_date": date.strftime("%d/%m/%Y"),
                "invoice_reference": f"INV/{date.year}/{i:05d}",
                "invoice_category": category,
                "invoice_payment_method": random.choice(self.payment_methods),
                "invoice_amount": self.random_amount(category),
                "username": random.choice(self.users)
            }

            invoices.append(invoice)

        return pd.DataFrame(invoices)


if __name__ == "__main__":

    generator = InvoiceDataGenerator()

    df = generator.generate(5000)

    df = df.sort_values("invoice_date")

    df.to_csv("../data/invoices_data.csv", index=False)

    print(f"\nForam geradas {len(df)} faturas.")
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder


class InvoicePredictor:

    def __init__(self):

        self.model = RandomForestRegressor(
            n_estimators=300,
            random_state=42
        )

        self.encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value",
            unknown_value=-1
        )

        self.fitted = False

    # -----------------------------
    # Feature Engineering
    # -----------------------------
    def _prepare(self, df: pd.DataFrame):

        df = df.copy()

        df["invoice_date"] = pd.to_datetime(df["invoice_date"], dayfirst=True)

        df["month"] = df["invoice_date"].dt.month
        df["weekday"] = df["invoice_date"].dt.weekday

        categorical = [
            "invoice_category",
            "invoice_payment_method",
            "username"
        ]

        if not self.fitted:
            df[categorical] = self.encoder.fit_transform(df[categorical])
        else:
            df[categorical] = self.encoder.transform(df[categorical])

        return df[
            [
                "invoice_category",
                "invoice_payment_method",
                "username",
                "month",
                "weekday"
            ]
        ]

    # -----------------------------
    # Train
    # -----------------------------
    def fit(self, df: pd.DataFrame):

        X = self._prepare(df)
        y = df["invoice_amount"]

        self.model.fit(X, y)

        self.fitted = True

        return self

    # -----------------------------
    # Predict single invoice
    # -----------------------------
    def predict(self, invoice: dict):

        df = pd.DataFrame([invoice])

        X = self._prepare(df)

        pred = self.model.predict(X)[0]

        return float(pred)

    # -----------------------------
    # Predict batch
    # -----------------------------
    def predict_batch(self, df: pd.DataFrame):

        X = self._prepare(df)

        preds = self.model.predict(X)

        result = df.copy()
        result["predicted_invoice_amount"] = preds

        return result

    # -----------------------------
    # Save / Load
    # -----------------------------
    def save(self, path):
        joblib.dump({
            "model": self.model,
            "encoder": self.encoder,
            "fitted": self.fitted
        }, path)

    @classmethod
    def load(cls, path):

        data = joblib.load(path)

        obj = cls()
        obj.model = data["model"]
        obj.encoder = data["encoder"]
        obj.fitted = data["fitted"]

        return obj
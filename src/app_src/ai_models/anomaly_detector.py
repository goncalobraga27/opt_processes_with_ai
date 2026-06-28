from pathlib import Path
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OrdinalEncoder


class AnomalyDetector:

    def __init__(
        self,
        contamination=0.02,
        random_state=42
    ):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state
        )

        self.encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value",
            unknown_value=-1
        )

        self.fitted = False

    # ----------------------------
    # Feature Engineering
    # ----------------------------

    def _prepare_dataframe(self, df: pd.DataFrame):

        df = df.copy()

        df["invoice_date"] = pd.to_datetime(
            df["invoice_date"],
            dayfirst=True
        )

        df["month"] = df["invoice_date"].dt.month
        df["day"] = df["invoice_date"].dt.day
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
                "invoice_amount",
                "invoice_category",
                "invoice_payment_method",
                "username",
                "month",
                "day",
                "weekday"
            ]
        ]

    # ----------------------------
    # Train
    # ----------------------------

    def fit(self, dataframe: pd.DataFrame):

        X = self._prepare_dataframe(dataframe)

        self.model.fit(X)

        self.fitted = True

        return self

    # ----------------------------
    # Predict
    # ----------------------------

    def predict(self, dataframe):
        if not self.fitted:
            raise RuntimeError("Modelo ainda não foi treinado.")

        X = self._prepare_dataframe(dataframe)

        result = dataframe.copy()
        result["prediction"] = self.model.predict(X)
        result["score"] = self.model.decision_function(X)

        result["status"] = result["prediction"].map({
            1: "Normal",
            -1: "Anómala"
        })

        return result

    # ----------------------------
    # Score
    # ----------------------------

    def anomaly_score(self, dataframe: pd.DataFrame):

        if not self.fitted:
            raise RuntimeError("Modelo ainda não foi treinado.")

        X = self._prepare_dataframe(dataframe)

        return self.model.decision_function(X)

    # ----------------------------
    # Save
    # ----------------------------

    def save(self, path):

        joblib.dump(
            {
                "model": self.model,
                "encoder": self.encoder,
                "fitted": self.fitted,
            },
            path,
        )

    # ----------------------------
    # Load
    # ----------------------------

    @classmethod
    def load(cls, path):

        data = joblib.load(path)

        detector = cls()

        detector.model = data["model"]
        detector.encoder = data["encoder"]
        detector.fitted = data["fitted"]

        return detector
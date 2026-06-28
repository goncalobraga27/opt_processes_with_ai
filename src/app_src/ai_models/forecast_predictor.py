import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor


class ForecastPredictor:

    def __init__(self, n_lags=12, random_state=42):
        self.n_lags = n_lags

        self.model = RandomForestRegressor(
            n_estimators=500,
            random_state=random_state
        )

        self.fitted = False
        self.history = None

    # -----------------------
    # Feature Engineering
    # -----------------------
    def _prepare_series(self, df):

        df = df.copy()

        df["invoice_date"] = pd.to_datetime(df["invoice_date"], dayfirst=True)

        monthly = (
            df.groupby(pd.Grouper(key="invoice_date", freq="ME"))["invoice_amount"]
            .sum()
            .sort_index()
        )

        return monthly

    # -----------------------
    # Create supervised data
    # -----------------------
    def _create_lags(self, series):
        # Converter corretamente a Series para DataFrame
        ts = series.to_frame(name="value").copy()

        # Criar os lags
        for i in range(1, self.n_lags + 1):
            ts[f"lag_{i}"] = ts["value"].shift(i)

        # Remover apenas as linhas que ficaram incompletas devido aos lags
        ts = ts.dropna().reset_index(drop=True)

        # Separar features e target
        X = ts[[f"lag_{i}" for i in range(1, self.n_lags + 1)]]
        y = ts["value"]

        return X, y

    # -----------------------
    # Train
    # -----------------------
    def fit(self, df):

        series = self._prepare_series(df)

        if len(series) <= self.n_lags:
            raise ValueError(
                f"São necessários mais de {self.n_lags} meses de histórico. "
                f"Foram encontrados apenas {len(series)}."
            )

        X, y = self._create_lags(series)

        self.model.fit(X, y)

        self.history = list(series.values)

        self.fitted = True

        return self

    # -----------------------
    # Predict next n months
    # -----------------------
    def forecast(self, steps=12):

        if not self.fitted:
            raise RuntimeError("Modelo ainda não foi treinado.")

        history = self.history.copy()

        predictions = []

        for _ in range(steps):

            if len(history) < self.n_lags:
                raise ValueError("Histórico insuficiente para lags.")

            columns = [f"lag_{i}" for i in range(1, self.n_lags + 1)]

            x_input = pd.DataFrame(
                [history[-self.n_lags:]],
                columns=columns
            )

            pred = self.model.predict(x_input)[0]

            predictions.append(pred)

            history.append(pred)

        return predictions

    # -----------------------
    # Save / Load
    # -----------------------
    def save(self, path):
        joblib.dump({
            "model": self.model,
            "history": self.history,
            "n_lags": self.n_lags,
            "fitted": self.fitted
        }, path)

    @classmethod
    def load(cls, path):

        data = joblib.load(path)

        obj = cls(n_lags=data["n_lags"])

        obj.model = data["model"]
        obj.history = data["history"]
        obj.fitted = data["fitted"]

        return obj
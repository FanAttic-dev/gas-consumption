from pathlib import Path
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from datetime import datetime


class DataAnalyzer:
    def __init__(self, csv_name: str):
        self.csv_name = csv_name
        self.df = pd.read_csv(csv_name, decimal=',')
        self.df["digits"] = self.df["digits"].astype(float)
        self.df = self.df.sort_values("img_name")
        self.df["date"] = self.df["img_name"].apply(
            DataAnalyzer.img_name_to_date
        )

    @staticmethod
    def img_name_to_date(img_name: str) -> str:
        dt = datetime.strptime(Path(img_name).stem, '%Y%m%d_%H%M%S')
        return f"{dt.day}.{dt.month}.{dt.year}"

    def discard_outliers_LOF(self, df):
        clf = LocalOutlierFactor(n_neighbors=20, contamination=0.3)
        X = np.reshape(df["digits"], (-1, 1))

        y_pred = clf.fit_predict(X)
        n_outliers = sum(y_pred == -1)

        return self.df[y_pred == 1], n_outliers

    def discard_outliers_quantile(self, q=0.8):
        n_orig = len(self.df)
        q = self.df["digits"].quantile(0.8)
        df = self.df[self.df["digits"] < q]
        n_outliers = n_orig - len(df)
        return df, n_outliers

    def analyze(self):

        n_orig = len(self.df)

        self.df = self.df.dropna()
        n_na = n_orig - len(self.df)

        # self.df, n_outliers = self.discard_outliers_quantile(self.df)
        self.df, n_outliers = self.discard_outliers_LOF(self.df)

        print(
            f"Original size: {n_orig}, NaN count: {n_na}, outlier count: {n_outliers}"
        )

        plt.plot(self.df["date"], self.df["digits"], marker='o')
        plt.grid(axis='y')
        plt.gcf().autofmt_xdate()
        plt.show()

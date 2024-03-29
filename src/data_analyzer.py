from pathlib import Path
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from datetime import datetime
import matplotlib.dates as mdates


class DataAnalyzer:
    def __init__(self, csv_name: str):
        self.csv_name = csv_name
        self.df = pd.read_csv(csv_name, decimal=',')
        self.df["digits"] = self.df["digits"].astype(float)
        self.df["date"] = self.df["img_name"].apply(
            DataAnalyzer.img_name_to_date
        )
        self.df.set_index('date', inplace=True)
        self.df.sort_index(inplace=True)

    @staticmethod
    def img_name_to_date(img_name: str) -> str:
        return datetime.strptime(Path(img_name).stem, '%Y%m%d_%H%M%S')

    def discard_outliers_LOF(self, df: pd.DataFrame):
        df = df.dropna()
        clf = LocalOutlierFactor(n_neighbors=20, contamination=0.3)
        X = np.reshape(df["digits"], (-1, 1))

        y_pred = clf.fit_predict(X)
        n_outliers = sum(y_pred == -1)

        return df[y_pred == 1], n_outliers

    def analyze(self):
        n_orig = len(self.df)
        n_na = self.df["digits"].isna().sum()

        self.df, n_outliers = self.discard_outliers_LOF(self.df)

        print(
            f"Original size: {n_orig}, NaN count: {n_na}, Outlier count: {n_outliers}"
        )

        plt.plot(self.df.index, self.df["digits"], marker='o')
        plt.title("Gas consumption [m3]")
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        plt.grid()
        plt.show()

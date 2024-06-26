from pathlib import Path
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib

from services.constants import CSV_FILENAME, FIGURE_FILENAME, FIGURES_DIRNAME, CSV_DIRNAME, MIN_IMAGES


class DataAnalyzer:
    LOF_N_NEIGHBORS = 20
    LOF_CONTAMINATION = 0.3
    
    def __init__(self, csv_folder: Path, figures_folder: Path, lof_n_neighbors=LOF_N_NEIGHBORS, lof_contamination=LOF_CONTAMINATION):
        self.figures_folder = figures_folder
        figures_folder.mkdir(exist_ok=True, parents=True)
        csv_path = csv_folder / CSV_FILENAME
        self.df = pd.read_csv(csv_path, decimal=',')
        self.df["digits"] = self.df["digits"].astype(float)
        self.df["date"] = self.df["img_name"].apply(
            DataAnalyzer.img_name_to_date
        )
        self.df.set_index('date', inplace=True)
        self.df.sort_index(inplace=True)
        
        self.lof_n_neighbors = lof_n_neighbors
        self.lof_contamination = lof_contamination

    @staticmethod
    def img_name_to_date(img_name: str) -> str:
        return datetime.strptime(Path(img_name).stem, '%Y%m%d_%H%M%S')

    def discard_na_outliers_LOF(self, df: pd.DataFrame) -> pd.DataFrame:
        n_orig = len(df)
        n_na = df["digits"].isna().sum()

        df = df.dropna()
        clf = LocalOutlierFactor(n_neighbors=self.lof_n_neighbors, contamination=self.lof_contamination)
        X = np.reshape(df["digits"], (-1, 1))

        y_pred = clf.fit_predict(X)
        n_outliers = sum(y_pred == -1)

        print(
            f"Original size: {n_orig}, NaN count: {n_na}, Outlier count: {n_outliers}"
        )

        return df[y_pred == 1]

    def plot_gas_meter_values(self, ax: plt.Axes):
        ax.plot(self.df.index, self.df["digits"], marker='o')
        ax.set_title("Gas meter values [m3]")
        plt.gcf().autofmt_xdate()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        ax.grid()
            

    def plot_mean_gas_consumption_per_month(self, ax: plt.Axes):
        consumption_per_month = self.df.groupby(pd.Grouper(freq='ME'))[
            ['digits']].last().diff().rename(columns={'digits': 'consumption'})
        mean_consumption_per_month = consumption_per_month.groupby(
            consumption_per_month.index.month).mean().rename_axis("month")

        mean_consumption_per_month.plot.bar(ax=ax)
        ax.set_title('Mean gas consumption per month')
        ax.set_ylabel("Gas consumption [m3]")
        ax.set_xlabel("Month")
        ax.legend().remove()

    def analyze(self, show: bool):
        if not show:
            matplotlib.use('agg')
                    
        self.df = self.discard_na_outliers_LOF(self.df)
        
        fig, ax = plt.subplots(1, 2, figsize=(8, 3))
        self.plot_gas_meter_values(ax[0])
        self.plot_mean_gas_consumption_per_month(ax[1])
        plt.savefig(self.figures_folder / FIGURE_FILENAME)
        if show:
            plt.show()

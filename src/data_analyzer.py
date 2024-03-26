import pandas as pd
from matplotlib import pyplot as plt

class DataAnalyzer:
    def __init__(self, csv_name: str):
        self.csv_name = csv_name
        self.df = pd.read_csv(csv_name, decimal=',')
        self.df["digits"] = self.df["digits"].astype(float)
        self.df = self.df.sort_values("img_name")
        
    def analyze(self):
        # q = self.df["digits"].quantile(0.8)
        # df_filt = self.df[self.df["digits"] < q]
        df_filt = self.df
        
        plt.scatter(df_filt["img_name"], df_filt["digits"])
        # plt.boxplot(self.df.index, self.df["digits"])
        plt.show()
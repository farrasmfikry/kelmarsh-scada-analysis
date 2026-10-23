import matplotlib as plt
import pandas as pd
import seaborn as sns
import numpy as np

sns.set_theme(style="whitegrid")

def plot_empirical_power (df: pd.DataFrame, wind_speed_col: str = 'Windspeed_avg', power_col: str = 'power_avg', turbine_name: str = 'turbine' ):

    fig, ax = plt.subplots(figsize=(10,6))

    #1. Raw Data Scatter
    ax.scatter(df[wind_speed_col], df[power_col], alpha=0.15, color='dodgerblue', s=10, label='10-min SCADA Data' )

    #2. Calculate Binned Average
    bins = np.arange (0, df[wind_speed_col].max() + 0.5, 0.5)
    df['Wind_Bin'] = pd.cut(df[wind_speed_col], bins=bins)
    binned = df.groundby('Wind_Bin', observed=False)[]



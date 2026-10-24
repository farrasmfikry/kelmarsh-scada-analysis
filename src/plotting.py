import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

sns.set_theme(style="whitegrid")

def plot_empirical_power_curve (df: pd.DataFrame, wind_speed_col: str = 'Wind speed (m/s)', power_col: str = 'Power (kW)', turbine_name: str = 'Turbine' ):

    fig, ax = plt.subplots(figsize=(10,6))

    #1. Raw Data Scatter
    ax.scatter(df[wind_speed_col], df[power_col], alpha=0.15, color='dodgerblue', s=10, label='10-min SCADA Data' )

    #2. Calculate Binned Average (Bin widt = 0.5 m/s)
    bins = np.arange (0, df[wind_speed_col].max() + 0.5, 0.5)
    df['Wind_Bin'] = pd.cut(df[wind_speed_col], bins=bins)
    binned = df.groupby('Wind_Bin', observed=False)[power_col].mean().reset_index()
    binned['Bin_Center'] = binned['Wind_Bin'].apply(lambda x: x.mid)

    #3 Plot Binned Mean Line
    ax. plot(binned['Bin_Center'], binned[power_col], color='darkred', linewidth=2.5, marker='o', markersize=5, label='Binned Mean Power Curve')

    #Formatting
    ax.set_title(f'Empirical Power Curve - {turbine_name}', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Wind Speed (m/s)', fontsize=12)
    ax.set_ylabel('Active Power(kW)', fontsize=12)
    ax.legend(frameon=True, facecolor='white', loc='upper left')
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    return fig, ax


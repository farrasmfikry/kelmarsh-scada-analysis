import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from windrose import WindroseAxes

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

def plot_wind_rose (df: pd.DataFrame, speed_col: str = 'Wind speed (m/s)', dir_col: str = 'Wind direction (°)', turbine_name: str = 'Turbine'):
    """
    Plots a standardized wind rose showing wind speed frequency and directional distribution.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing wind speed and wind direction columns.
    speed_col : str
        Column name for wind speed (m/s).
    dir_col : str
        Column name for wind direction (degrees).
    turbine_name : str
        Identifier for the turbine or meteorological mast.
    """
    # Create a polar projection figure for the wind rose
    fig = plt.figure(figsize=(8, 8))
    ax = WindroseAxes.from_ax(fig=fig)
    
    # Extract arrays and drop any missing values for these specific columns
    plot_data = df[[speed_col, dir_col]].dropna()
    wind_speed = plot_data[speed_col].values
    wind_dir = plot_data[dir_col].values
    
    # Plot wind rose (normed=True displays percentage frequency)
    ax.bar(
        wind_dir, 
        wind_speed, 
        normed=True, 
        opening=0.8, 
        edgecolor='white', 
        bins=np.arange(0, 20, 2), # 2 m/s speed bins up to 20 m/s
        cmap=plt.cm.viridis
    )
    
    # Formatting legend and title
    ax.set_legend(title="Wind Speed (m/s)", loc="upper right", bbox_to_anchor=(1.25, 1.0))
    ax.set_title(f"Site Wind Rose & Sector Analysis - {turbine_name}", va="bottom", fontsize=14, fontweight='bold', pad=20)
    
    return fig, ax

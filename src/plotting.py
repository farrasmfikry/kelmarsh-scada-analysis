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

def plot_scada_timeseries_anomaly(df: pd.DataFrame, start_time: str, end_time: str,
                                  power_col: str = 'Power (kW)',
                                  temp_col: str = 'Gear oil temperature (°C)',
                                  wind_col: str = 'Wind speed (m/s)',
                                  turbine_name: str = 'Turbine'):
    """
    Plots a multi-axis time-series window to inspect physical correlations between 
    wind speed, power output, and component temperatures during operational anomalies.
    """
    # Slice the dataframe to the desired time window
    window_df = df.loc[start_time:end_time]

    if window_df.empty:
        raise ValueError(f"No data found between {start_time} and {end_time}. Check your date format and index. ")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8), sharex=True)

    # 1. Top Subplot: Wind Speed & Active Power
    color = 'tab:blue'
    ax1.set_ylabel('Wind Speed (m/s)', color=color, fontsize=11)
    line1 = ax1.plot(window_df.index, window_df[wind_col], color=color, alpha=0.7, label='Wind Speed')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    ax1_twin = ax1.twinx()
    color = 'tab:orange'
    ax1_twin.set_ylabel('Active Power (kW)', color=color, fontsize=11)
    line2 = ax1_twin.plot(window_df.index, window_df[power_col], color=color, alpha=0.8, label='Active Power')
    ax1_twin.tick_params(axis='y', labelcolor=color)
    ax1_twin.grid(False) # Avoid grid overlap
    
    # Combine legends for top plot
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    ax1.set_title(f'Telemetry & Operational Window - {turbine_name} ({start_time} to {end_time})', fontsize=13, fontweight='bold')

    # 2. Bottom Subplot: Component Temperatures
    color = 'tab:red'
    ax2.set_ylabel('Temperature (°C)', color=color, fontsize=11)
    ax2.plot(window_df.index, window_df[temp_col], color=color, linewidth=1.5, label='Gearbox / Bearing Temp')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('Timestamp', fontsize=11)
    ax2.legend(loc='upper left')

    plt.tight_layout()
    return fig, (ax1, ax2)

def plot_multi_turbine_power_curves(turbine_dfs: dict, wind_speed_col: str = 'Wind speed (m/s)', power_col: str = 'Power (kW)'):
    """
    Compares the empirical power curves of multiple wind turbines in a wind farm.
    
    Parameters:
    -----------
    turbine_dfs : dict
        A dictionary where keys are turbine names (e.g., 'Turbine 1') 
        and values are their respective cleaned pandas DataFrames.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define a color palette for distinction
    colors = plt.cm.tab10(np.linspace(0, 1, len(turbine_dfs)))
    
    for (name, df), color in zip(turbine_dfs.items(), colors):
        # Calculate binned mean power curve for each turbine
        bins = np.arange(0, df[wind_speed_col].max() + 0.5, 0.5)
        df_temp = df.copy()
        df_temp['Wind_Bin'] = pd.cut(df_temp[wind_speed_col], bins=bins)
        binned = df_temp.groupby('Wind_Bin', observed=False)[power_col].mean().reset_index()
        binned['Bin_Center'] = binned['Wind_Bin'].apply(lambda x: x.mid)
        
        # Plot binned mean line
        ax.plot(binned['Bin_Center'], binned[power_col], color=color, linewidth=2, label=name)
        
    ax.set_title('Farm-Wide Multi-Turbine Power Curve Comparison', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Wind Speed (m/s)', fontsize=12)
    ax.set_ylabel('Active Power (kW)', fontsize=12)
    ax.legend(frameon=True, facecolor='white', loc='upper left')
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    return fig, ax
import pandas as pd
from pathlib import Path

def generate_scada_overview_report(turbine_dfs: dict, power_col: str = 'Power (kW)', rated_power_mw: float = 2.0) -> pd.DataFrame:
    """
    Generates a multi-turbine SCADA overview audit summary matching OpenWindSCADA standards.
    
    Parameters:
    -----------
    turbine_dfs : dict
        Dictionary of turbine names/IDs as keys and their pandas DataFrames as values.
    power_col : str
        Column name for active power (assumed in kW).
    rated_power_mw : float
        Rated capacity of the turbine in MW (Senvion MM92 is typically ~2.0 MW).
        
    Returns:
    --------
    pd.DataFrame
        Formatted overview audit table.
    """
    report_data = {}
    
    for t_name, df in turbine_dfs.items():
        # Ensure index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError(f"DataFrame for {t_name} must have a DatetimeIndex.")
            
        first_ts = df.index.min()
        last_ts = df.index.max()
        n_vars = len(df.columns)
        n_datapoints = len(df)
        
        # Expected 10-min intervals over the active time span
        full_range = pd.date_range(start=first_ts, end=last_ts, freq='10min')
        expected_points = len(full_range)
        
        # Count missing power measurements as missing datapoints.
        power_valid_points = df[power_col].notna().sum()
        missing_points = expected_points - power_valid_points
        uptime_pct = (
            power_valid_points / expected_points * 100
            if expected_points > 0
            else 0.0
        )
        
        # Energy Produced Total (MWh): ActivePower (kW) * (10 minutes / 60 mins) / 1000 = MWh
        # Assuming regular 10-min spacing for valid rows
        total_energy_mwh = (df[power_col].sum() * (10 / 60)) / 1000.0
        
        # Hours in period and Capacity Factor
        total_hours = n_datapoints * (10 / 60)
        max_possible_energy = rated_power_mw * total_hours
        capacity_factor = total_energy_mwh / max_possible_energy if max_possible_energy > 0 else 0.0
        
        # Full Load Hours (FLH) = Total Energy Produced (MWh) / Rated Power (MW)
        flh = total_energy_mwh / rated_power_mw
        
        report_data[t_name] = {
            "# Variables": float(n_vars),
            "First Timestamp": str(first_ts),
            "Last Timestamp": str(last_ts),
            "# Datapoints": float(n_datapoints),
            "Datapoints missing": float(max(0, missing_points)),
            "Data uptime (%)": round(uptime_pct, 1),
            "Energy Produced Total (MWh)": round(total_energy_mwh, 1),
            "Capacity Factor": round(capacity_factor, 2),
            "FLH (h)": round(flh, 1)
        }
        
    summary_df = pd.DataFrame(report_data)
    return summary_df
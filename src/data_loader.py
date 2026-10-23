import pandas as pd
from pathlib import Path

def load_scada_data(file_path: str | Path) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found at: {path}")
    #read CSV
    # The first nine lines are metadata; line 10 is the header, including its leading "#" marker in Greenbyte exports.
    df = pd.read_csv(path, skiprows=9)
    df.columns = df.columns.str.lstrip("#").str.strip()
    

    #SCADA timestamp column check (adjust to match the actual CSV columns)
    timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]

    if timestamp_cols:
        ts_col = timestamp_cols [0]
        df[ts_col] = pd.to_datetime(df[ts_col])
        df = df.sort_values(by=ts_col).reset_index(drop=True)
        df.set_index(ts_col, inplace=True)
    else:
        print ("Warning: No timestamp coloumn detected. Check column name ")

    return df

def filter_operational_data(df: pd.DataFrame, power_col: str = 'ActivePower_Avg', wind_speed_col: str = 'WindSpeed_Avg') ->pd.DataFrame:
 
    cleaned_df = df.copy()

     #remove negative power values caused by sensor errors
    if power_col in cleaned_df.columns:
        cleaned_df = cleaned_df[cleaned_df[power_col] >= 0]

    return cleaned_df
           
                
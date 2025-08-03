import pandas as pd

def assign_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    if 'total_fantasy_ppr' not in df.columns:
        raise ValueError("Missing 'total_fantasy_ppr' column in input data.")
    
    max_points = df['total_fantasy_ppr'].max()
    df['auto_dollar_value'] = (df['total_fantasy_ppr'] / max_points * 60).round(2)
    return df

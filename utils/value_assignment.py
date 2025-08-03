
def assign_values(df):
    df = df.copy()
    max_total = df['total_fantasy_ppr'].max()
    df['auto_dollar_value'] = (df['total_fantasy_ppr'] / max_total * 60).round(2)
    return df

import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Convert crash_date and crash_hour to datetime
    df["crash_date"] = pd.to_datetime(df["crash_date"], errors="coerce")
    df["crash_hour"] = pd.to_numeric(df["crash_hour"], errors="coerce").fillna(0)

    # Month & weekday
    df["month"] = df["crash_date"].dt.month
    df["weekday"] = df["crash_date"].dt.day_name()

    # Fatal flag
    df["is_fatal"] = df["injuries_fatal"].fillna(0).astype(int) > 0

    # Default injuries_total
    df["injuries_total"] = pd.to_numeric(df.get("injuries_total", pd.Series([0]*len(df))), errors="coerce").fillna(0)

    return df

def compute_kpis(df):
    total = len(df)
    fatal_pct = df["is_fatal"].mean() * 100 if total else 0
    avg_injuries = df["injuries_total"].mean()
    top_weather = df["weather_condition"].value_counts().idxmax() if not df["weather_condition"].value_counts().empty else "Unknown"
    return {"total": total, "fatal_pct": fatal_pct, "avg_injuries": avg_injuries, "top_weather": top_weather}

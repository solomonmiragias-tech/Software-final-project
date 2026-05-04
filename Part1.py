import os
import pandas as pd

def export_daily_close_onecol(
    csv_path: str,
    out_txt_path: str,
    ticker: str,
    start_date: str | None = None,
    end_date: str | None = None,
    tz: str = "America/New_York",
):
    usecols_try = ["timestamp", "close", "ticker"]

    try:
        it = pd.read_csv(csv_path, usecols=usecols_try, chunksize=2_000_000, dtype={"ticker": "string"})
        timestamp_col = "timestamp"
    except ValueError:
        usecols_try = ["Unnamed: 0", "close", "ticker"]
        it = pd.read_csv(csv_path, usecols=usecols_try, chunksize=2_000_000, dtype={"ticker": "string"})
        timestamp_col = "Unnamed: 0"

    start = pd.Timestamp(start_date, tz=tz) if start_date else None
    end = pd.Timestamp(end_date, tz=tz) if end_date else None

    daily_parts = []

    for chunk in it:
        ts_utc = pd.to_datetime(chunk[timestamp_col], utc=True, errors="coerce")
        ts = ts_utc.dt.tz_convert(tz)

        mask = (chunk["ticker"] == ticker)
        if start is not None:
            mask &= (ts >= start)
        if end is not None:
            mask &= (ts <= end + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))

        if mask.any():
            daily_parts.append(pd.DataFrame({"ts": ts[mask].values, "close": chunk.loc[mask, "close"].values}))

    if not daily_parts:
        open(out_txt_path, "w").close()
        return pd.Series(dtype="float64")

    df = pd.concat(daily_parts, ignore_index=True).sort_values("ts")
    daily_close = df.groupby(df["ts"].dt.date)["close"].last()

    daily_close.to_csv(out_txt_path, index=False, header=False, float_format="%.6f")
    return daily_close

csv_path = "SP500.min.2023Jan.bars.csv"
out_path = "VISA_close.txt"

print("CSV exists?", os.path.exists(csv_path))

daily = export_daily_close_onecol(
        csv_path=csv_path,
        out_txt_path=out_path,
        ticker="V",
        start_date="2023-01-01",
        end_date="2023-01-31",
    )

print("WROTE:", out_path, "exists?", os.path.exists(out_path))
print("N daily points:", len(daily))
print(daily.head())


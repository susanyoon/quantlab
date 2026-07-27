from pathlib import Path

import pandas as pd

dates = pd.to_datetime(["2023-01-03", "2023-01-04", "2023-01-05"])
df = pd.DataFrame(
    {
        "open": [100.0, 101.0, 102.0],
        "high": [103.0, 104.0, 105.0],
        "low": [99.0, 100.0, 101.0],
        "close": [102.0, 103.0, 104.0],
        "volume": [1_000_000, 1_100_000, 1_050_000],
    },
    index=dates,
)
df.index.name = "date"

out = Path("tests/data")
out.mkdir(parents=True, exist_ok=True)
df.to_parquet(out / "AAPL_2023-01-03_2023-01-06.parquet")
print("Fixture written.")

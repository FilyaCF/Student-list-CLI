import pandas as pd
from pathlib import Path


def save_to_csv(df: pd.DataFrame, path: str | Path):
    """Save a DataFrame to a CSV file at the given path.

    Parent directories are created automatically if they do not exist.
    The index is not written to the file.

    Args:
        df: The DataFrame to save.
        path: Destination file path.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")

def load_from_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path}")

    df = pd.read_csv(path, na_values=["None"])

    int_cols = [c for c in df.columns
                if c in ("id", "group") or c.startswith("mark_")]
    df[int_cols] = df[int_cols].astype("Int64")
    return df

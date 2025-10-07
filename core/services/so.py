import pandas as pd
from core.model.so import fetch_struktur_organisasi


def fetch_hierarchy():
    df = fetch_struktur_organisasi()

    return build_hierarchy(df)


def build_hierarchy(df: pd.DataFrame) -> dict:
    """
    Build hierarchy using pandas operations for better performance with large datasets.
    """
    if df.empty:
        return {"hierarchy": {}}

    # Create nodes dictionary using dict comprehension
    nodes = {
        row["key"]: {**row, 'subordinates': []}
        for row in df.to_dict(orient="records")
    }

    # Find root node using pandas filtering
    root_row = df[df["boss"] == 0]
    if not root_row.empty:
        root_key = root_row.iloc[0]["key"]
        root_node = {"hierarchy": nodes[root_key]}
    else:
        # Fallback: use first node as root if no boss=0 found
        root_key = df.iloc[0]["key"]
        root_node = {"hierarchy": nodes[root_key]}

    # Build hierarchy using vector-like operations
    for _, row in df.iterrows():
        key = row["key"].item()  # Get scalar value
        boss_id = row["boss"].item()  # Get scalar value

        if boss_id != 0 and boss_id in nodes:
            nodes[boss_id]["subordinates"].append(nodes[key])

    return root_node

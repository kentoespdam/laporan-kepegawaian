import pandas as pd
from core.model.so import fetch_struktur_organisasi


def fetch_hierarchy():
    df = fetch_struktur_organisasi()

    return build_hierarchy(df)


def build_hierarchy(df: pd.DataFrame) -> dict:
    nodes = {item["key"]: {**item, 'subordinates': []}
             for item in df.to_dict(orient="records")}
    # ic(nodes)

    for _, node in nodes.items():
        parent_id = node.get("boss")
        if parent_id == 0:
            root = {"hieararchy": node}
        elif parent_id in nodes:
            nodes[parent_id]["subordinates"].append(node)

    return root

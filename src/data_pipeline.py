from __future__ import annotations
import hashlib, json, zipfile
from datetime import datetime, timezone
from pathlib import Path
from io import BytesIO
import pandas as pd
import requests
from .config import RAW, METADATA, STATCAN_TABLES

def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def download_statcan_table(key: str, timeout: int = 90) -> Path:
    """Download/extract a Statistics Canada full-table ZIP and save provenance."""
    if key not in STATCAN_TABLES:
        raise KeyError(f"Unknown Statistics Canada source key: {key}")
    RAW.mkdir(parents=True, exist_ok=True)
    METADATA.mkdir(parents=True, exist_ok=True)
    spec = STATCAN_TABLES[key]
    response = requests.get(spec["url"], timeout=timeout,
                            headers={"User-Agent": "SE-Bridge-Research/0.1"})
    response.raise_for_status()
    payload = response.content
    if not payload.startswith(b"PK"):
        raise ValueError("Expected a ZIP response from Statistics Canada")
    zip_path = RAW / f"{spec['table_id']}-eng.zip"
    zip_path.write_bytes(payload)
    with zipfile.ZipFile(BytesIO(payload)) as archive:
        members = [n for n in archive.namelist() if n.lower().endswith(".csv")]
        if not members:
            raise ValueError("No CSV member found in downloaded ZIP")
        member = next((n for n in members if "metadata" not in n.lower()), members[0])
        csv_bytes = archive.read(member)
    csv_path = RAW / f"{spec['table_id']}.csv"
    csv_path.write_bytes(csv_bytes)
    manifest = {
        "publisher": "Statistics Canada", "table_id": spec["table_id"],
        "title": spec["title"], "url": spec["url"],
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "zip_sha256": sha256_bytes(payload), "csv_sha256": sha256_bytes(csv_bytes),
        "zip_member": member, "licence": "Open Government Licence - Canada; verify source terms"
    }
    (METADATA / f"{spec['table_id']}_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")
    return csv_path

def read_statcan_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]
    return df

def build_analysis_extract(table_path: str | Path, output_path: str | Path,
                           dimension_hint: str) -> pd.DataFrame:
    """Retain all source dimensions; do not guess measure, sex, year or industry filters."""
    df = read_statcan_csv(table_path)
    if "VALUE" not in df.columns:
        raise ValueError("Expected VALUE column in Statistics Canada table")
    df["VALUE"] = pd.to_numeric(df["VALUE"], errors="coerce")
    df["source_table"] = Path(table_path).stem
    df["dimension_hint"] = dimension_hint
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df

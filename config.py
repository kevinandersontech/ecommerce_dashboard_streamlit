
import os
from pathlib import Path

# Default location relative to this app folder
DEFAULT_DB = Path(__file__).parent.parent / "ecommerce_data_pipeline_v1" / "warehouse" / "ecom.duckdb"

def get_duckdb_path() -> str:
    """Resolve DuckDB file path from environment or use default."""
    return str(os.environ.get("DUCKDB_PATH", DEFAULT_DB))

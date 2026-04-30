from pathlib import Path
import yaml


def load_report_config(path: str) -> dict:
    report_path = Path(path)

    if not report_path.exists():
        raise FileNotFoundError(f"Report config not found: {path}")

    with report_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("Report config must be a YAML object.")

    required_fields = ["name", "owner", "email", "sources", "template"]
    missing = [field for field in required_fields if field not in config]

    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")

    return config

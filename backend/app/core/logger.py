"""Simple logging utility.

Provides a helper to save debug logs into the logs directory with a
module-specific filename and timestamp.
"""

from datetime import datetime
from pathlib import Path

TIME_FMT = "%m%d%H%M"
BASE_DIR = Path(__file__).resolve().parents[3]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


def write_log(module_name: str, content: str) -> None:
    """Write content to a log file.

    Args:
        module_name: Module name used for the log filename.
        content: Text to record.

    Returns:
        None
    """
    timestamp = datetime.now().strftime(TIME_FMT)
    file_path = LOG_DIR / f"{module_name}{timestamp}.log"
    try:
        with file_path.open("w", encoding="utf-8") as log_file:
            log_file.write(content)
    except OSError as err:
        print(f"log write failed: path={file_path}, error={err}")

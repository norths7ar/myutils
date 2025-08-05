import inspect
import logging
from datetime import datetime
from pathlib import Path


def init_step_logger(name_suffix: str = "",
                     with_date: bool = False,
                     log_level: int = logging.INFO) -> logging.Logger:
    """
    Initialize a logger for the current step script, inferred from caller file.

    Returns:
        A configured logger instance.
    """
    # Automatically extract step name from caller file name
    caller_path = Path(inspect.stack()[1].filename).resolve()
    step_name = caller_path.stem.split("_")[0]  # "step03"

    if name_suffix:
        step_name += f"_{name_suffix}"

    # Automatically create log directory
    project_root = caller_path.parent  # NOTE: Generally we are in 1.NER/stepXX.py
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    if with_date:
        today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
        log_file = log_dir / f"{step_name}_{today}.log"
    else:
        log_file = log_dir / f"{step_name}.log"

    logger = logging.getLogger(step_name)
    logger.setLevel(log_level)

    if not logger.handlers:
        fh = logging.FileHandler(log_file)
        sh = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(sh)

    return logger


def get_logger(name: str,
               log_dir: Path|None = None,
               log_level: int = logging.INFO,
               with_date: bool = False) -> logging.Logger:
    """
    Create a logger with a specific name and configuration.

    Args:
        name: logger name, will also be used as filename.
        log_dir: where to store log files (e.g. NER_DIR / "logs")
        log_level: logging level
        with_date: if True, log file name will include current date

    Returns:
        A configured logger instance.
    """
    if log_dir is None:
        caller_path = Path(inspect.stack()[1].filename).resolve()
        log_dir = caller_path.parent / "logs"

    if with_date:
        today = datetime.today().strftime("%Y-%m-%d")
        log_file = log_dir / f"{name}_{today}.log"
    else:
        log_file = log_dir / f"{name}.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

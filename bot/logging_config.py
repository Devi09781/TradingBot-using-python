import os
import logging
from datetime import datetime

def setup_logging(logger_name: str = "FuturesBot") -> logging.Logger:
    """
    Configures and returns a structured logger with dual-routing capabilities:
    - INFO level and above streams live to the terminal console.
    - DEBUG level and above writes into daily rotated-style log files.
    """
    # 1. Create a dedicated directory for log outputs
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate log filename dynamically based on current date
    log_filename = os.path.join(log_dir, f"binance_futures_{datetime.now().strftime('%Y%m%d')}.log")

    # 2. Define a clean, uniform layout format
    # Alignment formatting ensures severity columns stay uniformly spaced
    log_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 3. File Handler Setup (The exhaustive data vault)
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)  # Captures full internal tracking and responses

    # 4. Console Handler Setup (The clean terminal layout)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)  # Shields terminal from noisy JSON payloads

    # 5. Core Logger Architecture
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # Root baseline catch-all level

    # Prevent duplicate handlers from stacking if function is invoked multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    # Standard configuration verification test
    test_logger = setup_logging("LoggerTest")
    test_logger.debug("This is a DEBUG message (Will only show up in the log file).")
    test_logger.info("This is an INFO message (Visible on both terminal and file).")
    test_logger.warning("This is a WARNING alert.")
    print("\n[Verification Complete]: Check the created './logs/' folder to review file behavior.")
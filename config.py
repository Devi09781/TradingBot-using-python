import os
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------------
# 1. BASE DIRECTORY SETTINGS
# --------------------------------------------------------
# Automatically detect project root directory
BASE_DIR = Path(__file__).resolve().parent

# Load local system environment configuration file (.env)
load_dotenv(dotenv_path=BASE_DIR / ".env")

# --------------------------------------------------------
# 2. BINANCE NETWORK CONFIGURATIONS
# --------------------------------------------------------
# Active endpoints pointed directly to official Binance USDT-M Testnet
BINANCE_TESTNET_BASE_URL = "https://demo-fapi.binance.com"
BINANCE_TESTNET_WSS_URL = "wss://fstream.binancefuture.com"

# API authentication parameters extracted safely from operational system layers
API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY")

# --------------------------------------------------------
# 3. DIRECTORY & LOGGING ROUTE CONFIGURATIONS
# --------------------------------------------------------
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)  # Instantly ensure physical existence

# --------------------------------------------------------
# 4. SAFETY APPLICATION CONSTRAINTS
# --------------------------------------------------------
# Universal protective thresholds to minimize systemic financial risk exposure
MAX_ORDER_RETRY_ATTEMPTS = 3
DEFAULT_NOTIONAL_MINIMUM = 5.0  # Safe proxy buffer limit for USDT pairs

# --------------------------------------------------------
# 5. CREDENTIAL STRUCTURAL INTEGRITY VERIFICATION
# --------------------------------------------------------
def validate_config():
    """
    Validates structural presence of necessary keys inside runtime layers
    before initiating socket calls or sending downstream transaction blocks.
    """
    missing_variables = []
    
    if not API_KEY:
        missing_variables.append("BINANCE_TESTNET_API_KEY")
    if not SECRET_KEY:
        missing_variables.append("BINANCE_TESTNET_SECRET_KEY")
        
    if missing_variables:
        raise ImportError(
            f"Initialization terminated: Essential configuration missing fields: {missing_variables}. "
            f"Please verify their layout structure matches parameters inside your project local .env file."
        )

# Execute verification process implicitly on package invocation sequence
validate_config()

if __name__ == "__main__":
    # Local sandboxed print validations confirmation
    print("=" * 50)
    print("    CONFIG ARCHITECTURE LAYER DIAGNOSTIC RUN    ")
    print("=" * 50)
    print(f"Project Home Directory Route  : {BASE_DIR}")
    print(f"Project Active Logs Directory : {LOG_DIR}")
    print(f"Target Exchange Base Gateway  : {BINANCE_TESTNET_BASE_URL}")
    print(f"Target Credentials Check Status: PASSED (Keys are loaded effectively)")
    print("=" * 50)
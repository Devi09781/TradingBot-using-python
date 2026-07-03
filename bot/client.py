import os
import logging
import time
from dotenv import load_dotenv

# Setup a dedicated logger for the client initialization
logger = logging.getLogger("FuturesBot.Client")

class MockUMFutures:
    """
    A local simulation class that mimics the official binance.um_futures.UMFutures client.
    Requires zero API keys and never hits the network.
    """
    def __init__(self, key=None, secret=None, base_url=None):
        logger.info("🤖 SYSTEM: Running in Mock Simulation Mode. No network requests will be made.")

    def time(self) -> dict:
        """Simulates server time response."""
        return {"serverTime": int(time.time() * 1000)}

    def exchange_info(self) -> dict:
        """
        Simulates the trading rules, precision steps, and limits for 
        major pairs (BTCUSDT and ETHUSDT).
        """
        return {
            "symbols": [
                {
                    "symbol": "BTCUSDT",
                    "pricePrecision": 2,
                    "quantityPrecision": 3,
                    "filters": [
                        {"filterType": "PRICE_FILTER", "tickSize": "0.01"},
                        {"filterType": "LOT_SIZE", "minQty": "0.001", "stepSize": "0.001"},
                        {"filterType": "MIN_NOTIONAL", "notional": "5.0"}
                    ]
                },
                {
                    "symbol": "ETHUSDT",
                    "pricePrecision": 2,
                    "quantityPrecision": 2,
                    "filters": [
                        {"filterType": "PRICE_FILTER", "tickSize": "0.01"},
                        {"filterType": "LOT_SIZE", "minQty": "0.01", "stepSize": "0.01"},
                        {"filterType": "MIN_NOTIONAL", "notional": "5.0"}
                    ]
                }
            ]
        }

    def new_order(self, **kwargs) -> dict:
        """
        Simulates a successful order execution payload matching 
        the exact format returned by Binance.
        """
        return {
            "orderId": 987654321,
            "symbol": kwargs.get("symbol"),
            "side": kwargs.get("side"),
            "type": kwargs.get("type"),
            "status": "FILLED",
            "executedQty": kwargs.get("quantity"),
            "avgPrice": kwargs.get("price", "95000.00"),
            "updateTime": int(time.time() * 1000)
        }

def get_binance_client() -> MockUMFutures:
    """
    Initializes and returns the simulated client context wrapper.
    """
    try:
        logger.debug("Initializing Mock Binance Futures client...")
        client = MockUMFutures()
        
        # Test connectivity mock verification
        server_time = client.time()
        logger.info(f"Mock client successfully synchronized. Local Server Time: {server_time.get('serverTime')}")
        
        return client

    except Exception as e:
        logger.exception(f"Failed to establish mock workspace: {e}")
        raise e

if __name__ == "__main__":
    # Quick standalone functional check
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    print("Testing client initialization...")
    try:
        test_client = get_binance_client()
        print("Success! Mock client simulation is functional.")
        print(f"Sample exchange_info lookup keys: {test_client.exchange_info().keys()}")
    except Exception as err:
        print(f"Test failed: {err}")
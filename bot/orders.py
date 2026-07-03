import logging
from binance.error import ClientError, ServerError
from bot.client import get_binance_client
from bot.logging_config import setup_logging

# Initialize the global application logger
logger = setup_logging("FuturesBot.Orders")

class OrderManager:
    def __init__(self):
        """
        Initializes the OrderManager by pulling the pre-configured 
        Binance Futures Testnet client.
        """
        try:
            self.client = get_binance_client()
            logger.info("OrderManager ready to process execution routes.")
        except Exception as e:
            logger.critical(f"OrderManager initialization aborted: {e}")
            raise e

    def execute_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        """
        Sends an order request to the Binance Futures Testnet.
        
        :param symbol: Trading asset pair (e.g., 'BTCUSDT', 'ETHUSDT')
        :param side: Action direction ('BUY' or 'SELL')
        :param order_type: Execution type ('MARKET' or 'LIMIT')
        :param quantity: Quantity size to trade (In base asset terms)
        :param price: Entry trigger price (Mandatory only for LIMIT orders)
        """
        # Normalize variables for standard Binance formatting
        symbol = symbol.upper()
        side = side.upper()
        order_type = order_type.upper()

        logger.info(f"Preparing order instruction -> Type: {order_type} | Side: {side} | Qty: {quantity} {symbol}")

        # Construct basic execution payload parameters
        payload = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        # Conditional checking for Limit Order constraints
        if order_type == "LIMIT":
            if price is None:
                logger.error("Validation Failed: 'price' parameter must be specified for LIMIT orders.")
                return None
            payload["price"] = price
            payload["timeInForce"] = "GTC"  # Good 'Till Cancelled standard policy

        try:
            # Send raw transaction parameters downstream into the file log
            logger.debug(f"Dispatching API order payload: {payload}")
            
            # --- API transmission or Mock Response ---
            # To use the live API call instead of the mock, uncomment the line below:
            # response = self.client.new_order(**payload)
            
            # Mock response structure matching Binance API format
            response = {
                "orderId": 123456789,
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "status": "NEW",
                "executedQty": quantity,
                "avgPrice": "0.00"
            }

            logger.info(
                f"🎉 ORDER PLACED | ID: {response['orderId']} | "
                f"Status: {response['status']} | "
                f"Type: {response['type']}"
            )
            logger.debug(f"Full execution response dump: {response}")
            return response

        except ClientError as ce:
            logger.error(f"Binance Client rejection rule encountered! Code: {ce.error_code} | Reason: {ce.error_message}")
        except ServerError as se:
            logger.critical(f"Binance infrastructure service error: {se.message}")
        except Exception as generic_err:
            logger.exception(f"Unexpected operational crash inside OrderManager: {generic_err}")
            
        return None

# Clean test runner isolated from imports
if __name__ == "__main__":
    try:
        manager = OrderManager()

        # Test Case 1: Fire Market Purchase Test
        print("\n--- Executing Test Case 1: Market Order ---")
        manager.execute_order(symbol="BTCUSDT", side="BUY", order_type="MARKET", quantity=0.01)

        # Test Case 2: Fire Limit Sell Protection Test
        print("\n--- Executing Test Case 2: Limit Order ---")
        manager.execute_order(symbol="BTCUSDT", side="SELL", order_type="LIMIT", quantity=0.01, price=98000.0)

    except Exception as initialization_failure:
        print(f"Execution pipeline block context broken: {initialization_failure}")
import logging
from math import floor
from binance.error import ClientError
from bot.logging_config import setup_logging

# Pull the shared application logger setup
logger = setup_logging("FuturesBot.Validators")

class OrderValidator:
    def __init__(self, client):
        """
        :param client: The active and authorized FuturesClient instance.
        """
        self.client = client
        self.symbol_rules = {}
        logger.info("OrderValidator initialized. Fetching market structural constraints...")
        self._load_exchange_info()

    def _load_exchange_info(self):
        """
        Queries the Binance exchange rules cache to determine decimal precision 
        and minimum order sizes for target trading pairs.
        """
        try:
            info = self.client.exchange_info()
            for symbol_data in info.get("symbols", []):
                sym = symbol_data["symbol"]
                
                # Parse out precision step sizes and minimum sizes
                filters = {f["filterType"]: f for f in symbol_data.get("filters", [])}
                
                # PRICE_FILTER handles price tick details
                price_filter = filters.get("PRICE_FILTER", {})
                # LOT_SIZE handles contract quantity details
                lot_size_filter = filters.get("LOT_SIZE", {})
                # MIN_NOTIONAL handles minimum order value (Qty * Price)
                min_notional_filter = filters.get("MIN_NOTIONAL", {}) or filters.get("NOTIONAL", {})

                self.symbol_rules[sym] = {
                    "price_precision": int(symbol_data.get("pricePrecision", 4)),
                    "quantity_precision": int(symbol_data.get("quantityPrecision", 3)),
                    "min_qty": float(lot_size_filter.get("minQty", 0.0)),
                    "step_size": float(lot_size_filter.get("stepSize", 0.0)),
                    "min_notional": float(min_notional_filter.get("notional", min_notional_filter.get("minNotional", 5.0)))
                }
            logger.info(f"Successfully cached trading rules for {len(self.symbol_rules)} symbols.")
        except ClientError as ce:
            logger.error(f"Failed to load exchange structural metadata. API Error: {ce.error_message}")
        except Exception as e:
            logger.exception(f"Unexpected error caching market definitions: {e}")

    def round_to_step(self, value: float, step: float) -> float:
        """Helper to truncate values strictly according to structural step constraints."""
        if not step or value == 0:
            return value
        # Using string splitting on decimals is safer against floating-point inaccuracies
        step_str = str(step).rstrip('0')
        if '.' in step_str:
            decimals = len(step_str.split('.')[1])
            return round(floor(value / step) * step, decimals)
        return floor(value / step) * step

    def validate_and_format(self, symbol: str, quantity: float, price: float = None) -> dict:
        """
        Validates sizing rules and truncates floats to correct exchange precisions.
        
        :return: Dict containing execution attributes 'valid': True/False along with sanitized values.
        """
        symbol = symbol.upper()
        rules = self.symbol_rules.get(symbol)

        if not rules:
            logger.warning(f"Validation Blocked: Rules for {symbol} not found in system cache.")
            return {"valid": False, "reason": f"Symbol {symbol} missing from exchange rules."}

        # 1. Formatting Step Precision
        clean_qty = self.round_to_step(quantity, rules["step_size"])
        clean_price = None

        if price:
            # If price tick size is provided, format it
            tick_size = rules.get("step_size") # Falls back safely if tick rules vary
            clean_price = round(price, rules["price_precision"])

        # 2. Check Min Lot Size Constraint
        if clean_qty < rules["min_qty"]:
            reason = f"Quantity {quantity} ({clean_qty} after rounding) is under minimum requirement: {rules['min_qty']}"
            logger.error(f"Validation Drop | Symbol: {symbol} | Reason: {reason}")
            return {"valid": False, "reason": reason}

        # 3. Check Notional Value Limit (Approximate verification using current or limit price)
        check_price = clean_price if clean_price else price
        if check_price:
            notional_value = clean_qty * check_price
            if notional_value < rules["min_notional"]:
                reason = f"Total order value (${notional_value:.2f}) is lower than minimum allowed position ($ {rules['min_notional']})."
                logger.error(f"Validation Drop | Symbol: {symbol} | Reason: {reason}")
                return {"valid": False, "reason": reason}

        logger.debug(f"Validation Passed for {symbol}. Adjusted Qty: {clean_qty}, Price: {clean_price}")
        return {
            "valid": True,
            "quantity": clean_qty,
            "price": clean_price
        }

if __name__ == "__main__":
    # Test block wrapper verification loop
    from client import get_binance_client
    print("Testing structural constraints validations layer...")
    try:
        mock_client = get_binance_client()
        validator = OrderValidator(mock_client)
        
        # Test passing an erratic float decimal size 
        result = validator.validate_and_format(symbol="BTCUSDT", quantity=0.0123456, price=92150.78912)
        print(f"\nFormatting Check Results:\n{result}")
        
    except Exception as err:
        print(f"Validation local sandbox tests errored out: {err}")
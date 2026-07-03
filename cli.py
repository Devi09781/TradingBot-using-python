import sys
from bot.orders import OrderManager
from bot.validators import OrderValidator
from bot.logging_config import setup_logging

# Initialize main application logging context
logger = setup_logging("FuturesBot.CLI")

def run_cli():
    logger.info("Initializing Interactive Futures Trading CLI Environment...")
    print("=" * 60)
    print("          BINANCE FUTURES TESTNET (USDT-M) CLI BOT          ")
    print("=" * 60)

    try:
        # Initialize operations managers
        manager = OrderManager()
        validator = OrderValidator(manager.client)
    except Exception as init_err:
        logger.critical(f"Failed to boot secure trading resources: {init_err}")
        print(f"\n[CRITICAL ERROR]: Could not initialize bot. Check logs for details. ({init_err})")
        sys.exit(1)

    print("\nInitialization successful. Type 'exit' at any prompt to close.")
    
    while True:
        print("\n" + "-" * 40)
        try:
            # 1. Capture Symbol Input
            symbol = input("Enter Symbol (e.g., BTCUSDT): ").strip().upper()
            if symbol == 'EXIT': break
            if not symbol: continue

            # 2. Capture Direction Side Input
            side = input("Enter Side (BUY / SELL): ").strip().upper()
            if side == 'EXIT': break
            if side not in ['BUY', 'SELL']:
                print("[!] Invalid entry. Side must be either BUY or SELL.")
                continue

            # 3. Capture Execution Type Input
            order_type = input("Enter Order Type (MARKET / LIMIT): ").strip().upper()
            if order_type == 'EXIT': break
            if order_type not in ['MARKET', 'LIMIT']:
                print("[!] Invalid entry. Type must be either MARKET or LIMIT.")
                continue

            # 4. Capture Quantity Input
            qty_input = input(f"Enter target quantity size for {symbol}: ").strip()
            if qty_input.upper() == 'EXIT': break
            try:
                quantity = float(qty_input)
            except ValueError:
                print("[!] Invalid number. Please enter a valid decimal for quantity.")
                continue

            # 5. Capture Price Input Conditional on Limit order requirements
            price = None
            if order_type == "LIMIT":
                price_input = input(f"Enter target entry limit price for {symbol}: ").strip()
                if price_input.upper() == 'EXIT': break
                try:
                    price = float(price_input)
                except ValueError:
                    print("[!] Invalid number. Please enter a valid decimal for price.")
                    continue

            # 6. Execute Pre-flight Guardrail Validation
            print(f"\n[*] Running strict exchange constraint validation parameters for {symbol}...")
            validation_result = validator.validate_and_format(symbol, quantity, price)

            if not validation_result["valid"]:
                print(f"❌ Validation Rejected! Reason: {validation_result['reason']}")
                continue

            # Extracted clean parameters adjusted exactly to exchange specifications
            sanitized_qty = validation_result["quantity"]
            sanitized_price = validation_result["price"]

            # Double-check confirmation step to avoid fat-finger mistakes
            confirm_msg = f"Confirm execution? {order_type} {side} {sanitized_qty} {symbol}"
            if sanitized_price:
                confirm_msg += f" @ ${sanitized_price}"
            
            confirm = input(f"{confirm_msg} (y/n): ").strip().lower()
            if confirm != 'y':
                logger.info("Order execution canceled by human operator input.")
                print("Order cancelled.")
                continue

            # 7. Discharging Safe Validated Trade Downstream
            print("[*] Broadcasting order parameters to Binance network...")
            response = manager.execute_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=sanitized_qty,
                price=sanitized_price
            )

            if response:
                print(f"\n🎉 SUCCESS! Order accepted by Testnet.")
                print(f"   Order ID: {response.get('orderId')} | Status: {response.get('status')}")
            else:
                print("\n❌ FAILED! Exchange rejected transaction layout. Verify details in file logs.")

        except KeyboardInterrupt:
            # Handle Ctrl+C interruptions cleanly
            print("\n\nExiting application session sequence...")
            break
        except Exception as runtime_error:
            logger.exception(f"Fatal application loop crash context: {runtime_error}")
            print(f"\n[CRITICAL]: Operational Exception: {runtime_error}")

    print("\n============================================================")
    print("  CLI Engine shutdown complete. Review logfiles for logs.   ")
    print("============================================================")

if __name__ == "__main__":
    run_cli()
```markdown
# Binance Futures CLI Trading Bot

##  Overview

This project is a Python command-line application that simulates placing **Market** and **Limit** orders for Binance USDT-M Futures. The project focuses on clean project architecture, command-line input handling, validation, logging, and exception handling.

> **Note:** This project currently runs in **mock mode** and does not connect to the Binance Futures Testnet. API integration can be added in the future.

---

## ✨ Features

- Simulated Market Orders
- Simulated Limit Orders
- BUY and SELL order support
- Command-Line Interface (CLI)
- Input Validation
- Modular Project Structure
- Logging of Requests and Responses
- Exception Handling

---

## 📂 Project Structure

```

trading_bot/
│
├── bot/
│   ├── **init**.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
│
├── cli.py
├── config.py
├── README.md
├── requirements.txt
└── logs/

````

---

## ⚙️ Requirements

- Python 3.x

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/trading_bot.git
cd trading_bot
````

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Limit Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 98000
```

---

## 📝 Logging

The application stores logs inside the `logs/` directory, including:

* Order Requests
* Simulated Responses
* Validation Errors
* Runtime Exceptions

---

## 🛠 Technologies Used

* Python 3
* argparse
* logging
* python-dotenv

---

## 🔮 Future Enhancements

* Binance Futures Testnet API Integration
* Real Market & Limit Order Placement
* Unit Testing
* Configuration Management
* Docker Support

---

## 📄 License

This project is developed for educational and learning purposes.

```
```

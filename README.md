# Binance Futures CLI Trading Bot

##  Overview

This project is a Python command-line application that simulates placing **Market** and **Limit** orders for **Binance USDT-M Futures**. It demonstrates a clean, modular project structure with command-line input handling, input validation, logging, and exception handling.

> **Note:** This project currently runs in **mock mode** and simulates order placement without connecting to the Binance Futures Testnet.

---

##  Features

* Simulated **Market Orders**
* Simulated **Limit Orders**
* Supports **BUY** and **SELL** order types
* Command-Line Interface (CLI)
* Input Validation
* Modular Project Structure
* Logging of Requests and Responses
* Exception Handling

---

## 📂 Project Structure

```text
trading_bot/
│
├── bot/
│   ├── __init__.py
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
```

---

## ⚙️ Requirements

* Python 3.x
* pip

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/trading_bot.git
cd trading_bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 4. Install the dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Place a Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a Limit Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 98000
```

---

## 📝 Logging

The application stores logs in the **logs/** directory, including:

* Order requests
* Simulated order responses
* Validation errors
* Runtime exceptions

---

## 🛠️ Technologies Used

* Python 3
* argparse
* logging
* python-dotenv

---

## 🔮 Future Improvements

* Integrate with the Binance Futures Testnet API
* Add API Key and Secret authentication
* Place real Market and Limit orders
* Support additional order types
* Add unit tests
* Improve configuration management

---

## 📄 License

This project is created for educational and learning purposes.

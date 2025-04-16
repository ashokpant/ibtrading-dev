# Trading View Webhook API

## Dependencies

Install requirements

```bash
pip install -r requirements.txt
```

Install TA-Lib

```bash
# https://ta-lib.org
wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib_0.6.4_amd64.deb
sudo dpkg -i ta-lib_0.6.4_amd64.deb
pip install TA-Lib
```

# Install vnpy

```bash
pip install vnpy
```

## Install IBKR API Gateway

https://www.interactivebrokers.com/en/trading/ibgateway-stable.php

## Install IBKR API

https://interactivebrokers.github.io/#
https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#unix-install

```bash
wget https://interactivebrokers.github.io/downloads/twsapi_macunix.1034.02.zip
sudo unzip twsapi_macunix.1034.02.zip $HOME
cd IBJts
sudo chmod -R 777 source/pythonclient
cd source/pythonclient
python -m pip install
```

## Running the server

```bash
cd tvwebhook
python main.py

```

## Webhook Setup

Request payload

```json
 {
  "action": "{{strategy.order.action}}",
  "contracts": "{{strategy.order.contracts}}",
  "symbol": "{{ticker}}",
  "position_size": "{{strategy.position_size}}",
  "market_position": "{{strategy.market_position}}",
  "market_position_size": "{{strategy.market_position_size}}",
  "time": "{{time}}",
  "close": "{{close}}",
  "open": "{{open}}",
  "high": "{{high}}",
  "low": "{{low}}",
  "volume": "{{volume}}",
  "timeframe": "{{interval}}",
  "exchange": "{{exchange}}",
  "timenow": "{{timenow}}",
  "currency": "{{syminfo.currency}}",
  "sec_type": "FUT",
  "last_trade_date_or_contract_month": "20241220",
  "message": "{{strategy.order.alert_message}} "
}
```

Webhook endpoint

```text
[POST] {{API_HOST]]/api/v1/webhook/{{API_KEY}}
```

# Cryptocurrency TWAP Calculator

A simple tool to calculate Time-Weighted Average Price (TWAP) for cryptocurrencies using CoinGecko API.

## Description

This tool fetches OHLC (Open, High, Low, Close) data for a specified cryptocurrency and calculates the TWAP over a given period.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.7+**: Required to run the application
- **pipenv**: Python package and virtual environment manager
- **make**: Required to run the provided Makefile commands
- **git**: For cloning the repository (if not downloaded directly)

## Installation 

To install the necessary dependencies:

```bash
    make setup
```
This will create a virtual environment using pipenv and install all required packages.

If you're using VS Code, you can set up the environment integration with:

```bash
    make vscode-setup
```

## Usage

Basic usage:

```bash
    make run COIN=xxx
```

With custom parameters:
```bash
    make run COIN=xxx CURRENCY=yyy DAYS=14
```

To log a run with description:
```bash
    make log-run COIN=xxx DESC="A xxx analysis for report"
```

## Past Runs

| Description | Timestamp | Output |
|-------------|-----------|--------|
| Example test run | 2025-02-26 15:29:32 | TWAP for ethereum in usd over 7 days: 2672.494642857143 |
| Example test run | 2025-02-26 15:32:51 | TWAP for bitcoin in usd over 7 days: 94877.29761904762 |


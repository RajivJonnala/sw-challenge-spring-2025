# Cardinal Trading Spring 25 Deliverable

## Overview
This data processing interface loads, cleans, and aggregates market trade data from CSV files. The program reads raw trade data, filters out invalid or duplicate records, and then aggregates the data into OHLCV (Open, High, Low, Close, Volume) bars based on a specified time interval.

## Features
- Loads trade data from CSV files in a specified directory.
- Cleans data by removing duplicates, filtering invalid entries, and ensuring trades occur within trading hours.
- Aggregates the cleaned data into OHLCV bars using customizable time intervals.
- Exports the aggregated data to a CSV file.

## Requirements
- Python 3.12.9

## Installation
Ensure you have [Python 3.12.9](https://www.python.org/downloads/). and the packages namely, os, csv, datetime and re will be preinstalled.

## Usage
### 1. Prepare Your Data
Place your trade data CSV files inside a directory (e.g., `data/`). The files should contain the following columns:
- `Timestamp` (format: `YYYY-MM-DD HH:MM:SS.sss`)
- `Price` (float)
- `Size` (integer)

### 2. Running the Program
Modify the script parameters as needed and execute the script:
```sh
python script.py
```

### 3. Configuring Time Intervals
The aggregation interval is defined using a string format:
- `1s` -> 1 second
- `1m` -> 1 minute
- `5m` -> 5 minutes
- `1h` -> 1 hour
- `1d` -> 1 day

Modify the interval in the script:
```python
interval = "1m"  # Set aggregation interval
start = "2024-09-16 09:30:00"
end = "2024-09-16 16:00:00"
output = "ohlcv_1m.csv"
```

### 4. Output File
The program generates an output CSV file containing OHLCV data with the following structure:
- `Timestamp`
- `Open`
- `High`
- `Low`
- `Close`
- `Volume`

## Data Cleaning Report
### Issues Identified
1. **Missing Values:**
   - Rows with missing timestamps, prices, or sizes are removed.
2. **Incorrect Data Types:**
   - Non-numeric values in price or size columns are ignored.
3. **Negative or Zero Values:**
   - Trades with price or size <= 0 are discarded.
4. **Duplicates:**
   - Entries with the same timestamp, price, and size are removed.
5. **Trading Hours:**
   - Only trades between 09:30 and 16:00 are considered.

## Assumptions & Limitations
- Data files must be in CSV format with correctly named columns.
- The program assumes timestamps are in `YYYY-MM-DD HH:MM:SS.sss` format.
- Aggregation is performed based on time-based bins and does not include custom logic for tick-based aggregation.
- The system works only within regular trading hours (09:30 - 14:00).

## **Data Cleaning Report**  

The data cleaning process was designed to ensure data integrity, accuracy, and consistency before aggregation into OHLCV bars. Several key issues were identified and addressed systematically. First, records with missing values in essential fields (`Timestamp`, `Price`, or `Size`) were discarded, as incomplete data could lead to inaccurate analysis. Next, strict type conversion was applied to enforce correct data formats; timestamps were parsed into proper datetime objects, `Price` values were converted to floats, and `Size` values to integers. Any records failing these conversions were removed. Additionally, non-positive trade values (i.e., `Price ≤ 0` or `Size ≤ 0`) were eliminated to prevent invalid calculations from affecting market analysis.  

Duplicate trades, identified using a unique combination of `(timestamp, price, size)`, were also removed to avoid over-representation of certain transactions. Another critical step involved filtering out trades occurring outside regular market hours (09:30 - 16:00), ensuring that only relevant market activity was considered. These anomalies were detected using predefined criteria, including format validation, numerical range checks, duplicate identification, and timestamp filtering based on exchange hours.  

The rationale behind these cleaning decisions was to enhance the dataset’s reliability and usability for financial analysis. Removing incomplete and erroneous data ensured consistency, while filtering out anomalies prevented distortions in price and volume trends. By enforcing trading hour restrictions, the dataset remained aligned with standard market operations, making it suitable for meaningful OHLCV aggregation and further analysis. These steps collectively contributed to a cleaner, more robust dataset that accurately reflects intraday market activity.

## Author
Rajiv Jonnala




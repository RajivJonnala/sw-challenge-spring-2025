import os
import csv
import datetime
import re

class DataLoader:
    def __init__(self, data_directory):
        self.data_directory = data_directory

    def load_data(self):
        data = []
        for file_name in sorted(os.listdir(self.data_directory)):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.data_directory, file_name)
                
                with open(file_path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        data.append(row)

            
        return data

class DataCleaner:
    def __init__(self):
        pass

    def clean_data(self, data):
        cleaned_data = []
        seen = set()  # To track duplicates based on (timestamp, price, size)
        
        for row in data:
            #Check for missing values.
            if not row.get('Timestamp') or not row.get('Price') or not row.get('Size'):
                continue

            # Convert timestamp string to datetime.
            try:
                timestamp = datetime.datetime.strptime(row['Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                price = float(row['Price'])
                size = int(row['Size'])
            except Exception as e:
                continue

            # Check for non-positive prices or sizes.
            if price <= 0 or size <= 0:
                continue

            # Remove duplicate entries.
            row_key = (timestamp, price, size)
            if row_key in seen:
                continue
            seen.add(row_key)

            # Filter out trades outside of regular trading hours.
            if not self._is_within_trading_hours(timestamp):
                continue

            cleaned_data.append({
                'Timestamp': timestamp,
                'Price': price,
                'Size': size
            })

        # Sort data by timestamp
        cleaned_data.sort(key=lambda x: x['Timestamp'])
        return cleaned_data

    def _is_within_trading_hours(self, timestamp):
        market_open = datetime.time(9, 30)
        market_close = datetime.time(16, 0)
        current_time = timestamp.time()
        return market_open <= current_time <= market_close


class DataAggregator:
    def __init__(self, cleaned_data):
        self.cleaned_data = cleaned_data

    def parse_interval(self, interval_str):
        pattern = re.compile(r"(\d+)([dhms])")
        matches = pattern.findall(interval_str)

        total_seconds = 0
        for value, unit in matches:
            value = int(value)
            if unit == 'd':
                total_seconds += value * 86400
            elif unit == 'h':
                total_seconds += value * 3600
            elif unit == 'm':
                total_seconds += value * 60
            elif unit == 's':
                total_seconds += value
        return datetime.timedelta(seconds=total_seconds)

    def aggregate(self, interval_str, start_dt, end_dt):
        interval = self.parse_interval(interval_str)
        current_bin_start = start_dt
        aggregated_bars = []
        current_bin_ticks = []

        # Iterate through all ticks in the cleaned data.
        for tick in self.cleaned_data:
            t = tick['Timestamp']
            if t < start_dt or t >= end_dt:
                continue

            while t >= current_bin_start + interval:
                if current_bin_ticks:
                    bar = self.compute_bar(current_bin_start, current_bin_ticks)
                    aggregated_bars.append(bar)
                    current_bin_ticks = []
                current_bin_start += interval

            current_bin_ticks.append(tick)

        # Flush the last bin if there are any remaining ticks.
        if current_bin_ticks:
            bar = self.compute_bar(current_bin_start, current_bin_ticks)
            aggregated_bars.append(bar)
        return aggregated_bars

    def compute_bar(self, bin_start, ticks):
        open_price = ticks[0]['Price']
        close_price = ticks[-1]['Price']
        high_price = max(t['Price'] for t in ticks)
        low_price = min(t['Price'] for t in ticks)
        volume = sum(t['Size'] for t in ticks)
        return {
            'Timestamp': bin_start,
            'Open': open_price,
            'High': high_price,
            'Low': low_price,
            'Close': close_price,
            'Volume': volume
        }


class DataInterface:
    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.data_loader = DataLoader(data_directory)
        self.data_cleaner = DataCleaner()
        self.data = None

    def load_and_clean_data(self):
        raw_data = self.data_loader.load_data()
        self.data = self.data_cleaner.clean_data(raw_data)
        #print((len(self.data)/len(raw_data)))
        #print(len(self.data))
        #print(len(raw_data))
    def generate_ohlcv(self, interval_str, start_str, end_str, output_file):
        
        start_dt = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")

        aggregator = DataAggregator(self.data)
        bars = aggregator.aggregate(interval_str, start_dt, end_dt)


        self.write_output(bars, output_file)

    def write_output(self, bars, output_file):
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            for bar in bars:
                ts_str = bar['Timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([ts_str, bar['Open'], bar['High'], bar['Low'], bar['Close'], bar['Volume']])


if __name__ == '__main__':
    data_dir = "data"
    
    interface = DataInterface(data_directory=data_dir)
    
    interface.load_and_clean_data()
    
    interval = "1m" 
    start = "2024-09-16 09:30:00"
    end = "2024-09-16 16:00:00"
    output = "ohlcv_1m.csv"
    
    interface.generate_ohlcv(interval, start, end, output)

    interval = "2m" 
    start = "2024-09-16 09:30:00"
    end = "2024-09-16 10:00:00"
    output = "ohlcv_2m.csv"
    
    interface.generate_ohlcv(interval, start, end, output)

    interval = "1h" 
    start = "2024-09-16 09:30:00"
    end = "2024-09-16 16:00:00"
    output = "ohlcv_1h.csv"
    
    interface.generate_ohlcv(interval, start, end, output)

    interval = "3m" 
    start = "2024-09-16 09:30:00"
    end = "2024-09-16 16:00:00"
    output = "ohlcv_3m.csv"
    
    interface.generate_ohlcv(interval, start, end, output)

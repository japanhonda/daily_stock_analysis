import os
import logging
from sequoia_x import SequoiaX
import akshare as ak

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Sequoia-X configuration and data engine
sequoia = SequoiaX()

# Sync the latest stock data for all A-share stocks
logging.info("Syncing stock data...")
stocks_data = ak.stock_zh_a_spot()

# Define strategies
def run_strategies(stocks_data):
    results = []
    strategies = [
        'MaVolumeStrategy',
        'TurtleTradeStrategy',
        'HighTightFlagStrategy',
        'LimitUpShakeoutStrategy',
        'UptrendLimitDownStrategy',
        'RpsBreakoutStrategy'
    ]
    
    for strategy in strategies:
        logging.info(f"Running {strategy}...")
        # Here you would instantiate and run each strategy, appending results to results
        # Example: results.extend(strategy_instance.run(stocks_data))
        results.extend([])  # Replace with actual implementation
    return results

# Run all strategies
results = run_strategies(stocks_data)

# Merge results and remove duplicates
unique_results = list(set(results))

# Filter out ST stocks and suspended stocks
filtered_results = [stock for stock in unique_results if not stock['is_st'] and not stock['is_suspended'] and (stock['board'] in ['Mainboard', 'ChiNext'])]

# Load existing STOCK_LIST from .env
env_path = '.env'
stock_list = []
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('STOCK_LIST='):
                stock_list = line.split('=')[1].strip().split(',')

# Merge new results with existing STOCK_LIST and remove duplicates
updated_stock_list = list(set(filtered_results) | set(stock_list))
updated_stock_list = list(dict.fromkeys(updated_stock_list))  # Maintain order

# Update .env file
with open(env_path, 'w') as f:
    f.write('STOCK_LIST=' + ','.join(updated_stock_list) + '\n')

logging.info("Stock selection process completed.")

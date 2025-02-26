import json
import datetime
import argparse
import sys
import os
from pycoingecko import CoinGeckoAPI
import pandas as pd

# Constants
RUNS_FILE = "runs.json"
README_TEMPLATE = "README.template.md"
README_FILE = "README.md"

def load_run_history():
    """Load existing runs from JSON file or return empty list if file doesn't exist"""
    if os.path.exists(RUNS_FILE):
        with open(RUNS_FILE, 'r') as f:
            return json.load(f)
    return []

def update_readme_from_template():
    """Update README.md from template and runs data"""
    # Fail if template doesn't exist
    if not os.path.exists(README_TEMPLATE):
        raise FileNotFoundError(f"Required template file {README_TEMPLATE} not found")
    
    runs = load_run_history()
    
    # Read template
    with open(README_TEMPLATE, 'r') as f:
        template = f.read()
    
    # Generate runs table
    runs_table = "## Past Runs\n\n"
    runs_table += "| Description | Timestamp (UTC) | Output |\n"
    runs_table += "|-------------|----------------|--------|\n"
    
    for run in runs:
        # Format timestamp for readability
        timestamp = datetime.datetime.fromisoformat(run["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        
        # Clean any pipe characters that would break markdown table
        description = run["description"].replace("|", "\\|")
        output = run["output"].replace("|", "\\|")
        
        runs_table += f"| {description} | {timestamp} | {output} |\n"
    
    # Replace placeholder in template
    readme_content = template.replace("<!-- RUNS_TABLE -->", runs_table)
    
    # Write to README.md
    with open(README_FILE, 'w') as f:
        f.write(readme_content)

def log_run(description, output):
    """Log a run to the JSON file and update README"""
    runs = load_run_history()
    
    # Create new run entry
    run = {
        "description": description,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "output": output
    }
    
    # Add to runs and save
    runs.append(run)
    with open(RUNS_FILE, 'w') as f:
        json.dump(runs, f, indent=2)
    
    # Update README
    update_readme_from_template()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Get cryptocurrency OHLC data and calculate TWAP')
    parser.add_argument('coin_id', type=str, help='Cryptocurrency ID')
    parser.add_argument('--currency', type=str, default='usd', help='Currency to convert to (default: usd)')
    parser.add_argument('--days', type=int, default=7, help='Number of days of data to retrieve (default: 7)')
    parser.add_argument('--log', action='store_true', help='Log this run to history')
    parser.add_argument('--description', type=str, help='Description of this run (used with --log)')
    
    args = parser.parse_args()
    
    cg = CoinGeckoAPI()
    
    try:
        # Get data from CoinGecko
        trades = cg.get_coin_ohlc_by_id(args.coin_id, args.currency, args.days)
        
        # Process data
        if not trades or len(trades) == 0:
            print(f"No data returned for {args.coin_id}")
            sys.exit(1)
            
        df = pd.DataFrame(trades, columns=['time', 'open', 'high', 'low', 'close'])
        twap_price = df[['open', 'high', 'low', 'close']].mean(axis=None)
        
        output = f"TWAP for {args.coin_id} in {args.currency} over {args.days} days: {twap_price}"
        print(output)
        
        # Log run if requested
        if args.log:
            log_run(
                description=args.description or f"TWAP calculation for {args.coin_id}",
                output=output
            )
        
        return 0
        
    except ValueError as e:
        # Keep only the most specific error handling for user experience
        if "coin not found" in str(e).lower():
            print(f"Error: Coin ID '{args.coin_id}' not found.")
        else:
            print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
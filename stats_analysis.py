import json
import numpy as np
import pandas as pd
import argparse

def load_quotes(filepath):
    """Load quotes from JSON file and convert to a DataFrame with author and text columns."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert dictionary of lists to list of (author, quote) pairs
        quotes_list = []
        for author, quotes in data.items():
            for quote in quotes:
                quotes_list.append({'author': author, 'text': quote})
        
        return pd.DataFrame(quotes_list)
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def get_quote_length_stats(df):
    """Calculate statistics about quote lengths using NumPy."""
    if df is None or df.empty:
        return None
    
    # Calculate lengths of quotes
    quote_lengths = df['text'].str.len()
    
    stats = {
        'mean_length': np.mean(quote_lengths),
        'median_length': np.median(quote_lengths),
        'std_dev_length': np.std(quote_lengths),
        'min_length': np.min(quote_lengths),
        'max_length': np.max(quote_lengths)
    }
    
    return stats

def group_by_first_word(df):
    """Group quotes by their first word and calculate statistics."""
    if df is None or df.empty:
        return None
    
    # Extract first word from each quote
    df['first_word'] = df['text'].str.split().str[0]
    
    # Group by first word and calculate statistics
    grouped_stats = df.groupby('first_word').agg({
        'text': ['count', lambda x: np.mean([len(s) for s in x])],
        'author': 'count'
    }).round(2)
    
    # Rename columns for clarity
    grouped_stats.columns = ['quote_count', 'avg_quote_length', 'author_count']
    
    # Sort by quote count in descending order
    return grouped_stats.sort_values('quote_count', ascending=False)

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Analyze quote statistics from a JSON file.')
    parser.add_argument('filepath', help='Path to the JSON file containing quotes')
    args = parser.parse_args()
    
    # Load the data
    df = load_quotes(args.filepath)
    if df is None:
        return
    
    # Calculate quote length statistics
    length_stats = get_quote_length_stats(df)
    if length_stats:
        print("\nQuote Length Statistics:")
        for stat, value in length_stats.items():
            print(f"{stat.replace('_', ' ').title()}: {value:.2f}")
    
    # Group by first word and display statistics
    first_word_stats = group_by_first_word(df)
    if first_word_stats is not None:
        print("\nTop 10 First Words Statistics:")
        print(first_word_stats.head(10))

if __name__ == "__main__":
    main()

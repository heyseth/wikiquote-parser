import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

def plot_quote_length_histogram(df, save_path=None):
    """Create a histogram of quote lengths."""
    if df is None or df.empty:
        return
    
    quote_lengths = df['text'].str.len()
    
    plt.figure(figsize=(10, 6))
    plt.hist(quote_lengths, bins=30, edgecolor='black')
    plt.title('Distribution of Quote Lengths')
    plt.xlabel('Quote Length (characters)')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def plot_top_words_barchart(df, save_path=None):
    """Create a bar chart of most frequent first words in quotes."""
    if df is None or df.empty:
        return
    
    # Get first word counts
    first_words = df['text'].str.split().str[0].value_counts()
    top_words = first_words.head(10)
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(top_words)), top_words.values)
    plt.title('Top 10 Most Common First Words in Quotes')
    plt.xlabel('First Word')
    plt.ylabel('Frequency')
    plt.xticks(range(len(top_words)), top_words.index, rotation=45)
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def create_visualizations(filepath, save_plots=False):
    """Create all visualizations for the quotes data.
    
    Args:
        filepath (str): Path to the JSON file containing quotes
        save_plots (bool): If True, save plots to files. If False, display them.
    """
    df = load_quotes(filepath)
    
    if df is None:
        print("Error: Could not load data")
        return
    
    # Create output directory if saving plots
    if save_plots:
        import os
        os.makedirs('plots', exist_ok=True)
    
    # Generate visualizations
    plot_quote_length_histogram(
        df, 
        'plots/quote_lengths_histogram.png' if save_plots else None
    )
    
    plot_top_words_barchart(
        df,
        'plots/top_words_barchart.png' if save_plots else None
    )

if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Create visualizations from a quotes JSON file.')
    parser.add_argument('filepath', help='Path to the JSON file containing quotes')
    parser.add_argument('--save', action='store_true', help='Save plots to files instead of displaying them')
    args = parser.parse_args()
    
    # Create visualizations with provided arguments
    create_visualizations(args.filepath, save_plots=args.save)

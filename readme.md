# wikiquote-parser

There aren't many large, public datasets of quotes online, so I created my own by parsing and cleaning up a Wikiquote data dump.

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Download a data dump of wikiquote:

`wget https://dumps.wikimedia.org/enwikiquote/latest/enwikiquote-latest-pages-articles.xml.bz2`

Extract the archive:

`bzip2 -d enwikiquote-latest-pages-articles.xml.bz2`

Run the program:

`./parse_xml.py enwikiquote-latest-pages-articles.xml`

There are two optional parameters: quote cutoff length, and desired language. The default cutoff length is 100 characters, and the default language is English. The language must be specified as an [ISO Language Code](https://www.w3schools.com/tags/ref_language_codes.asp).

For instance, if you wanted quotes only in Spanish, and less than 50 characters in length, you would enter the following:

`./parse_xml.py enwikiquote-latest-pages-articles.xml 50 es`

Alternatively, if you don't want to specify a language, enter "all" (no quotes) for the language parameter. This will massively shorten the time it takes the program to run.

## Analysis Tools

The repository also includes two scripts for analyzing and visualizing the quote data:

### Statistical Analysis

Performs statistical analysis on the quotes using NumPy and Pandas:
- Calculates quote length statistics (mean, median, standard deviation)
- Groups quotes by first word and provides aggregated statistics
- Handles JSON files structured as `{"author": ["quote1", "quote2", ...], ...}`

Usage:

`./stats_analysis.py path/to/quotes.json`

### Data Visualization

Creates visualizations using Matplotlib:
- Generates and displays a histogram showing the distribution of quote lengths
- Generates and displays a bar chart of the top 10 most common first words

Usage:

`./visualize_quotes.py path/to/quotes.json`

## License

This project is licensed under the MIT License - see the license.md file for details.

## Acknowledgments
Huge thanks to:
* All the contributors to [Wikiquote](https://en.wikiquote.org/wiki/Main_Page), and the [Wikimedia Foundation](https://wikimediafoundation.org/wiki/Home).

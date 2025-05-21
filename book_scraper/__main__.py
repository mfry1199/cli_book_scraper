# book_scraper/__main__.py
from .cli import parse_args
from .scraper import scrape_books
from .df_filter import keyword_data_filter
from .sorter import sort_book_data


def main():
    """
    Main function: filters and/or sorts scraped book data based on CLI argument configurations,
    generates a summary, and exports processed data to CSV.
    """
    config = parse_args()
    book_data = scrape_books(config.pages)

    if config.filter:
        book_data = keyword_data_filter(book_data, config.filter)
    if config.sort:
        book_data = sort_book_data(book_data, config.sort, config.desc)
    if not config.filter and not config.sort:
        print('Data unsorted and unfiltered.')

    books_scraped = len(book_data)
    print(f'Books scraped: {books_scraped}')
    if books_scraped > 0:
        print(f'Filter using keyword(s): {config.filter if config.filter else None}.')
        print(
        f"Sorted in {'descending' if config.desc else 'ascending'} order based on {config.sort}"
        if config.sort else "Books unsorted.")
        print(book_data[['title', 'category']].head())
    
    output_file = "books.csv"
    book_data.to_csv(output_file, index=False)
    print(f"\nData exported to {output_file}")


if __name__=="__main__":
    main()
# book_scraper/cli.py
import argparse


def parse_args() -> argparse.Namespace:
    """
    Parses and returns user typed command-line arguments

    Returns:
        argparse.Namespace: User typed command-line arguments
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--sort', choices=['rating', 'price'], default=None, help='Optional argument to sort by specific data')
    parser.add_argument('--desc', dest='desc', action='store_true', help='Sort in descending order')
    parser.add_argument('--asc', dest='desc', action='store_false', help='Sort in ascending order')
    parser.set_defaults(desc=True)
    parser.add_argument('--filter', default=None, help='Optional argument for filtering data based on keywords')
    parser.add_argument('--pages', type=int, default=1, help='Optional argument for limiting number of pages scraped')

    return parser.parse_args()
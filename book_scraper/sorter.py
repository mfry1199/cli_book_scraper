# book_scraper/sorter.py
import pandas as pd
import re

def sort_book_data(book_data: pd.DataFrame, sort_option: str, desc: bool) -> pd.DataFrame:
    """
    Sorts book data in ascending or descending order by rating or price.

    Args:
        book_data (pd.DataFrame): Contains book data to be filtered.
        sort_option (str): Specifies what to sort dataframe by, rating or price.
        desc (bool): When true, sort order is descending. When false, sort order is ascending.

    Return:
        pandas.DataFrame: Sorted book data
    """
    if sort_option == 'rating':
        return sort_by_rating(book_data, desc)
    else:
        return sort_by_price(book_data, desc)
    


def sort_by_rating(book_data: pd.DataFrame, desc: bool) -> pd.DataFrame:
    """
    Sorts book data by rating in ascending or decending order.

    Args:
        book_data (pd.DataFrame): Book data to be filtered.
        desc (bool): When true, sort order is descending. When false, sort order is ascending.

    Return:
        book_data_sorted (pd.DataFrame): Book data sorted by rating.
    """
    book_data['temp_sort'] = pd.to_numeric(book_data['rating'], errors='coerce')

    if desc == True:
        book_data_sorted = book_data.sort_values(by='temp_sort', ascending=False, na_position='last')
    else:
        book_data_sorted = book_data.sort_values(by='temp_sort', ascending=True, na_position='last')
        
    book_data_sorted.drop(columns='temp_sort', inplace=True)

    return book_data_sorted


def sort_by_price(book_data: pd.DataFrame, desc: bool) -> pd.DataFrame:
    """
    Sorts book data by price in ascending or decending order.

    Args:
        book_data (pd.DataFrame): Book data to be filtered.
        desc (bool): When true, sort order is descending. When false, sort order is ascending.

    Return:
        book_data_sorted (pd.DataFrame): Book data sorted by price.
    """
    book_data['money_value'] = book_data['price'].apply(extract_money_value)
    
    if desc == True:
        book_data_sorted = book_data.sort_values(by='money_value', ascending=False)
    else:
        book_data_sorted = book_data.sort_values(by='money_value', ascending=True)

    book_data_sorted.drop(columns='money_value', inplace=True)

    return book_data_sorted


def extract_money_value(money_string: str) -> int:
    """
    Extracts integer value from currency string and multiplies by 1000 if 'k' suffix present.

    Args:
        money_string (str): Currency string of various formats.

    Return:
        value (int): Value of currency with any k suffix calculated in.
    """
    pattern = r'([\d,.]+(?:\.\d+)?)([kK]?)'

    match = re.search(pattern, money_string)

    if match:
        num, suffix = match.groups()

        num = num.replace(',', '')
        try:
            value = float(num)
            if suffix.lower() == 'k':
                value *= 1000
            return value
        except ValueError:
            return None
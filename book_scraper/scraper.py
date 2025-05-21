# book_scraper/scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://books.toscrape.com/'
CATALOGUE_URL = BASE_URL + 'catalogue/'

def scrape_books(pages_requested: int) -> pd.DataFrame:
    """
    Scrapes and returns requested number of pages of book data.

    Args:
        pages_requested (int): Number of pages to scrape.

    Returns:
        pd.DataFrame: Pandas DataFrame containing book data.
    """
    book_data = []
    page = 0
    pages_to_scrape = 1

    while page<pages_to_scrape:
        page_url = BASE_URL
        page_html = extract_page_html(page_url)
        pages_books = extract_books_from_page(page_html)
        next_page_url = extract_next_page_url(page_html)

        if pages_books == []:
            break
        for book in pages_books:
            book_data.append(book)
        if next_page_url == '':
            break

        page_number_tag = page_html.select_one('.current')
        _, total_pages = page_number_tag.text.split('Page ')[1].split(' of ')

        if pages_requested > int(total_pages):
            pages_to_scrape = int(total_pages)
        elif pages_requested is None or pages_requested <= 0:
            pass
        else:
            pages_to_scrape = pages_requested

        print(f'{page + 1} of {pages_to_scrape} pages scraped.')

        page_url = next_page_url
        page += 1
        
    return pd.DataFrame(book_data)


def extract_books_from_page(page_html: BeautifulSoup) -> list:
    """
    Scrapes and returns book data from one page.
    
    Args:
        page_html (BeautifulSoup): Pages HTML to extract books from.

    Returns:
        books (list): List of dictionaries containing book data.
    """
    books = []
    for book_html in page_html.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        books.append(scrape_single_book(book_html))

    return books


def scrape_single_book(book_html: BeautifulSoup) -> dict:
    """
    Extract data for one book.

    Args:
        book_html (BeautifulSoup): HTML of book to extract data from.

    Returns:
        book_details (dict): Book details if available, or None.
    """
    title_tag = book_html.find('h3')
    book_details_page_url = construct_url(title_tag.find('a')['href'] if title_tag and title_tag.find('a') else '')
    if book_details_page_url:
        book_details = extract_book_details(book_details_page_url)
    else:
        book_details = None

    return book_details
    
    
def extract_book_details(book_details_page_url: str) -> dict:
    """
    Extracts book details from book page.

    Args:
        book_page_url (str): URL for page containing book details.

    Returns:
        dict: Book title, price, rating, category, description, url.
    """
    book_page_html = extract_page_html(book_details_page_url)

    breadcrumb_tag = book_page_html.select_one('.breadcrumb')
    category = breadcrumb_tag.find_all('li')[-2].find('a').text.strip() if breadcrumb_tag and breadcrumb_tag.find_all('li')[-2].find('a') else 'No category'

    description_tag = book_page_html.select_one('.product_page')
    description = description_tag.find('p').text.strip() if description_tag else 'No description'

    book_details_html = book_page_html.find('div', class_='col-sm-6 product_main')
    if book_details_html:
        title = book_details_html.find('h1').text.strip() if book_details_html.find('h1') else 'No title'
        price = book_details_html.find('p', class_='price_color').text.strip() if book_details_html.find('p', class_='price_color') else 'No price'
        rating = extract_rating_from_html(book_details_html)
    else:
        return None
    return({'title': title,
            'price': price,
            'rating': rating,
            'category': category,
            'description': description,
            'url': book_details_page_url})


def extract_rating_from_html(book_details_html: BeautifulSoup) -> int:
    """
    Extracts rating from book pages HTML.

    Args:
        book_details_html (BeautifulSoup): HTML of book page.

    Returns:
        int: Rating of book or None.
    """
    rating_text = book_details_html.select_one('.star-rating').attrs.get('class', '')[1].strip() if book_details_html.select_one('.star-rating') else ''
    if rating_text:
        string_integer_mapping = {'zero': 0,
                                      'one': 1,
                                      'two': 2,
                                      'three': 3,
                                      'four': 4,
                                      'five': 5}
        return string_integer_mapping[rating_text.lower()]
    return 'No rating'


def extract_next_page_url(current_page_html: BeautifulSoup) -> str:
    """
    Finds next button href and constructs URL.

    Args:
        current_page_html (BeautifulSoup): HTML of current page.

    Returns:
        str: URL for next page.
    """
    href_tag = current_page_html.find('li', class_='next')

    if not href_tag:
        return ''
    return construct_url(href_tag.find('a').attrs.get('href', ''))


def construct_url(href: str) -> str:
    """
    Construct full URL based on href.

    Args:
        href (str): The relative or absolute link to convert.

    Returns
        str: A complete, absolute URL.
    """
    if href.startswith('http'):
        return href
    elif href.startswith('catalogue'):
        return BASE_URL + href
    return CATALOGUE_URL + href


def extract_page_html(page_url: str) -> BeautifulSoup:
    """
    Extract page html.

    Args:
        page_url (str): URL of page to extract html from.

    Returns:
        BeautifulSoup: Parsed HTML from page.
    """
    response = requests.get(page_url)
    return BeautifulSoup(response.text, 'html.parser')
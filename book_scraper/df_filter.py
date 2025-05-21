# book_scraper/df_filter.py
import pandas as pd

def keyword_data_filter(df: pd.DataFrame, keywords: str) -> pd.DataFrame:
    """
    Filter a pandas DataFrame based on one or more keywords.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        keywords (str): Keyword or space-separated keyword(s) to search for in each column of every row.

    Returns:
        df[mask] (pd.DataFrame): A filtered DataFrame containing only rows with keyword matches.
    """
    mask = df.apply(lambda row: row.astype(str).str.contains('|'.join(keywords.split()), 
                                                                    case=False, na=False).any(), axis=1)

    return df[mask]
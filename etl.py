import os
import logging
from pathlib import Path
import requests
import pandas as pd
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def initialize_secrets():
    """
    Loads env, creates url and parameters
    Args: none
    Returns: url, params
    """
    
    logger.info("Initializing secrets...")
    
    # Load env variables
    load_dotenv()

    FRIDGEWATCHDOG_API_KEY = os.getenv('FRIDGEWATCHDOG_API_KEY')
    API_SERVER = os.getenv('API_SERVER')
    
    if not (FRIDGEWATCHDOG_API_KEY and API_SERVER):
        logger.error("Environmental variables are not accessible")
        raise ValueError("Environmental variables are not accessible")
    
    ENDPOINT = "/get"

    # Create URL for fetching data
    url = f"{API_SERVER}{ENDPOINT}"

    # Create parameters for API
    params = {
        'code': FRIDGEWATCHDOG_API_KEY
    }
    
    logger.info("Success! Secrets initialized")
    return url, params


def get_data(url: str, params: dict) -> pd.DataFrame:
    """Request API for data"""
    
    logger.info("Getting data...")
    
    try:
        response = requests.get(url=url, params=params, timeout=30)
        
        response.raise_for_status()
        
        data = response.json()
        logger.info("Text decoded to JSON")
        
        df = pd.json_normalize(data)
        logger.info(f"Successfully fetched {len(df)} records")
        
        return df
        
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        raise
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Couldn't decode JSON: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise


def save_data(df: pd.DataFrame) -> None:
    """Save DataFrame to multiple formats"""
    
    logger.info("Saving data...")
    
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)
    
    try:
        df.to_csv(output_dir / 'fridgewatchdog-open-dataset.csv', sep=',', index=False)
        logger.info("CSV saved")
        
        df.to_excel(output_dir / 'fridgewatchdog-open-dataset.xlsx', index=False)
        logger.info("Excel saved")
        
        df.to_json(output_dir / 'fridgewatchdog-open-dataset.json', orient='records', indent=2)
        logger.info("JSON saved")
        
        logger.info("All files saved successfully")
        
    except Exception as e:
        logger.error(f"Error saving files: {e}")
        raise


if __name__ == "__main__":
    try:
        url, params = initialize_secrets()
        df = get_data(url, params)
        save_data(df)
        
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise
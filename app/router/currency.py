import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()

def load_currency_data():
    """
    Load currency data from the JSON file
    Returns the currency data as a dictionary
    """
    try:
        current_dir = Path(__file__).parent
        json_path = current_dir / 'currency.json'
        with open(json_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Currency data file not found"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Error parsing currency data file"
        )

@router.get("/currencyapi/latest")
async def get_latest_rates():
    """
    Get the latest currency exchange rates
    Returns a dictionary with meta information and currency rates
    """
    return load_currency_data()
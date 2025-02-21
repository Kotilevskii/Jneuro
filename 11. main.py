"""
SPECIFICATION

Purpose:
The script serves as the main FastAPI application for processing and analyzing data through Google Sheets.

Features:
1. Data Processing:
   - Handles input data cleaning and formatting
   - Removes duplicate headers
   - Processes empty cells
   - Converts data to Google Sheets format

2. API Endpoints:
   - /create-sheet: Creates and processes sheet data
   - /health: Health check endpoint

3. Logging:
   - Logs all operations
   - Stores request and error data
   - Tracks data preparation steps

Input Format:
- Cleaned string data with pipe-separated values
- Headers and content rows

Output Format:
- Processed data in Google Sheets compatible format
- Error messages if processing fails
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from google_sheets import process_sheet_data
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    filename='/opt/eng-analysis/server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

# Update model for new parameter
class SheetRequest(BaseModel):
    cleaned_str: str

def prepare_data_for_google(rows: List[str]) -> dict:
    """
    Prepare data for Google Sheets:
    1. Excludes header duplication
    2. Removes empty rows
    3. Converts to proper format
    """
    logging.info(f"Starting data preparation. Received {len(rows)} rows")
    
    # If single string received - split by newlines
    if len(rows) == 1:
        rows = rows[0].split('\n')
    
    # Remove empty rows
    rows = [row for row in rows if row.strip()]
    
    logging.info(f"After splitting: {len(rows)} rows")
    
    # Remove duplicate headers
    seen_headers = set()
    filtered_rows = []
    for row in rows:
        cells = row.split('|')
        # Check if row is a header
        if cells and (
            "Problem|Problem Description|Quote" in row or 
            "Brief Problem title|Description of Current Situation|Quote Fragment" in row
        ):
            header_key = cells[0].strip()
            if header_key not in seen_headers:
                seen_headers.add(header_key)
                filtered_rows.append(row)
                logging.info("Header row added")
        else:
            filtered_rows.append(row)

    logging.info(f"After headers deduplication: {len(filtered_rows)} rows")

    # Convert to Google Sheets format
    sheet_data = []
    for row in filtered_rows:
        cells = row.split('|')
        # Preserve empty cells, replacing with space
        cells = [cell.strip() if cell.strip() else " " for cell in cells]
        
        row_data = {
            "values": [
                {
                    "userEnteredValue": {
                        "stringValue": cell
                    }
                } for cell in cells
            ]
        }
        sheet_data.append(row_data)

    logging.info(f"Final sheet data has {len(sheet_data)} rows")
    return {
        "output": sheet_data
    }

@app.post("/create-sheet")
async def create_sheet(request: SheetRequest):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Received new request at {timestamp}")
    
    try:
        # Log input data
        with open('/opt/eng-analysis/request_data.log', 'w') as f:
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Raw request data: {request.cleaned_str}\n")
        
        # Get rows from request
        rows = [row for row in request.cleaned_str.split('\n') if row.strip()]
        logging.info(f"Received {len(rows)} rows")
        
        # Prepare data
        logging.info("Starting data preparation")
        prepared_data = prepare_data_for_google(rows)
        
        # Log prepared data
        with open('/opt/eng-analysis/prepared_data.log', 'w') as f:
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Prepared data: {str(prepared_data)}\n")
        
        logging.info("Data preparation completed")
        
        # Process data through Google Sheets API
        result = process_sheet_data(prepared_data)
        
        if result.get("status") == "error":
            error_msg = result.get("message", "Unknown error occurred")
            logging.error(f"Error processing data: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)
            
        return result
        
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error processing request: {error_msg}")
        
        # Log error
        with open('/opt/eng-analysis/error_data.log', 'w') as f:
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Exception: {error_msg}\n")
        
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logging.info("Health check requested")
    return {"status": "healthy"}

# Log server start
logging.info("Server started")
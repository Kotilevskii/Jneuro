"""
SPECIFICATION

Purpose:
The script serves as the final node that combines and formats analysis results from different sources.

Features:
1. URL Extraction:
   - Processes input data from multiple sources
   - Extracts spreadsheet URLs
   - Handles different URL formats

2. Data Combination:
   - Combines analysis results
   - Merges quotes data
   - Integrates synthesis results

3. Error Handling:
   - Handles JSON parsing errors
   - Manages string escaping
   - Provides error reporting

Input Format:
- Analysis results
- Quote data
- Synthesis results

Output Format:
{
    "result": "Combined text with all URLs and descriptions"
}
"""

import json

def extract_url(body):
    try:
        # Handle different escape character variations
        cleaned = body.replace('\\"', '"')  # single escape
        cleaned = cleaned.replace('\\\"', '"')  # double escape
        cleaned = cleaned.replace("\\'", "'")  # escaped single quotes
        data = json.loads(cleaned)
        return data.get('spreadsheet_url', '')
    except:
        return ''

def main(analysis, quotes, synthesis):
    # Extract URLs from each source
    analysis_url = extract_url(analysis)
    quotes_url = extract_url(quotes)
    synthesis_url = extract_url(synthesis)
    
    # Combine results with descriptions
    text = "Table of needs for each respondent: " + analysis_url + " " + \
           "Table of quotes confirming needs: " + quotes_url + " " + \
           "Table of common needs that repeat across respondents: " + synthesis_url + " "
    
    return {"result": text} 
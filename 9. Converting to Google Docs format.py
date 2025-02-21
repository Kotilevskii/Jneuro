"""
SPECIFICATION

Purpose:
The script prepares analysis and synthesis results for publication by formatting and cleaning the data.

Execution sequence:
1. main(output):
   - Accepts output data in dict or string format
   - Processes and cleans the input data
   - Handles headers and table formatting
   - Returns cleaned and formatted string in JSON format

Input format:
- Dictionary with 'output' key containing data
- Direct string input with data

Output format:
{
    "cleaned_str": "formatted and cleaned string with table data"
}

Features:
1. Header processing:
   - Handles two types of headers (main and description)
   - Prevents header duplication
   - Maintains proper table structure
2. Cell processing:
   - Handles empty cells
   - Escapes special characters
   - Maintains proper cell formatting
3. JSON compatibility:
   - Ensures output is JSON-compatible
   - Properly escapes quotes and special characters
"""

import json

def main(output):
    try:
        # Get input data
        if isinstance(output, dict) and 'output' in output:
            input_str = output['output']
        else:
            input_str = str(output)
        
        # Remove leading and trailing quotes
        input_str = input_str.strip('"')
        
        # Replace escaped characters
        input_str = input_str.replace('\\"', '"')  # remove extra escaping for double quotes
        input_str = input_str.replace('\\\\', '\\')  # replace double backslashes with single ones
        
        # Process lines
        lines = []
        header_processed = False
        general_header_processed = False
        
        # Define table headers
        header_line = "|Problem|Problem Description|Quote|Negative Emotional State|Undesired Result|Desired Result|Deep Goal|Desired Emotional State|Importance of Desired Result|Frequency|Achievement Events|Desired Result Deadline|Achievement Criteria|Current Solutions|Satisfaction with DR Solutions|Solution Cost|Reasons for Dissatisfaction|Consequences/Costs|Drivers|Barriers|Ideal Solution|Respondent|"
        description_line = "|Brief Problem title|Description of Current Situation|Quote Fragment|Current Negative Emotions|What they want to escape from|What they want to achieve|Long-term Goal|Desired Positive Emotions|Rating 1-10|How often it occurs|Supporting Events|Desired Deadline|Measurable Indicators|What they tried before|Rating 1-10|How much paid for solutions|Triggers for refusal|Measurable Costs|Motivation for Change|Barriers to Achievement|Ideal Option|Respondent Name|"
        
        for line in input_str.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Skip repeating headers
            if line == header_line and header_processed:
                continue
            if line == description_line and general_header_processed:
                continue
            
            if line == header_line and not header_processed:
                header_processed = True
                general_header_processed = False  # Reset for the next header type
            elif line == description_line and not general_header_processed:
                general_header_processed = True
                header_processed = False  # Reset for the next header type
            
            # Remove leading and trailing pipe characters
            if line.startswith('|'):
                line = line[1:]
            if line.endswith('|'):
                line = line[:-1]
            
            # Split into cells by pipe character
            cells = line.split('|')
            
            # Process each cell
            processed_cells = []
            for cell in cells:
                cell = cell.strip()
                # Escape pipe character in quotes
                if "«" in cell and "»" in cell:
                    cell = cell.replace('|', '\\|')
                # Keep empty cells as spaces
                processed_cells.append(cell if cell else " ")
            
            # Form line with pipe separator
            processed_line = '|'.join(processed_cells)
            if processed_line.strip():
                lines.append(processed_line)
        
        # Build final string
        cleaned_str = '\n'.join(lines)
        
        # Escape quotes for JSON
        cleaned_str = cleaned_str.replace('"', '\\"')
        
        # Validate JSON format
        test_json = json.dumps({"cleaned_str": cleaned_str})
        
        return {
            "cleaned_str": cleaned_str
        }
    
    except Exception as e:
        return {
            "cleaned_str": f"Error: {str(e)}"
        }
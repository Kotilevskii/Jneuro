"""
SPECIFICATION

Purpose:
The script converts input data into a format compatible with Google Docs, handling table formatting and data cleaning.

Features:
1. Data Processing:
   - Handles input in both dict and string formats
   - Cleans and formats text data
   - Processes table structures

2. Table Formatting:
   - Handles table headers
   - Processes table cells
   - Maintains data integrity

3. Character Processing:
   - Handles special characters
   - Manages quotes and escaping
   - Processes empty cells

Input Format:
- Dict with 'output' key containing data, or
- Direct string input with table data

Output Format:
{
    "cleaned_str": "processed and formatted string"
}
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
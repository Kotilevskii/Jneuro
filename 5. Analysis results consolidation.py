"""
SPECIFICATION

Purpose:
The script consolidates analysis results by processing and combining multiple story inputs.

Features:
1. Input Processing:
   - Handles both JSON strings and dictionaries
   - Processes text data from multiple sources
   - Maintains data integrity during processing

2. Story Handling:
   - Extracts text from JSON structures
   - Processes raw text inputs
   - Combines multiple stories

3. Error Handling:
   - Handles JSON parsing errors
   - Manages different input formats
   - Provides error reporting

Input Format:
- List of stories in either:
  - JSON string format with "text" field
  - Dictionary format with "text" field
  - Direct text string

Output Format:
{
    "result": "Combined stories separated by double line breaks"
}
"""

def main(stories):
    # Specification: function processes both JSON strings and dictionaries
    all_stories = []
    
    for story in stories:
        # Check if story is a string
        if isinstance(story, str):
            try:
                # Try to parse string as JSON
                story_data = json.loads(story)
                if "text" in story_data:
                    all_stories.append(story_data["text"])
                else:
                    all_stories.append(story_data)
            except json.JSONDecodeError:
                # If it's just text, add it directly
                all_stories.append(story)
        elif isinstance(story, dict):
            # If story is already a dictionary
            if "text" in story:
                all_stories.append(story["text"])
            else:
                all_stories.append(story)
        else:
            # If format is unknown, add as is
            all_stories.append(story)
    
    # Combine all stories with double line breaks
    combined = "\n\n".join(all_stories)
    
    return {
        "result": combined
    }

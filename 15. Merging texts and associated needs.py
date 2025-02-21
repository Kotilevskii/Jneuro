'''
SPECIFICATION

Purpose:
Script pairs texts with their corresponding needs/stories based on text number identifiers.

Execution sequence:
1. main(text, stories):
  - Takes array[string] of JSON texts and array[string] of stories
  - Calls pair_texts_with_stories()
  - Returns JSON result

2. extract_text_number(text):
  - Extracts text number from different formats
  - Returns number or None if not found

3. pair_texts_with_stories(texts, stories):
  - Groups texts by number
  - Matches stories to texts
  - Combines each text with its stories
  - Returns array of JSON strings

Input format:
- text: array[string] of JSON texts with text_number
- stories: array[string] with text numbers in various formats

Output format:
{
   "result": [
       "{"text_with_stories": "text content + needs"}", 
       ...
   ]
}

Validation:
- Each text paired only with its matching stories
- Text numbers preserved
- Stories without text numbers skipped
- Unicode characters handled correctly
'''

import json
import re

def extract_text_number(text):
   # Extract text number from JSON or text patterns
   try:
       text_data = json.loads(text)
       return text_data.get("text_number")
   except:
       patterns = [
           r'(?:text_number|Text number)[:\s]+(\d+)',
           r'^(\d+)\.',
           r'текст[а]?\s+(\d+)'
       ]
       for pattern in patterns:
           match = re.search(pattern, text, re.I)
           if match:
               return int(match.group(1))
   return None

def pair_texts_with_stories(texts, stories):
   # Create dictionary of texts by number
   text_dict = {}
   for text in texts:
       text_data = json.loads(text)
       text_num = text_data["text_number"] 
       text_dict[text_num] = text

   # Group stories by text number
   story_dict = {}
   for story in stories:
       text_num = extract_text_number(story)
       if text_num:
           if text_num not in story_dict:
               story_dict[text_num] = []
           story_dict[text_num].append(story)

   # Combine texts with their stories
   result = []
   for text_num in sorted(text_dict.keys()):
       if text_num in story_dict:
           text_with_stories = text_dict[text_num] + "\n\nStories:\n" + "\n".join(story_dict[text_num])
           result.append(json.dumps({"text_with_stories": text_with_stories}, ensure_ascii=False))

   return result

def main(text, stories):
   # Process texts and stories, return combined result
   try:
       result = pair_texts_with_stories(text, stories)
       return {"result": result}
   except Exception as e:
       print(f"Error processing texts and stories: {str(e)}")
       return {"result": []}
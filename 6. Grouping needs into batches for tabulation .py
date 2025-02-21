def main(input_data):
    '''
    Function for preparing Job Stories for analysis by splitting them into small groups (chunks).
    
    Purpose:
        When we have a large text with multiple Job Stories (user stories),
        it needs to be split into small parts for further analysis. Each story
        starts with "Text number" and contains "**Problem".
        
        The function groups stories by 3 to:
        1. Avoid overloading the analysis system with large volumes of text
        2. Maintain context between related stories
        3. Ensure sequential data processing
    
    Args:
        input_data (Union[dict, str]): Text with Job Stories in one of two formats:
            - dict: {"input_data": "text with stories"}
            - str: "text with stories directly"
    
    Returns:
        dict: Dictionary with splitting results:
            {
                "result": [
                    # Each element is a JSON string with chunk information:
                    '{
                        "stories": ["Story 1", "Story 2", "Story 3"],  # up to 3 stories per chunk
                        "chunk_index": 1,                              # chunk number
                        "remove_header": false,                        # whether to remove header (for all except first)
                        "row_count": 3                                # number of stories in chunk
                    }',
                    # ... next chunks
                ]
            }
    
    Example:
        >>> text = """
        Text number 1 **Problem 1** Description of first problem...
        Text number 2 **Problem 1** Description of second problem...
        Text number 3 **Problem 1** Description of third problem...
        """
        >>> result = main(text)
        >>> # Result will contain one chunk with three stories
    '''
    try:
        # Determine input data format
        if isinstance(input_data, dict):
            text_data = input_data.get("input_data", "")
        else:
            text_data = input_data
            
        # Split text into Job Stories by text number pattern
        stories = text_data.split("Text number")
        stories = [s.strip() for s in stories if "**Problem" in s]  # Filter only parts with problems
        
        # Split into chunks of 3 stories
        chunk_size = 3
        chunks = []
        
        for i in range(0, len(stories), chunk_size):
            chunk = stories[i:i + chunk_size]
            chunk_index = (i // chunk_size) + 1
            remove_header = chunk_index != 1
            
            # Add "Text number" back to each story
            chunk_with_numbers = ["Text number" + s for s in chunk]
            
            # Add metadata to the beginning of first story in chunk
            chunk_with_numbers[0] = f"chunk_index: {chunk_index}\nremove_header: {remove_header}\n\nText number" + chunk[0]
            
            chunks.append(json.dumps({
                "stories": chunk_with_numbers,
                "row_count": len(chunk)
            }, ensure_ascii=False))
        
        return {"result": chunks}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"result": []} 
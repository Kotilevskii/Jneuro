import json

def main(input_data):
    try:
        # Get the list from input_data
        if isinstance(input_data, dict):
            text_list = input_data.get("input_data", [])
        else:
            text_list = input_data if isinstance(input_data, list) else [input_data]
        
        print("Processing list of length:", len(text_list))
        
        # Process each text in the list and collect all stories
        all_stories = []
        for text in text_list:
            # Split the text into stories using the "**Problem" marker
            stories = text.split("**Problem")
            stories = [s.strip() for s in stories if s.strip()]
            # Re-add the "**Problem" marker
            stories = ["**Problem" + s for s in stories]
            all_stories.extend(stories)
        
        print("Total stories found:", len(all_stories))
        
        # Split into chunks of 3 stories
        chunk_size = 3
        chunks = []
        
        for i in range(0, len(all_stories), chunk_size):
            chunk = all_stories[i:i + chunk_size]
            chunks.append(json.dumps({
                "stories": chunk
            }, ensure_ascii=False))
        
        print("Number of chunks created:", len(chunks))
        
        return {"result": chunks}
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return {"result": []}
'''
SPECIFICATION

Purpose:
The script splits an array of texts into numbered chunks while preserving sentence integrity.

Execution Sequence:
1. main(input_data):
   - Accepts either a dict containing an array of texts or an array of texts directly
   - Validates the input data format
   - For each text, calls split_into_chunks()
   - Generates metadata and formats JSON response

2. split_into_chunks(text, max_length):
   - Takes text and maximum chunk length (25000 characters)
   - Note: 25,000 characters + prompt = approximate context window size processable by the model
   - Iteratively splits text into chunks
   - For each chunk, calls find_sentence_boundary()
   - Returns an array of chunks

3. find_sentence_boundary(text, max_length):
   - Locates the last complete sentence within max_length
   - Uses regular expressions to find sentence endings (.!?)
   - Returns both the ending index and the text up to that index

Output Format:
{
    "result": [
        {
            "chunk_id": "1.1",      # Format: "<text_number>.<chunk_number>"
            "text": "...",          # Chunk content
            "length": 25000,        # Length of chunk
            "complete_sentences": true  # Flag indicating sentence integrity
        },
        ...
    ]
}

Constraints:
- Maximum chunk size: 25,000 characters
- All chunks (except the last one in each text) are close to maximum size
- Each chunk must end with a complete sentence
'''

import json
import re

def join_chunks_to_texts(chunks):
    texts_dict = {}
    
    for chunk in chunks:
        try:
            # Remove markdown code block indicators
            chunk = re.sub(r'```json\n|```', '', chunk)
            
            # Parse JSON string into a dictionary
            chunk_data = json.loads(chunk)
            chunk_id = chunk_data["chunk_id"]
            chunk_content = chunk_data["text"]
            
            # Парсим X.Y из номера чанка
            text_num = int(chunk_id.split('.')[0])
            chunk_num = int(chunk_id.split('.')[1])
            
            if text_num not in texts_dict:
                texts_dict[text_num] = []
                
            texts_dict[text_num].append((chunk_num, chunk_content))
            
        except Exception as e:
            print(f"Ошибка парсинга чанка: {e}")
            continue
    
    # Собираем тексты в правильном порядке с сохранением номера текста
    assembled_texts = []
    for text_num in sorted(texts_dict.keys()):
        # Сортируем чанки по номеру для сохранения последовательности
        sorted_chunks = sorted(texts_dict[text_num], key=lambda x: x[0])
        full_text = ' '.join(chunk[1] for chunk in sorted_chunks)
        
        # Создаем словарь и сразу преобразуем его в JSON-строку
        text_data = json.dumps({
            "text_number": text_num,
            "text": full_text
        }, ensure_ascii=False)
        assembled_texts.append(text_data)
    
    return assembled_texts

def main(cleaned_text_chunks):
    """
    Input: cleaned_text_chunks - array[string] с JSON-форматированными чанками
    Output: array[string] with reassembled texts
    """
    try:
        texts_for_analysis = join_chunks_to_texts(cleaned_text_chunks)
        
        if not texts_for_analysis:
            raise ValueError("Failed to assemble texts from chunks")
        
        return {"result": texts_for_analysis}
        
    except Exception as e:
        print(f"Error assembling texts: {str(e)}")
        return {"result": []}

def find_sentence_boundary(text, max_length):
    """
    Finds the boundary of the last complete sentence within max_length
    """
    sentence_endings = list(re.finditer('[.!?]+(?=\s|$)', text[:max_length]))
    
    if not sentence_endings:
        return -1, ""
    
    last_ending = sentence_endings[-1]
    end_idx = last_ending.end()
    
    while end_idx < len(text) and text[end_idx].isspace():
        end_idx += 1
        
    return end_idx, text[:end_idx]

def split_into_chunks(text, max_length):
    """
    Splits text into chunks while preserving sentence boundaries
    """
    chunks = []
    remaining_text = text
    
    while remaining_text:
        if len(remaining_text) <= max_length:
            chunks.append(remaining_text)
            break
            
        end_idx, chunk = find_sentence_boundary(remaining_text, max_length)
        
        if end_idx == -1:
            chunks.append(remaining_text[:max_length])
            remaining_text = remaining_text[max_length:]
        else:
            chunks.append(chunk)
            remaining_text = remaining_text[end_idx:].strip()
    
    return chunks

def main(input_data):
    """
    Splits input texts into chunks considering size and sentence integrity
    Input: dict with text array or text array directly
    Output: JSON with numbered chunks
    """
    try:
        # Determine input data format
        if isinstance(input_data, dict):
            texts = input_data.get("result", [])
        else:
            texts = input_data if isinstance(input_data, list) else [input_data]
        
        MAX_CHUNK_SIZE = 25000
        chunked_texts = []
        
        # Process each text
        for text_idx, text in enumerate(texts, 1):
            if not text:
                continue
                
            # Split text into chunks
            chunks = split_into_chunks(str(text), MAX_CHUNK_SIZE)
            
            # Generate metadata for each chunk
            for chunk_idx, chunk in enumerate(chunks, 1):
                chunk_data = {
                    "chunk_id": f"{text_idx}.{chunk_idx}",
                    "text": chunk,
                    "length": len(chunk),
                    "complete_sentences": True
                }
                chunked_texts.append(chunk_data)
        
        # Convert to JSON with ensure_ascii=False parameter
        output_chunks = [json.dumps(chunk, ensure_ascii=False) for chunk in chunked_texts]
        return {"result": output_chunks}
        
    except Exception as e:
        print(f"Error processing chunks: {str(e)}")
        return {"result": []}
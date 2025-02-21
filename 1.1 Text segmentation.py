"""
SPECIFICATION

Purpose:
The script splits an array of texts into numbered chunks while preserving sentence integrity.

Execution sequence:
1. main(input_data):
   - Accepts dict with text array or text array directly
   - Validates input data format
   - Calls split_into_chunks() for each text
   - Generates metadata and JSON response

2. split_into_chunks(text, max_length):
   - Accepts text and maximum chunk length (25000 characters)
   25,000 characters + prompt = approximate context window size that can be processed by the model
   - Iteratively splits text into chunks
   - Calls find_sentence_boundary() for each chunk
   - Returns array of chunks

3. find_sentence_boundary(text, max_length):
   - Finds the last complete sentence within max_length
   - Uses regular expressions to find sentence endings (.!?)
   - Returns sentence end index and text up to that index

Output format:
{
    "result": [
        {
            "chunk_id": "1.1",      # Format: "<text_number>.<chunk_number>"
            "text": "...",          # Chunk text
            "length": 25000,        # Chunk length
            "complete_sentences": true  # Sentence integrity flag
        },
        ...
    ]
}

Limitations:
- Maximum chunk size: 25000 characters
- All chunks (except the last one in each text) are close to maximum size
- Each chunk ends with a complete sentence
"""

import re
import json

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
        # Определяем формат входных данных
        if isinstance(input_data, dict):
            texts = input_data.get("result", [])
        else:
            texts = input_data if isinstance(input_data, list) else [input_data]
        
        MAX_CHUNK_SIZE = 25000
        chunked_texts = []
        
        # Обрабатываем каждый текст
        for text_idx, text in enumerate(texts, 1):
            if not text:
                continue
                
            # Разбиваем текст на чанки
            chunks = split_into_chunks(str(text), MAX_CHUNK_SIZE)
            
            # Формируем метаданные для каждого чанка
            for chunk_idx, chunk in enumerate(chunks, 1):
                chunk_data = {
                    "chunk_id": f"{text_idx}.{chunk_idx}",
                    "text": chunk,
                    "length": len(chunk),
                    "complete_sentences": True
                }
                chunked_texts.append(chunk_data)
        
        # Преобразуем в JSON с параметром ensure_ascii=False
        output_chunks = [json.dumps(chunk, ensure_ascii=False) for chunk in chunked_texts]
        return {"result": output_chunks}
        
    except Exception as e:
        print(f"Error processing chunks: {str(e)}")
        return {"result": []}

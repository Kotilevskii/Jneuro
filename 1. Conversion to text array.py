def main(docextractor):
    texts = []
    for text in docextractor:
        if text:  
            texts.append(str(text))
    
    return {
        "result": texts
    }
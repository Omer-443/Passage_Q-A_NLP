import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def chunk_text(text, max_tokens=200):
    sentences = sent_tokenize(text)
    chunks, chunk, count = [], [], 0
    for sentence in sentences:
        sentence_len = len(sentence.split())
        if count + sentence_len > max_tokens:
            if chunk:
                chunks.append(" ".join(chunk))
            chunk = [sentence]
            count = sentence_len
        else:
            chunk.append(sentence)
            count += sentence_len
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

from underthesea import word_tokenize

VIETNAMESE_STOPWORDS = [
    "và", "là", "của", "cho", "với", "các", "một",
    "những", "được", "tại", "trong", "khi", "đến",
    "này", "đó", "rất", "có", "không"
]

def vietnamese_tokenizer(text):
    return word_tokenize(text, format="text").split()

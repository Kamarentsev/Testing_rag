import os
import re
import numpy as np
from docx import Document
from transformers import RobertaTokenizer, RobertaModel
import torch
import faiss

# Загрузка модели и токенизатора
tokenizer = RobertaTokenizer.from_pretrained('DeepPavlov/roberta-large')
model = RobertaModel.from_pretrained('DeepPavlov/roberta-large')

def encode_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

def clean_text(text):
    # Удаление ненужных шаблонов и слов
    text = re.sub(r"шаблонные слова и предложения", "", text)
    return text

def extract_text_from_docs(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".docx"):
            doc_path = os.path.join(directory, filename)
            doc = Document(doc_path)
            doc_text = [para.text for para in doc.paragraphs]
            documents.append((filename, doc_text))
    return documents

def index_texts(documents):
    all_texts = []
    for doc_name, paragraphs in documents:
        for i, para in enumerate(paragraphs):
            cleaned_text = clean_text(para)
            all_texts.append((doc_name, i, cleaned_text))
    
    vectors = [encode_text(text) for _, _, text in all_texts]
    dimension = vectors[0].shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.vstack(vectors))
    return index, all_texts

def search(index, query, all_texts):
    query_vector = encode_text(query)
    D, I = index.search(query_vector, k=5)  # Найти 5 ближайших
    results = [all_texts[i] for i in I[0]]
    return results

# Основная часть кода
if __name__ == "__main__":
    directory = 'path_to_word_docs'  # Укажите путь к папке с документами
    documents = extract_text_from_docs(directory)
    index, all_texts = index_texts(documents)

    query = input("Введите текст запроса: ")
    results = search(index, query, all_texts)

    for doc_name, para_num, result in results:
        print(f"Документ: {doc_name}, Абзац: {para_num + 1}")
        print(result)
        print()


------------------

from spellchecker import SpellChecker
import pymorphy2

# Инициализируем проверку орфографии
spell = SpellChecker(language='ru')
morph = pymorphy2.MorphAnalyzer()

def check_spelling(text):
    words = text.split()
    misspelled = spell.unknown(words)  # Поиск орфографических ошибок

    if not misspelled:
        print("Орфографических ошибок не найдено.")
    else:
        print("Найдены орфографические ошибки:")
        for word in misspelled:
            print(f"{word} -> {spell.correction(word)}")

def check_grammar(text):
    words = text.split()
    corrected_text = []

    for word in words:
        parsed_word = morph.parse(word)[0]
        normal_form = parsed_word.normal_form  # Получаем нормальную форму слова
        
        # Здесь можно добавить дополнительные проверки на согласование слов,
        # но это требует более сложных алгоритмов.

        corrected_text.append(normal_form)

    return " ".join(corrected_text)

def main():
    input_text = input("Введите текст для проверки: ")
    
    # Проверка орфографии
    check_spelling(input_text)
    
    # Проверка и исправление грамматики
    corrected_text = check_grammar(input_text)
    print(f"Исправленный текст: {corrected_text}")

if __name__ == "__main__":
    main()


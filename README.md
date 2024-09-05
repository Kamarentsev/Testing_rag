import os
import docx
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Функция для чтения абзацев из файлов .docx
def read_docx_files(directory):
    paragraphs = []
    filenames = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".docx"):
            doc_path = os.path.join(directory, filename)
            doc = docx.Document(doc_path)
            for para in doc.paragraphs:
                text = para.text.strip()
                if text:  # добавляем только непустые абзацы
                    paragraphs.append(text)
                    filenames.append(filename)
                    
    return paragraphs, filenames

# 2. Функция для создания эмбеддингов
def embed_paragraphs(paragraphs, model):
    return model.encode(paragraphs)

# 3. Функция для создания и индексации с FAISS
def create_faiss_index(embeddings):
    d = embeddings.shape[1]  # размерность эмбеддингов
    index = faiss.IndexFlatL2(d)  # создаем индекс для поиска
    index.add(embeddings)  # добавляем все эмбеддинги
    return index

# 4. Функция для поиска по запросу
def search_similar_paragraphs(query, model, index, paragraphs, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for idx in indices[0]:
        results.append(paragraphs[idx])
    
    return results

# Основной код
def main(directory, query, top_k=5):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Загружаем модель
    
    # Шаг 1: Чтение абзацев из документов
    paragraphs, filenames = read_docx_files(directory)
    
    # Шаг 2: Создание эмбеддингов для абзацев
    embeddings = embed_paragraphs(paragraphs, model)
    
    # Шаг 3: Индексация эмбеддингов с помощью FAISS
    index = create_faiss_index(embeddings)
    
    # Шаг 4: Поиск по запросу
    similar_paragraphs = search_similar_paragraphs(query, model, index, paragraphs, top_k)
    
    # Вывод результатов
    print("Результаты поиска:")
    for i, paragraph in enumerate(similar_paragraphs):
        print(f"Результат {i+1}:")
        print(paragraph)
        print()
        
# Пример использования
directory = "path_to_your_docx_files"
query = "Введите ваш поисковый запрос"
main(directory, query)

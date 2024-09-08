#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import pandas as pd
from docx import Document

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def split_and_filter_text(text, min_length):
    # Разделение текста по строкам
    paragraphs = [para.strip() for para in text.split('\n') if para.strip()]
    
    filtered_paragraphs = []
    temp_paragraph = ""
    previous_paragraph = ""
    
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i]
        # Проверка на наличие нумерации
        if re.match(r'^\d+(\.\s+|–\s+)', para):
            if previous_paragraph:
                # Объединяем предыдущий абзац с текущими нумерованными абзацами
                temp_paragraph = f"{previous_paragraph}\n{para}"
                previous_paragraph = ""  # Сброс предыдущего абзаца
            else:
                temp_paragraph = para
            # Продолжаем добавлять все следующие нумерованные абзацы
            while i + 1 < len(paragraphs) and re.match(r'^\d+(\.\s+|–\s+)', paragraphs[i + 1]):
                temp_paragraph += f"\n{paragraphs[i + 1]}"
                i += 1
            filtered_paragraphs.append(temp_paragraph)
            temp_paragraph = ""
        elif len(para) >= min_length:
            # Если уже есть сохранённый предыдущий абзац, добавляем его в filtered_paragraphs
            if previous_paragraph:
                filtered_paragraphs.append(previous_paragraph)
            previous_paragraph = para
        i += 1
    
    # Добавляем последний сохранённый абзац, если он не пустой
    if previous_paragraph:
        filtered_paragraphs.append(previous_paragraph)
    
    # Объединяем все отфильтрованные абзацы в один текст
    combined_text = "\n".join(filtered_paragraphs)
    
    return combined_text

def process_files_to_dataframe(input_dir, min_length):
    data = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.docx'):
            input_file_path = os.path.join(input_dir, filename)
            
            # Чтение текста из файла
            text = read_docx(input_file_path)
            
            # Обработка текста
            combined_text = split_and_filter_text(text, min_length)
            
            # Добавление данных в список
            data.append({
                'name_doc': filename,
                'text': combined_text
            })
    
    # Создание DataFrame
    df = pd.DataFrame(data, columns=['name_doc', 'text'])
    return df

# Пример использования
input_directory = r'C:\Users\kamar\Desktop\word_files'
min_length = 60

pd.set_option('display.max_colwidth', None)
#pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None) 

df = process_files_to_dataframe(input_directory, min_length)

df


# In[2]:


from datasets import Dataset
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.neighbors import NearestNeighbors

ds = Dataset.from_pandas(df)

tokenizer = AutoTokenizer.from_pretrained("ai-forever/ruRoberta-large")
model = AutoModel.from_pretrained("ai-forever/ruRoberta-large")

device = torch.device("cpu")
model.to(device)

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]

def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt"
    )
    encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
    model_output = model(**encoded_input)
    return cls_pooling(model_output)

embeddings_dataset = ds.map(
    lambda x: {"embeddings": get_embeddings(x["text"]).detach().cpu().numpy()[0]}
)


# In[8]:


import faiss

embeddings_dataset.add_faiss_index(column="embeddings")

question = "Из-за чего было обновлено программное обеспечение?"
question_embedding = get_embeddings([question]).cpu().detach().numpy()
question_embedding.shape


# In[9]:


scores, samples = embeddings_dataset.get_nearest_examples(
    "embeddings", question_embedding, k=3,
)


# In[10]:


import pandas as pd

samples_df = pd.DataFrame.from_dict(samples)
samples_df["scores"] = scores
samples_df.sort_values("scores", ascending=False, inplace=True)


# In[11]:


for _, row in samples_df.iterrows():
    print(f"name_doc: {row.name_doc}")
    print(f"SCORE: {row.scores}")
    print(f"TEXT: {row.text}")    
    print("=" * 50)
    print()


# In[12]:


samples_df


# In[16]:


get_ipython().system('pip install sentence_transformers -q')


# In[17]:


import faiss
from sentence_transformers import SentenceTransformer
import numpy as np


# In[18]:


# Загружаем модель для создания эмбеддингов предложений
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')


# In[19]:


# Ваши тексты датасета
texts = [
    '''В ходе выполнения регулярных технических работ по обновлению серверного оборудования 5 сентября 2023 года был выявлен ряд неполадок в системе резервного копирования данных. А именно, обнаружена сбойная работа программного обеспечения, ответственного за автоматическое создание резервных копий критически важных данных компании.\nСогласно графику, копирование должно осуществляться ежедневно в 02:00 ночи, однако с 1 по 5 сентября копии не создавались из-за ошибки в скриптах автоматизации. Ситуация была выявлена в процессе анализа логов системы после того, как несколько сотрудников обратились с жалобами на проблемы с доступом к старым версиям файлов.\n1. Обновлено программное обеспечение для резервного копирования;\n2. Выполнена полная проверка целостности существующих данных;\n3. Вручную созданы резервные копии всех критических данных.\nРекомендую провести аудит всей системы автоматизации резервного копирования, а также установить дополнительное программное обеспечение для мониторинга корректности выполнения процессов. Подробный отчет о выполненных действиях прилагается к докладной записке.''',
    '''В связи с расширением отдела маркетинга и необходимостью введения новой должности для обеспечения роста клиентской базы и увеличения объёмов продаж, приказываю:\n1. Внести изменения в штатное расписание ООО «РеалИнвест», добавив новую должность "Менеджер по работе с ключевыми клиентами" с окладом в размере 120 000 рублей в месяц.\n2. Установить, что должность будет относиться к категории специалистов отдела маркетинга и будет подчиняться непосредственно начальнику отдела.\n3. Руководителю отдела кадров Мироновой В. С. внести необходимые изменения в штатное расписание и уведомить бухгалтерию о введении новой должности.\n4. Начальнику отдела маркетинга Лебедеву И. Н. подготовить описание должностных обязанностей для новой позиции и провести отбор кандидатов на вакантную должность до 30 сентября 2023 года.\n5. Контроль за выполнением настоящего приказа оставляю за собой.''',
    '''В ходе проведения сверки расчетов с контрагентами по состоянию на 30 августа 2023 года была выявлена задолженность в размере 750 000 рублей от компании «ТехПром», по договору № 123/22 от 15 июня 2023 года. Согласно условиям договора, оплата должна была быть произведена не позднее 1 августа 2023 года, однако на сегодняшний день денежные средства не поступили.\nПосле направления нескольких уведомлений о просрочке платежа со стороны бухгалтерии ООО «ТехПром», ответа или подтверждения оплаты не последовало. В связи с этим, предлагаю направить официальное претензионное письмо в адрес контрагента с требованием о погашении задолженности в течение 10 рабочих дней с момента получения письма.\nПрошу вашего одобрения на данный шаг и, при необходимости, дальнейшие консультации с юридическим отделом для подготовки документов в суд в случае продолжения просрочки.''',
    # Добавьте больше текстов
]

# Создаем эмбеддинги для всех текстов
embeddings = model.encode(texts, convert_to_numpy=True)

# Создаем индекс FAISS
dimension = embeddings.shape[1]  # Размерность эмбеддингов
index = faiss.IndexFlatL2(dimension)  # Используем L2 (евклидову метрику)
index.add(embeddings)  # Добавляем эмбеддинги в индекс


# In[20]:


# Ваш запрос
query = "технические работы по обновлению"

# Преобразуем запрос в вектор
query_embedding = model.encode([query], convert_to_numpy=True)

# Ищем ближайшие тексты (k = количество результатов)
k = 3  # Найти топ-3 ближайших текста
distances, indices = index.search(query_embedding, k)

# Выводим результаты
print(f"Запрос: {query}")
for i, idx in enumerate(indices[0]):
    print(f"Результат {i+1}: {texts[idx]} (дистанция: {distances[0][i]})")


# In[ ]:





# In[ ]:





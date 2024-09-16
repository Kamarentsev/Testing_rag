import spacy
import re

# Загружаем модель для русского языка
nlp = spacy.load("ru_core_news_sm")

def replace_entities(text):
    # Пропускаем текст через NLP-модель
    doc = nlp(text)
    
    # Создаем копию текста
    new_text = text

    # Заменяем сущности, распознанные spaCy
    for ent in doc.ents:
        if ent.label_ == "ORG":  # Организации
            new_text = new_text.replace(ent.text, "[компания]")
        elif ent.label_ == "DATE":  # Даты
            new_text = new_text.replace(ent.text, "[дата]")
        elif ent.label_ == "MONEY":  # Суммы
            new_text = new_text.replace(ent.text, "[сумма]")
        elif ent.label_ == "PERSON":  # Имена сотрудников
            new_text = new_text.replace(ent.text, "[сотрудник]")

    # Обрабатываем даты формата "дд.мм.гггг" через регулярные выражения
    new_text = re.sub(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', '[дата]', new_text)
    
    # Обрабатываем суммы (например, "120000 рублей", "50 USD")
    new_text = re.sub(r'\b\d+[\s]?(руб(лей)?|USD|EUR|долларов|евро)\b', '[сумма]', new_text)
    
    # Обрабатываем имена с инициалами (например, "Лебедев И.А.")
    new_text = re.sub(r'\b[А-ЯЁ][а-яё]+ [А-ЯЁ]\.[А-ЯЁ]\.', '[сотрудник]', new_text)
    
    return new_text

# Пример текста
text = """
Компания ООО Ромашка заключила договор с ООО Василек в срок до 15.06.2023 на сумму 120000 рублей в месяц.
Сотрудник Лебедев И.А. будет ответственным за выполнение контракта.
"""

# Преобразуем текст
new_text = replace_entities(text)
print(new_text)

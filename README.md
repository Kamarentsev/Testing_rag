import spacy

# Загружаем модель для русского языка
nlp = spacy.load("ru_core_news_sm")

def replace_entities(text):
    # Пропускаем текст через NLP-модель
    doc = nlp(text)
    
    # Создаем копию текста
    new_text = text
    
    # Заменяем сущности в тексте
    for ent in doc.ents:
        if ent.label_ == "ORG":  # Организации
            new_text = new_text.replace(ent.text, "[компания]")
        elif ent.label_ == "DATE":  # Даты
            new_text = new_text.replace(ent.text, "[дата]")
        elif ent.label_ == "MONEY":  # Суммы
            new_text = new_text.replace(ent.text, "[сумма]")
    
    return new_text

# Пример текста
text = "Компания ООО Ромашка заключила договор с ООО Василек 12 января 2023 года на сумму 500000 рублей."

# Преобразуем текст
new_text = replace_entities(text)
print(new_text)

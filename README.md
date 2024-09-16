import spacy
import re

# Используем более крупную модель для лучшего распознавания
nlp = spacy.load("ru_core_news_lg")

def replace_entities(text):
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
        elif ent.label_ == "PERSON":  # Фамилии и имена
            new_text = new_text.replace(ent.text, "[сотрудник]")

    # Регулярные выражения для дат (формат: дд.мм.гггг)
    new_text = re.sub(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', '[дата]', new_text)

    # Регулярные выражения для сумм (например, "120000 рублей", "50 USD")
    new_text = re.sub(r'\b\d+[\s]?(руб(лей)?|USD|EUR|долларов|евро)\b', '[сумма]', new_text)

    # Регулярные выражения для фамилий с инициалами (например, "Лебедев И.Н.")
    new_text = re.sub(r'\b[А-ЯЁ][а-яё]+ [А-ЯЁ]\.[А-ЯЁ]\.', '[сотрудник]', new_text)
    
    # Регулярные выражения для полного ФИО с инициалами (например, "Иванов И.И.")
    new_text = re.sub(r'\b[А-ЯЁ][а-яё]+ [А-ЯЁ]\.[А-ЯЁ]\.', '[сотрудник]', new_text)

    # Регулярные выражения для ФИО с полным именем и отчеством (например, "Иванов Иван Иванович")
    new_text = re.sub(r'\b[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+\b', '[сотрудник]', new_text)

    return new_text

# Пример текста
text = """
Начальнику отдела маркетинга Лебедеву И.Н. необходимо подготовить отчет до 30 сентября 2023 года на сумму 120000 рублей.
Сотрудник Иванов Иван Иванович подписал контракт с компанией ООО Ромашка.
"""

# Преобразуем текст
new_text = replace_entities(text)
print(new_text)

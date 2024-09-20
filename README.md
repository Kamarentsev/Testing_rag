import spacy
from spellchecker import SpellChecker
from transformers import pipeline

# Загрузка NLP модели из spacy (предположим, на русском языке)
nlp = spacy.load("ru_core_news_sm")

# Инициализация проверки орфографии
spell = SpellChecker(language='ru')

# Функция для проверки орфографии
def correct_spelling(text):
    words = text.split()
    corrected_text = []
    for word in words:
        corrected_word = spell.correction(word)
        corrected_text.append(corrected_word)
    return ' '.join(corrected_text)

# Использование модели для грамматических и лексических ошибок
def correct_text(text):
    # Применение орфографической коррекции
    text = correct_spelling(text)
    
    # Применение модели spacy для лексического и грамматического анализа
    doc = nlp(text)
    corrected_tokens = []
    
    for token in doc:
        # Для примера заменяем только некоторые ошибки
        if token.pos_ == 'VERB' and token.tag_ != 'VERB_CORRECT_FORM':
            corrected_tokens.append(token.lemma_)  # Ставим глаголы в правильную форму
        else:
            corrected_tokens.append(token.text)
    
    corrected_text = ' '.join(corrected_tokens)
    return corrected_text

# Тест программы
input_text = "Я хачу сделат програму котороя правет ошипки в тексте"
corrected_text = correct_text(input_text)
print("Исправленный текст:", corrected_text)

import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Загрузка модели и токенизатора GPT-2
tokenizer = GPT2Tokenizer.from_pretrained('rugpt2large')
model = GPT2LMHeadModel.from_pretrained('rugpt2large')

# Функция для разбивки текста на предложения
def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

# Фильтрация диалогов и разговорных конструкций
def is_dialogue(text):
    # Поиск конструкций с тире, кавычками или словами, характерными для диалогов
    dialogue_keywords = ["сказал", "спросил", "ответил", "прошептал", "воскликнул"]
    
    if re.search(r'["“”]', text):  # Проверяем наличие кавычек
        return True
    if text.startswith("–"):  # Проверяем наличие тире в начале строки
        return True
    if any(keyword in text.lower() for keyword in dialogue_keywords):  # Проверяем ключевые слова
        return True
    return False

# Функция для дополнения каждого предложения с помощью GPT-2, исключая диалоги
def expand_sentence(sentence, model, tokenizer):
    input_ids = tokenizer.encode(sentence, return_tensors='pt')
    outputs = model.generate(
        input_ids,
        max_length=50,  # Длина дополнения
        num_beams=5,    # Количество лучей для генерации
        temperature=0.5,  # Более низкая температура для формального текста
        top_p=0.8,        # Ограничение для разнообразия
        no_repeat_ngram_size=3,
        do_sample=True
    )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Фильтрация текста на наличие диалогов или разговорных конструкций
    if is_dialogue(generated_text):
        # Если обнаружены диалоги, возвращаем оригинальное предложение
        return sentence
    else:
        return generated_text

# Вводный текст (абзац)
paragraph = "Технологии развиваются. Мы живем в удивительное время. Искусственный интеллект уже меняет нашу жизнь."

# Разбиваем абзац на предложения
sentences = split_into_sentences(paragraph)

# Дополняем каждое предложение, избегая диалогов и разговорных конструкций
expanded_sentences = [expand_sentence(sentence, model, tokenizer) for sentence in sentences]

# Соединяем предложения обратно в абзац
expanded_paragraph = ' '.join(expanded_sentences)

print(expanded_paragraph)

import spacy
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Загружаем модель spaCy для русского языка
nlp = spacy.load("ru_core_news_lg")

# Подготовка модели ruGPT-3 и токенизатора
model_name = "sberbank-ai/rugpt3medium_based_on_gpt2"  # Русская GPT-3
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def expand_sentence(sentence, max_length=100, temperature=0.8):
    # Токенизация предложения
    inputs = tokenizer.encode(sentence, return_tensors='pt')

    # Генерация расширенного текста для одного предложения
    outputs = model.generate(
        inputs,
        max_length=max_length,
        do_sample=True,  # Использование сэмплинга для креативного текста
        temperature=temperature,  # Параметр для настройки креативности
        top_p=0.95,
        num_return_sequences=1  # Количество генерируемых вариантов (оставим 1)
    )

    # Декодирование сгенерированного текста
    expanded_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return expanded_sentence

def expand_paragraph(input_paragraph):
    # Токенизация текста на предложения с помощью spaCy
    doc = nlp(input_paragraph)
    sentences = [sent.text for sent in doc.sents]
    
    expanded_sentences = []
    for sentence in sentences:
        # Расширение каждого предложения
        expanded_sentence = expand_sentence(sentence)
        expanded_sentences.append(expanded_sentence)

    # Объединение всех расширенных предложений в один текст
    expanded_paragraph = ' '.join(expanded_sentences)
    return expanded_paragraph

# Пример использования
input_paragraph = "В начале осени дни становятся короче, а ночи длиннее. Листья на деревьях начинают менять цвет, становясь ярко-желтыми и красными."
expanded_text = expand_paragraph(input_paragraph)

print("Исходный текст:", input_paragraph)
print("Расширенный текст:", expanded_text)

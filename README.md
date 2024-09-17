import spacy
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Загружаем spaCy модель для русского языка
nlp = spacy.load("ru_core_news_lg")

# Загружаем ruGPT-3 модель и токенизатор
model_name = "sberbank-ai/rugpt3medium_based_on_gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Функция для генерации текста
def expand_sentence(sentence, max_length=50, temperature=0.7):
    # Токенизация предложения
    inputs = tokenizer.encode(sentence, return_tensors='pt')

    # Генерация текста на основе предложения
    outputs = model.generate(
        inputs,
        max_length=max_length,      # Максимальная длина генерируемого текста
        do_sample=True,             # Включаем сэмплинг для креативности
        temperature=temperature,    # Контролируем "творческость"
        top_p=0.9,                  # Используем метод nucleus sampling
        num_return_sequences=1      # Оставляем только один результат
    )

    # Декодирование сгенерированного текста
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Возвращаем расширенное предложение (без исходного повторения)
    return generated_text

# Функция для расширения абзаца
def expand_paragraph(paragraph):
    # Разбиваем исходный текст на предложения с помощью spaCy
    doc = nlp(paragraph)
    expanded_sentences = []

    for sent in doc.sents:
        # Расширяем каждое предложение
        expanded_sentence = expand_sentence(sent.text)
        expanded_sentences.append(expanded_sentence)

    # Соединяем предложения в один абзац
    expanded_paragraph = ' '.join(expanded_sentences)
    return expanded_paragraph

# Пример использования
input_paragraph = "В начале осени дни становятся короче, а ночи длиннее. Листья на деревьях начинают менять цвет, становясь ярко-желтыми и красными."

expanded_text = expand_paragraph(input_paragraph)

print("Исходный текст:", input_paragraph)
print("Расширенный текст:", expanded_text)

import spacy
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Загружаем модель spaCy для русского языка
nlp = spacy.load("ru_core_news_lg")

# Загружаем ruGPT-3 модель и токенизатор
model_name = "sberbank-ai/rugpt3medium_based_on_gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Функция для генерации расширенного предложения
def expand_sentence(sentence, max_length=60, temperature=0.6, top_p=0.9):
    # Токенизация предложения
    inputs = tokenizer.encode(sentence, return_tensors='pt')

    # Генерация текста на основе предложения
    outputs = model.generate(
        inputs,
        max_length=max_length,      # Максимальная длина генерируемого текста
        do_sample=True,             # Включаем сэмплинг для большей креативности
        temperature=temperature,    # Контролируем степень "творчества"
        top_p=top_p,                # nucleus sampling, выбираем вероятные слова
        num_return_sequences=1      # Оставляем только один результат
    )

    # Декодирование сгенерированного текста
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Возвращаем только расширенное предложение
    return generated_text

# Функция для расширения каждого предложения в абзаце
def expand_paragraph(paragraph):
    doc = nlp(paragraph)  # Разбиваем текст на предложения
    expanded_sentences = []

    for sent in doc.sents:
        original_sentence = sent.text
        expanded_sentence = expand_sentence(original_sentence)
        expanded_sentences.append(expanded_sentence)

    # Собираем предложения в один абзац
    expanded_paragraph = ' '.join(expanded_sentences)
    return expanded_paragraph

# Пример использования
input_paragraph = "В ходе выполнения регулярных технических работ по обновлению серверного оборудования 5 сентября 2023 года был выявлен ряд неполадок в системе резервного копирования данных."

expanded_text = expand_paragraph(input_paragraph)

print("Исходный текст:", input_paragraph)
print("Расширенный текст:", expanded_text)

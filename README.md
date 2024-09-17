from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Загрузка модели и токенизатора
model_name = "sberbank-ai/rugpt3medium_based_on_gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def expand_text(input_text, max_length=300, temperature=0.9):
    # Токенизация входного текста
    inputs = tokenizer.encode(input_text, return_tensors='pt')

    # Генерация текста
    outputs = model.generate(
        inputs,
        max_length=max_length,
        do_sample=True,  # Используем сэмплинг для более креативного текста
        temperature=temperature,  # Настройка креативности
        top_p=0.95,  # Выбираем "умные" токены
        num_return_sequences=1  # Генерируем только 1 вариант
    )

    # Декодирование сгенерированного текста
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Пример использования
input_paragraph = "В начале осени дни становятся короче, а ночи длиннее. Листья на деревьях начинают менять цвет, становясь ярко-желтыми и красными."
expanded_text = expand_text(input_paragraph)

print("Исходный текст:", input_paragraph)
print("Расширенный текст:", expanded_text)

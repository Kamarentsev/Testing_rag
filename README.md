from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Загрузка модели и токенизатора
tokenizer = GPT2Tokenizer.from_pretrained('rugpt2large')
model = GPT2LMHeadModel.from_pretrained('rugpt2large')

# Ввод текста
input_text = "Технологии развиваются"

# Токенизация текста
input_ids = tokenizer.encode(input_text, return_tensors='pt')

# Генерация текста с параметрами, предотвращающими повторения
outputs = model.generate(
    input_ids,
    max_length=100,           # Увеличиваем максимальную длину
    num_beams=5,              # Используем несколько лучей для генерации
    temperature=0.7,          # Контроль над случайностью, ниже для более точного текста
    top_p=0.9,                # Nucleus sampling для разнообразия
    no_repeat_ngram_size=3,   # Предотвращаем повторения n-грамм (например, триграммы)
    do_sample=True            # Включаем выборку токенов для большей креативности
)

# Декодирование текста
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(generated_text)

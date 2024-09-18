import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Загрузка модели и токенизатора GPT-2
tokenizer = GPT2Tokenizer.from_pretrained('rugpt2large')
model = GPT2LMHeadModel.from_pretrained('rugpt2large')

# Функция для разбивки текста на предложения
def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

# Функция для дополнения каждого предложения с помощью GPT-2
def expand_sentence(sentence, model, tokenizer):
    input_ids = tokenizer.encode(sentence, return_tensors='pt')
    outputs = model.generate(
        input_ids,
        max_length=50,  # Длина дополнения
        num_beams=5,    # Количество лучей для генерации
        temperature=0.7,
        top_p=0.9,
        no_repeat_ngram_size=3,
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Вводный текст (абзац)
paragraph = "Технологии развиваются. Мы живем в удивительное время. Искусственный интеллект уже меняет нашу жизнь."

# Разбиваем абзац на предложения
sentences = split_into_sentences(paragraph)

# Дополняем каждое предложение
expanded_sentences = [expand_sentence(sentence, model, tokenizer) for sentence in sentences]

# Соединяем предложения обратно в абзац
expanded_paragraph = ' '.join(expanded_sentences)

print(expanded_paragraph)

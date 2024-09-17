from transformers import GPT2LMHeadModel, GPT2Tokenizer
import nltk

# Подготовка модели и токенизатора
model_name = "sberbank-ai/rugpt3medium_based_on_gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Загружаем пунктуационный пакет NLTK
nltk.download('punkt')

def expand_sentence(sentence, max_length=100, temperature=0.8):
    # Токенизация одного предложения
    inputs = tokenizer.encode(sentence, return_tensors='pt')

    # Генерация для одного предложения
    outputs = model.generate(
        inputs,
        max_length=max_length,
        do_sample=True,
        temperature=temperature,
        top_p=0.95,
        num_return_sequences=1
    )

    # Декодирование результата
    expanded_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return expanded_sentence

def expand_paragraph(input_paragraph):
    # Разбивка текста на предложения
    sentences = nltk.sent_tokenize(input_paragraph)
    
    expanded_sentences = []
    for sentence in sentences:
        # Расширение каждого предложения
        expanded_sentence = expand_sentence(sentence)
        expanded_sentences.append(expanded_sentence)

    # Соединение расширенных предложений обратно в текст
    expanded_paragraph = ' '.join(expanded_sentences)
    return expanded_paragraph

# Пример использования
input_paragraph = "В начале осени дни становятся короче, а ночи длиннее. Листья на деревьях начинают менять цвет, становясь ярко-желтыми и красными."
expanded_text = expand_paragraph(input_paragraph)

print("Исходный текст:", input_paragraph)
print("Расширенный текст:", expanded_text)

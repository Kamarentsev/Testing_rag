from transformers import AutoTokenizer, AutoModelForCausalLM

# Загружаем модель и токенайзер
model_name = "sberbank-ai/rugpt3medium_based_on_gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_text(prompt, max_length=100):
    # Токенизация входного текста
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    
    # Генерация текста
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)
    
    # Декодируем и возвращаем результат
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Пример использования:
user_query = input("Введите запрос: ")
generated_text = generate_text(user_query)
print(generated_text)

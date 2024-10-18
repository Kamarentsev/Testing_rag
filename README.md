from transformers import AutoTokenizer, AutoModelForCausalLM

# Загружаем модель и токенайзер
model_name = "sberbank-ai/rugpt3medium_based_on_gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_text_with_keywords(keywords, max_length=100):
    # Объединяем ключевые слова в строку для подачи модели
    prompt = " ".join(keywords)
    
    # Токенизация ключевых слов
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    
    # Генерация текста с более низкой "творческой свободой"
    outputs = model.generate(
        inputs, 
        max_length=max_length, 
        num_return_sequences=1, 
        no_repeat_ngram_size=2, 
        temperature=0.3,  # Уменьшение креативности
        top_p=0.8,  # Ограничение на менее вероятные продолжения
        do_sample=True
    )
    
    # Декодируем результат
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Пример использования:
keywords = ["сбой", "система безопасности", "утечка данных", "последствия", "устранение"]
generated_text = generate_text_with_keywords(keywords)
print(generated_text)

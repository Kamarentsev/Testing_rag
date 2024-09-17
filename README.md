from transformers import AutoModelForCausalLM, AutoTokenizer

# Загружаем модель и токенизатор
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")

# Пример текста, который нужно дополнить
text = "Москва — столица России. В городе много музеев. Архитектура Москвы сочетает старинные и современные здания."

# Подготовка подсказки для модели
prompt = f"Расширь этот текст, добавив больше деталей в каждое предложение: {text}"

# Токенизация текста
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

# Генерация ответа модели
outputs = model.generate(input_ids, max_length=500, do_sample=True)

# Декодирование и вывод текста
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)

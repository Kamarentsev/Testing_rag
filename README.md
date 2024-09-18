from transformers import T5ForConditionalGeneration, T5Tokenizer

# Загрузка модели и токенизатора
tokenizer = T5Tokenizer.from_pretrained('T5')
model = T5ForConditionalGeneration.from_pretrained('T5')

# Ввод текста
input_text = "расширь это предложение: Технологии развиваются."

# Препроцессинг текста для модели
input_ids = tokenizer.encode(input_text, return_tensors='pt')

# Генерация текста
outputs = model.generate(input_ids, max_length=50, num_beams=5, early_stopping=True)

# Декодирование выходного текста
output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(output_text)

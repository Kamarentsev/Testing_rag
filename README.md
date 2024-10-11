from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Загрузка модели и токенайзера
model_name = "ai-forever/rugpt2large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_text(prompt, max_length=100, temperature=0.7, top_p=0.9):
    # Токенизация запроса
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    # Генерация текста
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True
        )
    
    # Декодирование сгенерированного текста
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Пример использования функции
prompt = "Сбой в системе безопасности"
generated_text = generate_text(prompt)
print(generated_text)

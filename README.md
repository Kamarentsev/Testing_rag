from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Загрузка модели и токенайзера
model_name = "ai-forever/rugpt2large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_text(prompt, max_length=200, temperature=0.4, top_p=0.8, top_k=50):
    # Задать более конкретный ввод для коммерческого стиля
    formal_prompt = (f"Уважаемая служба поддержки,\n\n"
                     f"В связи с возникшим сбоем в системе безопасности, "
                     f"обращаюсь с жалобой. Был обнаружен {prompt}, "
                     f"что привело к нарушению нормальной работы.\n\n"
                     f"Прошу принять необходимые меры для устранения данного сбоя "
                     f"и предоставления разъяснений по возникшей ситуации.\n\n"
                     f"С уважением, клиент.")
    
    # Токенизация запроса
    input_ids = tokenizer.encode(formal_prompt, return_tensors="pt")
    
    # Генерация текста
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            repetition_penalty=1.2
        )
    
    # Декодирование сгенерированного текста
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Пример использования функции
prompt = "сбой в системе безопасности"
generated_text = generate_text(prompt)
print(generated_text)


from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Загрузка модели и токенайзера
model_name = "ai-forever/rugpt2large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_formal_text(prompt, max_length=150, temperature=0.3, top_p=0.8, top_k=50):
    # Шаблон официального текста
    formal_prompt = (f"Уважаемая служба поддержки,\n\n"
                     f"Сообщаю о возникшем инциденте, связанном с {prompt}. "
                     f"Данный сбой нарушил работу системы безопасности, что привело к потенциальным рискам для клиентов.\n\n"
                     f"Прошу принять незамедлительные меры по устранению проблемы и предоставлению отчета о произошедшем. "
                     f"Пожалуйста, свяжитесь со мной по контактным данным для дальнейшего разъяснения ситуации.\n\n"
                     f"С уважением,\nКлиент")

    # Токенизация
    input_ids = tokenizer.encode(formal_prompt, return_tensors="pt")
    
    # Генерация текста
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length + len(input_ids[0]),
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=False,  # Избегаем случайного ответа для сдержанного тона
            repetition_penalty=1.3
        )
    
    # Декодирование сгенерированного текста
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Пример использования функции
prompt = "сбоем в системе безопасности"
generated_text = generate_formal_text(prompt)
print(generated_text)

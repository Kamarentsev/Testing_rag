from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Загрузка модели и токенайзера
model_name = "ai-forever/rugpt2large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_banking_text(prompt, max_length=150, temperature=0.3, top_p=0.8, top_k=50):
    # Универсальный шаблон для различных банковских запросов
    template = (f"Уважаемый отдел поддержки,\n\n"
                f"Сообщаю о возникшей проблеме, связанной с {prompt}. "
                f"Эта ситуация вызвала затруднения в использовании услуг банка и может негативно сказаться на "
                f"доверии клиентов. Прошу оперативно принять меры для разрешения данной проблемы и предоставить разъяснения по поводу возникшей ситуации.\n\n"
                f"Прошу также рассмотреть возможность возмещения возможных убытков, связанных с данным инцидентом.\n\n"
                f"С уважением,\nКлиент банка")

    # Токенизация
    input_ids = tokenizer.encode(template, return_tensors="pt")
    
    # Генерация текста
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length + len(input_ids[0]),
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=False,
            repetition_penalty=1.3
        )
    
    # Декодирование сгенерированного текста
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Пример использования функции
prompt = "неполадками в системе безопасности"
generated_text = generate_banking_text(prompt)
print(generated_text)

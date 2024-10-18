import random
import nltk
from nltk import word_tokenize
from collections import defaultdict

# Загрузите данные для токенизации, если еще не скачаны
nltk.download('punkt')

class MarkovChainTextGenerator:
    def __init__(self, text):
        self.words = word_tokenize(text.lower(), language='russian')  # Укажите язык как русский
        self.word_dict = defaultdict(list)
        self.build_chain()

    def build_chain(self):
        for i in range(len(self.words) - 1):
            self.word_dict[self.words[i]].append(self.words[i + 1])

    def generate_text(self, input_words, num_sentences=2):
        input_words = input_words.lower().split()
        start_word = random.choice(input_words)
        generated_sentences = []

        for _ in range(num_sentences):
            current_word = start_word
            sentence = []

            while current_word not in ['.', '!', '?'] and len(sentence) < 15:  # Ограничение на количество слов
                sentence.append(current_word)
                next_words = self.word_dict.get(current_word, [])
                if not next_words:
                    break
                current_word = random.choice(next_words)

            generated_sentences.append(' '.join(sentence).capitalize() + '.')  # Форматирование предложения

        return ' '.join(generated_sentences)


# Пример использования
if __name__ == "__main__":
    text_corpus = """
    Сбой в системе безопасности привел к потере данных. 
    Необходимо провести аудит безопасности. 
    Данные должны быть восстановлены как можно скорее. 
    Команда работает над решением проблемы. 
    Рекомендуется обновить систему безопасности для предотвращения повторных сбоев.
    """
    
    generator = MarkovChainTextGenerator(text_corpus)
    input_query = "сбой в системе безопасности"
    generated_text = generator.generate_text(input_query, num_sentences=3)
    print(generated_text)

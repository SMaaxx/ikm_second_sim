import random
from faker import Faker

class LinkedList:
    # Реализация списка
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

class Node:
    # Реализация элемента списка
    def __init__(self, data):
        self.data = data
        self.next = None

class WordChain:
    def __init__(self, words):
        self.words = LinkedList()
        for word in words:
            self.words.append(word)

    # Получение последней буквы
    def last_significant_letter(self, word):
        if word[-1] == 'ь' and len(word) > 1:
            return word[-2]
        return word[-1]

    # Поиск цепочки
    def find_chain(self):
        words_list = self.words.to_list()
        n = len(words_list)
        used = [False] * n
        result_chain = LinkedList()

        def backtrack(chain_list):
            if len(chain_list) == n:
                if self.last_significant_letter(chain_list[-1]) == chain_list[0][0]:
                    return chain_list
                return None

            last_letter = self.last_significant_letter(chain_list[-1])
            for i in range(n):
                if not used[i] and words_list[i][0] == last_letter:
                    used[i] = True
                    res = backtrack(chain_list + [words_list[i]])
                    if res:
                        return res
                    used[i] = False
            return None

        for i in range(n):
            used[i] = True
            res = backtrack([words_list[i]])
            if res:
                for word in res:
                    result_chain.append(word)
                return result_chain.to_list()
            used[i] = False

        return None

class InputHandler:
    def __init__(self):
        self.fake = Faker('ru_RU')

    # Ввод с консоли
    def get_words_from_console(self):
        input_str = input("Введите слова через пробел: ")
        return [w.lower() for w in input_str.split() if w]

    # Ввод из файла
    def get_words_from_file(self, filename="words.txt"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                input_str = f.readline().strip()
                return [w.lower() for w in input_str.split() if w]
        except FileNotFoundError:
            print(f"\nОшибка: файл '{filename}' не найден.")
            return None

    # Генерация
    def generate_words(self, num_words=10):
        words = []
        for _ in range(num_words):
            word = self.fake.word()
            words.append(word.lower())
        print("\nСгенерированные слова:", ' '.join(words))
        return words

class Menu:
    def __init__(self):
        self.input_handler = InputHandler()

    # Реализация меню
    def run(self):
        while True:
            print("\nМеню игры в слова:")
            print("1. Ввести слова с консоли")
            print("2. Считать слова из файла")
            print("3. Сгенерировать слова через Faker")
            print("4. Выход")

            choice = input("Выберите пункт (1-4): ")
            words = None  # Инициализация переменной

            if choice == '1':
                words = self.input_handler.get_words_from_console()
            elif choice == '2':
                filename = input("Введите имя файла: ")
                words = self.input_handler.get_words_from_file(filename)
                if words is None:
                    continue
                print("\nСчитанные слова:", ' '.join(words))
            elif choice == '3':
                try:
                    num_words = int(input("Введите количество слов для генерации: "))
                except ValueError:
                    print("Ошибка: введите целое число.")
                    continue
                words = self.input_handler.generate_words(num_words)
            elif choice == '4':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Пожалуйста, введите число от 1 до 4.")
                continue

            if words:
                word_chain = WordChain(words)
                chain = word_chain.find_chain()

                if chain:
                    print("\nНайденная цепочка:")
                    print(' -> '.join(chain))
                else:
                    print("\nЦепочка не найдена.")

if __name__ == "__main__":
    menu = Menu()
    menu.run()

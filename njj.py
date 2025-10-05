from pygame import *
from random import (randint)           # Імпортуємо функцію randint для генерації випадкових чисел

init()                                # Ініціалізуємо всі модулі pygame
window_size = 1200, 800               # Задаємо розмір вікна гри (ширина 1200, висота 800)
window = display.set_mode(window_size) # Створюємо вікно гри з заданими розмірами
clock = time.Clock()                  # Створюємо об’єкт годинника для контролю FPS
player_rect = Rect(150, window_size[1]//2-100, 100, 100)
# Створюємо прямокутник-гравця: x=150, y=центр по вертикалі мінус 100, ширина=100, висота=100

def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=650):
    # Функція створення перешкод-труб
    pipes = []                        # Порожній список для зберігання пар труб
    start_x = window_size[0]           # Початкове розташування труб по осі X (за правою межею вікна)
    for i in range(count):             # Створюємо потрібну кількість пар труб
        height = randint(min_height, max_height)   # Випадкова висота верхньої труби
        top_pipe = Rect(start_x, 0, pipe_width, height)  # Верхня труба
        bottom_pipe = Rect(start_x, height + gap, pipe_width, window_size[1] - (height + gap))
        # Нижня труба, розташована нижче зазорів
        pipes.extend([top_pipe, bottom_pipe])     # Додаємо обидві труби у список
        start_x += distance                       # Зсуваємо наступну пару труб вправо
    return pipes                                  # Повертаємо список усіх труб

pies = generate_pipes(150)             # Генеруємо початковий набір труб
main_font = font.Font(None, 100)       # Створюємо об’єкт шрифту для відображення рахунку
score = 0                              # Лічильник очок
lose = False                           # Прапорець стану поразки
y_vel = 2                               # Початкова вертикальна швидкість падіння гравця

while True:                             # Основний ігровий цикл
    for e in event.get():               # Обробка подій
        if e.type == QUIT:              # Якщо натиснули на кнопку закриття вікна
            quit()                      # Завершуємо програму

    window.fill('sky blue')             # Заповнюємо фон кольором неба
    draw.rect(window, 'red', player_rect) # Малюємо гравця (червоний прямокутник)

    for pie in pies[:]:                 # Проходимося копією списку труб
        if not lose:                    # Якщо гра не програна
            pie.x -= 10                 # Зсуваємо трубу вліво
        draw.rect(window, 'green', pie) # Малюємо трубу зеленим кольором
        if pie.x <= -100:               # Якщо труба вийшла за межі екрана
            pies.remove(pie)            # Видаляємо її зі списку
            score += 0.5                # Додаємо 0.5 бала (пара труб = 1 бал)
        if player_rect.colliderect(pie):# Перевірка зіткнення гравця з трубою
            lose = True                 # Якщо є зіткнення – гра програна

    if len(pies) < 8:                   # Якщо труб менше 8
        pies += generate_pipes(150)     # Генеруємо нову партію труб

    score_text = main_font.render(f'{int(score)}', 1, 'black') # Рендеримо текст рахунку
    center_text = window_size[0]//2 - score_text.get_rect().w  # Вираховуємо позицію по центру
    window.blit(score_text, (center_text, 40))  # Виводимо рахунок на екран

    display.update()                    # Оновлюємо зображення на екрані
    clock.tick(60)                      # Обмежуємо цикл до 60 кадрів/сек

    keys = key.get_pressed()            # Зчитуємо стан усіх клавіш
    if keys[K_w] and not lose:          # Якщо натиснуто W і гра не програна
        player_rect.y -= 15             # Рухаємо гравця вгору
    if keys[K_s] and not lose:          # Якщо натиснуто S і гра не програна
        player_rect.y += 15             # Рухаємо гравця вниз
    if keys[K_r] and lose:              # Якщо натиснуто R і гра програна
        lose = False                    # Скидаємо стан програшу
        score = 0                       # Обнуляємо рахунок
        pies = generate_pipes(150)      # Створюємо нові труби
        player_rect.y = window_size[1]//2-100 # Повертаємо гравця у центр
        y_vel = 2                       # Скидаємо швидкість падіння

    if player_rect.y >= window_size[1] - player_rect.h:
        # Якщо гравець досяг нижньої межі екрана
        lose = True                     # Встановлюємо стан програшу

    if lose:                            # Якщо гра програна
        player_rect.y += y_vel          # Гравець починає падати
        y_vel *= 1.1                    # Швидкість падіння поступово збільшується

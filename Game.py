"""
Игра на Python с использованием Pygame.

Цель игры - управлять героем, избегая столкновений с вылетающими объектами (NIR, OOP, VKR).
Игрок может перемещать героя вверх и вниз, чтобы избежать столкновений. Каждые 10 секунд
скорость объектов увеличивается, что делает игру более сложной.

Игра начинается с экрана меню.Чтобы начать игру, нужно нажать пробел. 
При столкновении с объектами игра заканчивается, и отображается время, 
на протяжении которого игрок избегал столкновений.

"""
import pygame
from sys import exit
import time

# включаем модуль pygame
pygame.init()

# объявляем ширину и высоту экрана
width = 800
height = 400
# создаём экран игры
screen = pygame.display.set_mode((width, height))
# устанавливаем количество кадров в секунду
fps = 60
# создаём объект таймера
clock = pygame.time.Clock()

# добавляем счётчики для подсчёта времени в игре — это будут наши очки
start_time = 0
final_score = 0

# загружаем в переменные картинки из папки с нашим файлом
back_main_screen = pygame.image.load('code_game_back.jpg').convert()
back = pygame.image.load('code_game_back_floor.jpg').convert()

# даём название окну игры
pygame.display.set_caption('Моя жизнь')

# объявляем переменную-флаг для цикла игры
game = False

# создаём классы для объектов игры
class GameObject:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Hero(GameObject):
    def __init__(self, x, y):
        super().__init__('me.png', x, y)

class OOP(GameObject):
    def __init__(self, x, y):
        super().__init__('OOP.jpg', x, y)

class NIR(GameObject):
    def __init__(self, x, y):
        super().__init__('NIR.jpg', x, y)

class VKR(GameObject):
    def __init__(self, x, y):
        super().__init__('VKR.jpg', x, y)

# создаём экземпляры объектов
hero = Hero(75, 180)
nir = NIR(900, 70)
oop = OOP(900, 200)
vkr = VKR(900, 345)

# текст с названием игры
text_font = pygame.font.Font('prstartk.ttf', 30)
text_surface = text_font.render('My life', False, 'White')
text_name_rect = text_surface.get_rect(center=(400, 30))

# текст с сообщением о столкновении
text_font_collide = pygame.font.Font('prstartk.ttf', 50)
text_collide = text_font_collide.render('Thats all!!', False, 'Red')
text_collide_rect = text_collide.get_rect(center=(400, 200))

# текст главного меню
text_font_new_game = pygame.font.Font('prstartk.ttf', 20)
text_newgame_str1 = text_font_new_game.render('If you want to start,', False, 'Green')
text_newgame_rect1 = text_newgame_str1.get_rect(center=(400, 325))
text_newgame_str2 = text_font_new_game.render('press space', False, 'Green')
text_newgame_rect2 = text_newgame_str2.get_rect(center=(400, 350))

# текст для подсчёта очков
text_font_score = pygame.font.Font('prstartk.ttf', 15)
# текст для вывода очков при окончании игры
text_ts_font = pygame.font.Font('prstartk.ttf', 20)

# начальная скорость объектов
initial_speed = 4
speed = initial_speed
last_speed_increase_time = 0

# функция подсчёта очков
def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = text_font_score.render(f'{current_time // 1000}', False, 'Purple')
    score_rect = score_surface.get_rect(bottomright=(795, 395))
    screen.blit(score_surface, score_rect)

# Функция для сброса начальных параметров
def reset_game():
    global game, start_time, vkr_flag, oop_flag, speed

    # Сбросим флаги и состояние игры
    vkr_flag = False
    oop_flag = False
    game = False

    # Переместим объекты в начальное положение
    hero.rect.center = (75, 180)
    nir.rect.center = (900, 70)
    oop.rect.center = (900, 200)
    vkr.rect.center = (900, 345)

    # Сбросим скорость до начального значения
    speed = initial_speed

# запускаем функцию начального состояния игры
reset_game()

# запускаем бесконечный цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()
            game = True
            start_time = pygame.time.get_ticks()

    if game:
        current_time = pygame.time.get_ticks()
        # Проверяем, прошло ли 10 секунд с последнего увеличения скорости
        if current_time - last_speed_increase_time >= 10000:
            speed += 1  # Увеличиваем скорость
            last_speed_increase_time = current_time  # Обновляем время последнего увеличения

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            hero.rect.top -= 5
            if hero.rect.top <= 0:
                hero.rect.top = 0
        if keys[pygame.K_DOWN]:
            hero.rect.top += 5
            if hero.rect.bottom >= height:
                hero.rect.bottom = height

        # размещаем все поверхности на главном экране
        screen.blit(back, (0, 0))
        hero.draw(screen)
        nir.draw(screen)
        oop.draw(screen)
        vkr.draw(screen)

        # запускаем движение всех предметов
        nir.rect.left -= speed
        if nir.rect.left <= 400:
            vkr_flag = True
        if vkr_flag:
            vkr.rect.left -= speed

        if vkr.rect.left <= 400:
            oop_flag = True
        if oop_flag:
            oop.rect.left -= speed

        if nir.rect.right <= 0:
            nir.rect.left = 800
        if vkr.rect.right <= 0:
            vkr.rect.left = 800
        if oop.rect.right <= 0:
            oop.rect.left = 1000

        if (hero.rect.colliderect(nir.rect) or
                hero.rect.colliderect(vkr.rect) or
                hero.rect.colliderect(oop.rect)):
            screen.blit(text_collide, text_collide_rect)
            final_score = (pygame.time.get_ticks() - start_time) // 1000
            text_ts_text = text_ts_font.render(f'You held out for {final_score} sec', False, 'White')
            text_ts_rect = text_ts_text.get_rect(center=(400, 250))
            screen.blit(text_ts_text, text_ts_rect)

            pygame.display.flip()
            time.sleep(3)
            game = False

        display_score()
    else:
        screen.blit(back_main_screen, (0, 0))
        pygame.draw.rect(back_main_screen, 'Black', (100, 300, 600, 80))
        screen.blit(text_newgame_str1, text_newgame_rect1)
        screen.blit(text_newgame_str2, text_newgame_rect2)
        # Отображаем название игры в главном меню
        screen.blit(text_surface, text_name_rect)

    pygame.display.update()
    clock.tick(fps)

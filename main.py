import pygame
import time
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1690, 1080
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GRAY = (169, 169, 169)

# Параметры персонажа
player_size = 40
player_speed = 7
gravity = 1
jump_strength = 15

# Параметры подземелья
tile_size = 50


# Генерация случайного подземелья
def generate_dungeon(width, height):
    dungeon = []
    for y in range(height):
        row = ""
        for x in range(width):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                row += "1"
            else:
                row += "1" if random.random() < 0.2 else "0"
        dungeon.append(row)
    return dungeon


# Инициализация персонажа
def init_player():
    return {
        "x": 0,
        "y": HEIGHT - player_size,
        "vel_y": 0,
        "on_ground": False
    }


player = init_player()


# Проверка коллизий
def check_collision(player_rect, dungeon):
    dungeon_height = len(dungeon)
    dungeon_width = len(dungeon[0])
    for y in range(dungeon_height):
        for x in range(dungeon_width):
            if dungeon[y][x] == "1":
                tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if player_rect.colliderect(tile_rect):
                    return True
    return False


# Отрисовка подземелья
def draw_dungeon(dungeon):
    dungeon_height = len(dungeon)
    dungeon_width = len(dungeon[0])
    for y in range(dungeon_height):
        for x in range(dungeon_width):
            if dungeon[y][x] == "1":
                pygame.draw.rect(win, WHITE, (x * tile_size, y * tile_size, tile_size, tile_size))


# Главное меню
def main_menu():
    while True:
        win.fill(BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render("Dungeon Game", True, WHITE)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

        font = pygame.font.Font(None, 56)
        play_text = font.render("Играть", True, WHITE)
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(play_text, play_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    game_loop()

        pygame.display.update()


# Основной цикл игры
def game_loop():
    player = init_player()
    start_time = time.time()
    dungeon = generate_dungeon(WIDTH // tile_size, HEIGHT // tile_size)
    dungeon_height = len(dungeon)
    dungeon_width = len(dungeon[0])
    run = True
    while run:
        pygame.time.delay(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player["x"] - player_speed >= 0:
            player["x"] -= player_speed
            if check_collision(pygame.Rect(player["x"], player["y"], player_size, player_size), dungeon):
                player["x"] += player_speed
        if keys[pygame.K_d] and player["x"] + player_speed + player_size <= WIDTH:
            player["x"] += player_speed
            if check_collision(pygame.Rect(player["x"], player["y"], player_size, player_size), dungeon):
                player["x"] -= player_speed
        if keys[pygame.K_w] and player["on_ground"]:
            player["vel_y"] = -jump_strength
            player["on_ground"] = False
        if keys[pygame.K_r]:
            player = init_player()
            start_time = time.time()

        # Применение гравитации
        player["y"] += player["vel_y"]
        player["vel_y"] += gravity

        # Проверка коллизий по вертикали
        player_rect = pygame.Rect(player["x"], player["y"], player_size, player_size)
        if check_collision(player_rect, dungeon):
            if player["vel_y"] > 0:  # Падение
                player["y"] = (player["y"] // tile_size) * tile_size
                player["on_ground"] = True
            elif player["vel_y"] < 0:  # Прыжок
                player["y"] = (player["y"] // tile_size + 1) * tile_size
            player["vel_y"] = 0

        # Ограничение по высоте
        if player["y"] + player_size >= HEIGHT:
            player["y"] = HEIGHT - player_size
            player["on_ground"] = True

        # Проверка достижения конца уровня
        end_rect = pygame.Rect((dungeon_width - 2) * tile_size, (dungeon_height - 2) * tile_size, tile_size, tile_size)
        if player_rect.colliderect(end_rect):
            print("Уровень пройден!")
            run = False

        # Отрисовка подземелья
        win.fill(BLACK)
        draw_dungeon(dungeon)

        # Отрисовка персонажа
        pygame.draw.rect(win, RED, (player["x"], player["y"], player_size, player_size))

        # Отрисовка конца уровня
        pygame.draw.rect(win, GREEN, end_rect)

        # Отрисовка секундомера
        elapsed_time = int(time.time() - start_time)
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Время: {elapsed_time} сек", True, RED)
        win.blit(timer_text, (10, 10))

        pygame.display.update()

    pygame.quit()


# Запуск главного меню
main_menu()

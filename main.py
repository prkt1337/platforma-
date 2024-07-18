import pygame
import time
import random

pygame.init()

WIDTH, HEIGHT = 1690, 1080
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GRAY = (0, 1, 50)
SPIKE_COLOR = (255, 165, 0)

player_size = 40
player_speed = 7
gravity = 1
jump_strength = 15
max_health = 20
dash_distance = 150
dash_cooldown = 0.5
last_dash_time = 0

tile_size = 50
spike_size = tile_size // 2

# Загрузка спрайта для стен
wall_sprite = pygame.image.load('wall.jpg')
wall_sprite = pygame.transform.scale(wall_sprite, (tile_size, tile_size))

def generate_dungeon(width, height):
    dungeon = []
    for y in range(height):
        row = []
        for x in range(width):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                row.append("1")
            else:
                if random.random() < 0.05:
                    row.append("2")
                else:
                    row.append("1" if random.random() < 0.2 else "0")
        dungeon.append(row)
    for y in range(5, 8):
        for x in range(1, 4):
            dungeon[y][x] = "0"
    dungeon[8][1] = "1"
    dungeon[8][2] = "1"
    dungeon[8][3] = "1"
    return dungeon

def init_player():
    return {
        "x": tile_size * 2,
        "y": tile_size * 5,
        "vel_y": 0,
        "on_ground": False,
        "health": max_health
    }

player = init_player()

def check_collision(player_rect, dungeon):
    dungeon_height = len(dungeon)
    dungeon_width = len(dungeon[0])
    for y in range(dungeon_height):
        for x in range(dungeon_width):
            if dungeon[y][x] == "1":
                tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if player_rect.colliderect(tile_rect):
                    return "wall", None
            elif dungeon[y][x] == "2":
                spike_rect = pygame.Rect(x * tile_size + spike_size // 2, y * tile_size + spike_size // 2, spike_size, spike_size)
                if player_rect.colliderect(spike_rect):
                    return "spike", spike_rect
    return None, None

def draw_dungeon(dungeon):
    dungeon_height = len(dungeon)
    dungeon_width = len(dungeon[0])
    for y in range(dungeon_height):
        for x in range(dungeon_width):
            if dungeon[y][x] == "1":
                win.blit(wall_sprite, (x * tile_size, y * tile_size))
            elif dungeon[y][x] == "2":
                pygame.draw.rect(win, SPIKE_COLOR, (x * tile_size + spike_size // 2, y * tile_size + spike_size // 2, spike_size, spike_size))

def draw_health_bar(player):
    health_ratio = player["health"] / max_health
    pygame.draw.rect(win, RED, (10, 90, 200, 20))
    pygame.draw.rect(win, GREEN, (10, 90, 200 * health_ratio, 20))
    pygame.draw.rect(win, WHITE, (10, 90, 200, 20), 2)

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

        controls_text = font.render("WASD - управление, Q/E - рывок", True, WHITE)
        win.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    game_loop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

        pygame.display.update()

def pause_menu():
    font = pygame.font.Font(None, 74)
    pause_text = font.render("Пауза", True, WHITE)
    win.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
    pygame.display.update()

def main():
    global paused
    paused = False
    run = True
    start_time = time.time()
    total_pause_time = 0
    pause_start_time = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        pause_start_time = time.time()
                    else:
                        total_pause_time += time.time() - pause_start_time

        if paused:
            pause_menu()
            continue

        # Основной игровой код здесь

        pygame.display.update()

    pygame.quit()
# Основной цикл игры
def game_loop():
    player = init_player()
    start_time = time.time()
    dungeon = generate_dungeon(WIDTH // tile_size, HEIGHT // tile_size)
    dungeon_height = len(dungeon)
    dungeon_width = len(dungeon[0])
    room_count = 10
    max_rooms = 10
    reset_cooldown = 10
    last_dash_time = 0
    dash_duration = 0.2
    dash_speed = 20
    player_speed = 8
    normal_speed = player_speed
    dashing = False
    dash_direction = 0
    dash_start_time = 0
    run = True
    paused = False
    pause_start_time = 0
    total_pause_time = 0

    while run:
        pygame.time.delay(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not paused:
                        paused = True
                        pause_start_time = time.time()
                    else:
                        paused = False
                        total_pause_time += time.time() - pause_start_time

        if paused:
            pause_menu()
            continue

        keys = pygame.key.get_pressed()

        if not dashing:
            if keys[pygame.K_a] and player["x"] - player_speed >= 0:
                player["x"] -= player_speed
                if check_collision(pygame.Rect(player["x"], player["y"], player_size, player_size), dungeon)[0] == "wall":
                    player["x"] += player_speed
            if keys[pygame.K_d] and player["x"] + player_speed + player_size <= WIDTH:
                player["x"] += player_speed
                if check_collision(pygame.Rect(player["x"], player["y"], player_size, player_size), dungeon)[0] == "wall":
                    player["x"] -= player_speed
            if keys[pygame.K_w] and player["on_ground"]:
                player["vel_y"] = -jump_strength
                player["on_ground"] = False
            if keys[pygame.K_r] and time.time() - reset_cooldown >= 3:
                player = init_player()
                dungeon = generate_dungeon(WIDTH // tile_size, HEIGHT // tile_size)
                reset_cooldown = time.time()
            if keys[pygame.K_q] and not player["on_ground"] and time.time() - last_dash_time > 2:
                dashing = True
                dash_direction = -1
                dash_start_time = time.time()
                last_dash_time = time.time()
            if keys[pygame.K_e] and not player["on_ground"] and time.time() - last_dash_time > 2:
                dashing = True
                dash_direction = 1
                dash_start_time = time.time()
                last_dash_time = time.time()
        else:
            if time.time() - dash_start_time < dash_duration:
                player["x"] += dash_direction * dash_speed
                if check_collision(pygame.Rect(player["x"], player["y"], player_size, player_size), dungeon)[0] == "wall":
                    player["x"] -= dash_direction * dash_speed
                    dashing = False
                player["vel_y"] = 0
            else:
                dashing = False
                player_speed = normal_speed

        if not dashing:
            player["y"] += player["vel_y"]
            player["vel_y"] += gravity

        player_rect = pygame.Rect(player["x"], player["y"], player_size, player_size)
        collision, spike_rect = check_collision(player_rect, dungeon)
        if collision == "wall":
            if player["vel_y"] > 0:
                player["y"] = (player["y"] // tile_size) * tile_size
                player["on_ground"] = True
            elif player["vel_y"] < 0:
                player["y"] = (player["y"] // tile_size + 1) * tile_size
            player["vel_y"] = 0
        elif collision == "spike":
            player["health"] -= 10
            if player["health"] <= 0:
                run = False
                game_over()
            else:
                if player["x"] < spike_rect.x:
                    player["x"] -= tile_size
                else:
                    player["x"] += tile_size

        if player["y"] + player_size >= HEIGHT:
            player["y"] = HEIGHT - player_size
            player["on_ground"] = True
        end_rect = pygame.Rect((dungeon_width - 2) * tile_size, (dungeon_height - 2) * tile_size, tile_size, tile_size)
        if player_rect.colliderect(end_rect):
            room_count -= 1
            if room_count <= 0:
                run = False
                victory_screen(start_time)
            else:
                dungeon = generate_dungeon(WIDTH // tile_size, HEIGHT // tile_size)
                player = init_player()

        win.fill(BLACK)
        draw_dungeon(dungeon)
        pygame.draw.rect(win, GREEN, (end_rect.x, end_rect.y, tile_size, tile_size))
        pygame.draw.rect(win, (255, 0, 0), (player["x"], player["y"], player_size, player_size))
        draw_health_bar(player)

        elapsed_time = time.time() - start_time - total_pause_time
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Время: {int(elapsed_time)} сек", True, RED)
        win.blit(timer_text, (10, 10))

        room_text = font.render(f"Комнаты: {room_count}/{max_rooms}", True, RED)
        win.blit(room_text, (10, 50))

        pygame.display.update()

    pygame.quit()

# Экран победы
def victory_screen(start_time):
    total_time = time.time() - start_time
    win.fill(BLACK)
    font = pygame.font.Font(None, 74)
    victory_text = font.render("Поздравляем! Вы прошли все уровни!", True, GREEN)
    win.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2 - 20))
    total_time_text = font.render(f"Общее время: {int(total_time)} сек", True, GREEN)
    win.blit(total_time_text, (WIDTH // 2 - total_time_text.get_width() // 2, HEIGHT // 2 - total_time_text.get_height() // 2 + 20))
    pygame.display.update()

    # Ожидание нажатия любой клавиши для выхода с экрана победы
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                waiting = False

    main_menu()
# Экран поражения
def game_over():
    win.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Игра окончена", True, RED)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    time.sleep(3)
    main_menu()

main_menu()

import pygame
import random
import os


# Inicialização do Pygame
pygame.init()

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configurações da janela
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Destruir Naves")

# Carregamento das imagens
game_folder = os.path.dirname(os.path.abspath(__file__))
img_folder = os.path.join(game_folder, "assets")

background_img = pygame.image.load(
    os.path.join(img_folder, "background.png")).convert()
ship_img = pygame.image.load(os.path.join(
    img_folder, "spaceship.png")).convert_alpha()
enemy_img = pygame.image.load(os.path.join(
    img_folder, "enemyship.png")).convert_alpha()
bullet_img = pygame.image.load(os.path.join(
    img_folder, "bullet.png")).convert_alpha()
bonus_img = pygame.image.load(os.path.join(
    img_folder, "bonus.png")).convert_alpha()
life_img = pygame.image.load(os.path.join(
    img_folder, "life.png")).convert_alpha()
life_bonus_img = pygame.image.load(os.path.join(
    img_folder, "life-bonus.png")).convert_alpha()
speed_bonus_img = pygame.image.load(os.path.join(
    img_folder, "speed-bonus.png")).convert_alpha()
life_img = pygame.transform.scale(life_img, (24, 24))
enemy_img = pygame.transform.scale(enemy_img, (100, 100))
background_img = pygame.transform.scale(background_img, (800, 600))

# Classe para representar a nave


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ship_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.is_invulnerable = False
        self.invincible_timer = pygame.time.get_ticks()
        self.shooting = False
        self.bonus_bullets = 0
        self.level = 1
        self.shoot_delay = 500  # Tempo entre os disparos em milissegundos
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_multiplier = 1.0  # Multiplicador de velocidade dos disparosf

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # Verificar se a nave está invulnerável
        if self.is_invulnerable:
            # Verificar o tempo decorrido desde que ficou invulnerável
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_timer >= 3000:
                self.is_invulnerable = False

        # Permitir que o jogador atire mais projéteis se tiver bônus de tiros extras
        if self.bonus_bullets > 0:
            if self.shooting:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot_time >= self.shoot_delay:
                    self.shoot()
                    self.last_shot_time = current_time
        else:
            if self.shooting:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot_time >= self.shoot_delay * self.shoot_multiplier:
                    self.shoot()
                    self.last_shot_time = current_time

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

        # Ajustar a taxa de disparo com base no shoot_multiplier
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay *= self.shoot_multiplier
        self.shoot_multiplier = 1

# Classe para representar os projéteis


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Classe para representar os inimigos


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 5)
        self.speed_x = random.randrange(-1, 1)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)
            self.speed_x = random.randrange(-2, 2)


# Classe para representar os bônus
class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['speed'])
        if self.type == 'speed':
            self.image = pygame.transform.scale(speed_bonus_img, (24, 24))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 4)

    def check_collision(self, player):
        if pygame.sprite.collide_rect(self, player):
            return self.type
        return None


# Classe para representar as vidas extras
class Life(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(life_img, (24, 24))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 4)


# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
lives = pygame.sprite.Group()

player = Ship()
all_sprites.add(player)

# Variáveis de controle do jogo
score = 0
lives_count = 3
enemy_speed = 10  # Velocidade de queda inicial dos inimigos
enemy_count = 3  # Quantidade inicial de inimigos


# Adicionar inimigos
for _ in range(enemy_count):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Loop principal do jogo
running = True
clock = pygame.time.Clock()

# Define the font
font = pygame.font.Font(None, 36)

# Tela de "Jogar"
start_text = font.render("Pressione ESPAÇO para jogar", True, WHITE)
start_rect = start_text.get_rect()
start_rect.center = (WIDTH // 2, HEIGHT // 2)
window.blit(start_text, start_rect)
pygame.display.flip()

# Aguardar pela tecla ESPAÇO para começar o jogo
start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start = True

while running:
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 5
            elif event.key == pygame.K_SPACE:
                player.shooting = True
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.speed_x < 0:
                player.speed_x = 0
            elif event.key == pygame.K_RIGHT and player.speed_x > 0:
                player.speed_x = 0
            elif event.key == pygame.K_SPACE:
                player.shooting = False

    # Atualizar sprites
    all_sprites.update()

    if score > 10:
        enemy_count += 5
        score = 0

    if random.random() < 0.0002:
        bonus = Bonus()
        all_sprites.add(bonus)
        bonuses.add(bonus)

    # Adicionar vidas extras
    if random.random() < 0.0002:
        life = Life()
        all_sprites.add(life)
        lives.add(life)

    # Verificar colisões dos projéteis com os inimigos
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        0

    # Verificar colisões do jogador com os inimigos
    hits = pygame.sprite.spritecollide(
        player, enemies, False, pygame.sprite.collide_circle)
    if hits and not player.is_invulnerable:
        lives_count -= 1
        if lives_count == 0:
            running = False
        else:
            player.is_invulnerable = True
            player.invincible_timer = pygame.time.get_ticks()
            player.rect.centerx = WIDTH // 2
            player.rect.bottom = HEIGHT - 10

    # Verificar colisões do jogador com os bônus
    hits = pygame.sprite.spritecollide(player, bonuses, True)
    for hit in hits:
        player.shoot_multiplier = 0.55

    # Verificar colisões do jogador com as vidas extras
    hits = pygame.sprite.spritecollide(player, lives, True)
    for hit in hits:
        lives_count += 1
        life = Life()
        lives.add(life)

    # Limpar a tela
    window.blit(background_img, (0, 0))

    # Desenhar sprites
    all_sprites.draw(window)

    # Desenhar texto
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)
    window.blit(score_text, score_rect)

    for i in range(lives_count):
        life_rect = life_img.get_rect()
        life_rect.x = 10 + (30 * i)
        life_rect.y = 60
        window.blit(life_img, life_rect)

    # Atualizar tela
    pygame.display.flip()

    # Controlar a taxa de atualização
    clock.tick(60)

# Encerrar o Pygame
pygame.quit()

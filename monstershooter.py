import pyxel
import random

WIDTH, HEIGHT = 160, 120
pyxel.init(WIDTH, HEIGHT, fps=30)
PLAYER_SPEED = 2
BULLET_SPEED = 3
MAX_ENEMIES = 5
ENEMY_SPAWN_THRESHOLD = 3
HEALTH_BOOST_SPAWN_INTERVAL = 300
LAST_BOSS_SCORE_THRESHOLD = 30


pyxel.sound(0).set(notes='C3', tones='N', volumes='3', effects='N', speed=10)  # Sound for firing a bullet
pyxel.sound(1).set(notes='A3A2', tones='NP', volumes='3322', effects='N', speed=10)  # Sound for enemy hit
pyxel.sound(2).set(notes='C4C3', tones='N', volumes='3', effects='NN', speed=10)  # Game over sound
pyxel.sound(3).set(notes='E3E2', tones='N', volumes='3', effects='NN', speed=10)  # Game clear sound
pyxel.sound(4).set(notes='F3F2', tones='N', volumes='3', effects='NN', speed=10)  # Damage sound

pyxel.sound(6).set(
    notes='C3E3G3C4',  # Example notes (you can change this)
    tones='S',  # Sustain
    volumes='4444',  # Volume
    effects='NNNN',  # No effects
    speed=15  # ）
)



class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 20
        self.health = 3
        self.score = 0
        self.damage_flash_frames = 0 

    def update(self):
        global game_over, game_clear, game_started


        if not game_over and not game_clear:
            if not game_started:
                if pyxel.btnp(pyxel.KEY_S):
                    game_started = True
            else:
                if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
                    self.x -= PLAYER_SPEED
                if pyxel.btn(pyxel.KEY_RIGHT) and self.x < WIDTH - 8:
                    self.x += PLAYER_SPEED
                if pyxel.btnp(pyxel.KEY_SPACE):
                    # Play the bullet firing sound
                    pyxel.play(0, 0)
                    bullets.append(Bullet(self.x + 1, self.y - 5))
                if self.damage_flash_frames > 0:
                    self.damage_flash_frames -= 1
                    

    def draw(self):
        pyxel.line(self.x + 2, self.y - 6, self.x + 2, self.y - 1, 11)  # Body
        pyxel.line(self.x + 2, self.y - 6, self.x, self.y - 3, 11)  # Left arm
        pyxel.line(self.x + 2, self.y - 6, self.x + 4, self.y - 3, 11)  # Right arm
        pyxel.line(self.x + 2, self.y - 1, self.x, self.y + 2, 11)  # Left leg
        pyxel.line(self.x + 2, self.y - 1, self.x + 4, self.y + 2, 11)  # Right leg
        pyxel.line(self.x + 1, self.y - 3, self.x + 3, self.y - 3, 11)  # Mouth
        pyxel.rect(self.x + 2, self.y - 5, 1, 1, 11)  # Eye
    def take_damage(self):
        self.health -= 1
        pyxel.play(4, 4)  # Play damage sound
        self.damage_flash_frames = 10

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y -= BULLET_SPEED

    def draw(self):
        pyxel.rect(self.x, self.y, 2, 6, 12)

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 8)
        self.y = random.randint(0, HEIGHT // 2)
        self.hit = False
        self.speed = random.uniform(1, 3)

    def update(self):
        global game_over, game_clear
        if not game_over and not game_clear:
            self.y += self.speed

            if self.y > HEIGHT:
                self.y = 0
                self.x = random.randint(0, WIDTH - 8)
                self.hit = False

    def draw(self):
        if not self.hit:
            pyxel.rect(self.x, self.y, 8, 8, 8)

class HealthBoost:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 8)
        self.y = random.randint(0, HEIGHT // 2)

    def update(self):
        global player
        if not game_over and not game_clear:
            # Check collision with bullets
            for bullet in bullets:
                if (
                    bullet.x < self.x + 8
                    and bullet.x + 2 > self.x
                    and bullet.y < self.y + 8
                    and bullet.y + 6 > self.y
                ):
                    player.health = min(player.health + 1, 3)
                    health_boosts.remove(self)
                   

    def draw(self):
        pyxel.rect(self.x, self.y, 8, 8, 10)

def reset_game():
    global player, bullets, enemies, health_boosts, game_over, game_clear, game_started, frame_count
    player = Player()
    bullets = []
    enemies = [Enemy() for _ in range(MAX_ENEMIES)]
    health_boosts = []
    game_over = False
    game_clear = False
    game_started = False
    frame_count = 0

player = Player()
bullets = []
enemies = [Enemy() for _ in range(MAX_ENEMIES)]
health_boosts = []
game_over = False
game_clear = False
game_started = False
frame_count = 0

def update():
    global game_over, game_clear, enemies, health_boosts, game_started, frame_count

    frame_count += 1

    if not game_over and not game_clear:
        if not game_started:
            if pyxel.btnp(pyxel.KEY_S):
                game_started = True
        else:
            player.update()

            for bullet in bullets:
                bullet.update()

            for enemy in enemies:
                enemy.update()

                # Check collision with bullets
                for bullet in bullets:
                    if (
                        bullet.x < enemy.x + 8
                        and bullet.x + 2 > enemy.x
                        and bullet.y < enemy.y + 8
                        and bullet.y + 6 > enemy.y
                    ):
                        # Play the enemy hit sound
                        pyxel.play(1, 1)
                        enemy.hit = True
                        bullets.remove(bullet)
                        player.score += 1

                # Check collision with player
                if (
                    player.x < enemy.x + 8
                    and player.x + 4 > enemy.x
                    and player.y < enemy.y + 8
                    and player.y + 6 > enemy.y
                ):
                    player.health -= 1
                    enemy.hit = True

            # Remove hit enemies
            enemies = [enemy for enemy in enemies if not enemy.hit]

            # Spawn new enemies if below the threshold
            if len(enemies) < ENEMY_SPAWN_THRESHOLD:
                enemies.extend([Enemy() for _ in range(MAX_ENEMIES - len(enemies))])

            
            if frame_count % HEALTH_BOOST_SPAWN_INTERVAL == 0:
                health_boosts.append(HealthBoost())

            for health_boost in health_boosts:
                health_boost.update()

            if player.health <= 0:
                game_over = True
                pyxel.play(2, 2) 

          
            if player.score >= LAST_BOSS_SCORE_THRESHOLD:
                game_clear = True
                pyxel.play(3, 3) 

    if game_over or game_clear:
        if pyxel.btnp(pyxel.KEY_R):
            reset_game()

def reset_game():
    global player, bullets, enemies, health_boosts, game_over, game_clear, game_started, frame_count
    player = Player()
    bullets = []
    enemies = [Enemy() for _ in range(MAX_ENEMIES)]
    health_boosts = []
    game_over = False
    game_clear = False
    game_started = False
    frame_count = 0

def draw():
    pyxel.cls(0)

    for bullet in bullets:
        bullet.draw()

    player.draw()

    for enemy in enemies:
        enemy.draw()

    for health_boost in health_boosts:
        health_boost.draw()

    pyxel.text(5, 5, f"Health: {player.health}", 8)
    pyxel.text(WIDTH - 40, 5, f"Score: {player.score}", 8)

    if game_over:
        pyxel.text(WIDTH // 2 - 30, HEIGHT // 2, "Game Over", 8)
        pyxel.text(WIDTH // 2 - 40, HEIGHT // 2 + 10, "Press R to restart", 8)

    if game_clear:
        pyxel.text(WIDTH // 2 - 30, HEIGHT // 2, "Game Clear", 8)
        pyxel.text(WIDTH // 2 - 40, HEIGHT // 2 + 10, "Press R to restart", 8)

    if not game_over and not game_clear and not game_started:
        pyxel.text(WIDTH // 2 - 50, HEIGHT // 2 + 20, "Press S to start", 8)

pyxel.playm(0, loop=True)

pyxel.run(update, draw)

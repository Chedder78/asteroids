import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyberpunk Asteroids")

# Colors
BLACK = (0, 0, 0)
NEON_BLUE = (0, 195, 255)
NEON_PINK = (255, 0, 128)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (180, 0, 255)
DARK_BLUE = (10, 10, 40)

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.speed = 0
        self.rotation_speed = 4
        self.acceleration = 0.1
        self.max_speed = 5
        self.size = 20
        self.lives = 3
        self.invincible = 0
        self.shoot_cooldown = 0
        self.weapon_level = 1
        self.score = 0
        
    def rotate(self, direction):
        self.angle += self.rotation_speed * direction
        
    def accelerate(self):
        self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed
            
    def decelerate(self):
        self.speed -= self.acceleration / 2
        if self.speed < 0:
            self.speed = 0
            
    def update(self):
        # Move the player based on angle and speed
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        
        # Screen wrapping
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
            
        # Update cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1
            
    def draw(self):
        if self.invincible > 0 and self.invincible % 10 < 5:
            return  # Blink effect when invincible
            
        # Draw the player ship
        points = [
            (self.x + math.cos(math.radians(self.angle)) * self.size, 
             self.y + math.sin(math.radians(self.angle)) * self.size),
            (self.x + math.cos(math.radians(self.angle + 150)) * self.size, 
             self.y + math.sin(math.radians(self.angle + 150)) * self.size),
            (self.x + math.cos(math.radians(self.angle - 150)) * self.size, 
             self.y + math.sin(math.radians(self.angle - 150)) * self.size)
        ]
        pygame.draw.polygon(screen, NEON_BLUE, points)
        
        # Draw engine glow
        glow_points = [
            (self.x - math.cos(math.radians(self.angle)) * self.size * 0.7, 
             self.y - math.sin(math.radians(self.angle)) * self.size * 0.7),
            (self.x + math.cos(math.radians(self.angle + 150)) * self.size * 0.5, 
             self.y + math.sin(math.radians(self.angle + 150)) * self.size * 0.5),
            (self.x + math.cos(math.radians(self.angle - 150)) * self.size * 0.5, 
             self.y + math.sin(math.radians(self.angle - 150)) * self.size * 0.5)
        ]
        pygame.draw.polygon(screen, NEON_GREEN, glow_points, 1)
        
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 10
            bullets = []
            
            # Single shot for level 1
            if self.weapon_level == 1:
                bullets.append(Bullet(self.x, self.y, self.angle))
            # Triple shot for level 2
            elif self.weapon_level == 2:
                bullets.append(Bullet(self.x, self.y, self.angle))
                bullets.append(Bullet(self.x, self.y, self.angle - 10))
                bullets.append(Bullet(self.x, self.y, self.angle + 10))
            # Five-way shot for level 3
            elif self.weapon_level >= 3:
                bullets.append(Bullet(self.x, self.y, self.angle))
                bullets.append(Bullet(self.x, self.y, self.angle - 15))
                bullets.append(Bullet(self.x, self.y, self.angle + 15))
                bullets.append(Bullet(self.x, self.y, self.angle - 30))
                bullets.append(Bullet(self.x, self.y, self.angle + 30))
                
            return bullets
        return []

# Bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.lifetime = 60
        
    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.lifetime -= 1
        
        # Screen wrapping
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
            
        return self.lifetime <= 0
        
    def draw(self):
        pygame.draw.circle(screen, NEON_PINK, (int(self.x), int(self.y)), 3)
        # Draw a trail
        trail_x = self.x - math.cos(math.radians(self.angle)) * 5
        trail_y = self.y - math.sin(math.radians(self.angle)) * 5
        pygame.draw.line(screen, NEON_PURPLE, (self.x, self.y), (trail_x, trail_y), 1)

# Asteroid class
class Asteroid:
    def __init__(self, x=None, y=None, size=3):
        self.size = size  # 3=large, 2=medium, 1=small
        if x is None and y is None:
            # Spawn from the edge of the screen
            side = random.randint(0, 3)
            if side == 0:  # Top
                self.x = random.randint(0, WIDTH)
                self.y = 0
            elif side == 1:  # Right
                self.x = WIDTH
                self.y = random.randint(0, HEIGHT)
            elif side == 2:  # Bottom
                self.x = random.randint(0, WIDTH)
                self.y = HEIGHT
            else:  # Left
                self.x = 0
                self.y = random.randint(0, HEIGHT)
        else:
            self.x = x
            self.y = y
            
        self.angle = random.randint(0, 360)
        self.speed = random.uniform(0.5, 2.0)
        self.rotation = random.uniform(-1, 1)
        self.vertices = self.generate_vertices()
        self.health = size
        
    def generate_vertices(self):
        vertices = []
        num_vertices = random.randint(7, 12)
        radius = self.size * 15
        
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices
            distance = radius * random.uniform(0.8, 1.2)
            vertices.append((math.cos(angle) * distance, math.sin(angle) * distance))
            
        return vertices
        
    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        
        # Screen wrapping
        if self.x < -50:
            self.x = WIDTH + 50
        elif self.x > WIDTH + 50:
            self.x = -50
        if self.y < -50:
            self.y = HEIGHT + 50
        elif self.y > HEIGHT + 50:
            self.y = -50
            
    def draw(self):
        # Draw the asteroid
        points = []
        for vertex in self.vertices:
            rotated_x = vertex[0] * math.cos(math.radians(self.rotation)) - vertex[1] * math.sin(math.radians(self.rotation))
            rotated_y = vertex[0] * math.sin(math.radians(self.rotation)) + vertex[1] * math.cos(math.radians(self.rotation))
            points.append((self.x + rotated_x, self.y + rotated_y))
            
        pygame.draw.polygon(screen, NEON_GREEN, points, 2)
        
        # Draw inner details
        for i in range(len(points)):
            next_i = (i + 1) % len(points)
            mid_x = (points[i][0] + points[next_i][0]) / 2
            mid_y = (points[i][1] + points[next_i][1]) / 2
            center_x = (mid_x + self.x) / 2
            center_y = (mid_y + self.y) / 2
            pygame.draw.line(screen, NEON_PURPLE, (points[i][0], points[i][1]), (center_x, center_y), 1)
            
    def split(self):
        if self.size > 1:
            new_size = self.size - 1
            return [
                Asteroid(self.x, self.y, new_size),
                Asteroid(self.x, self.y, new_size)
            ]
        return []

# Power-up class
class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(["weapon", "shield", "life"])
        self.size = 10
        self.pulse = 0
        
    def update(self):
        self.pulse = (self.pulse + 0.1) % (2 * math.pi)
        
    def draw(self):
        # Pulse effect
        pulse_size = self.size + math.sin(self.pulse) * 3
        
        if self.type == "weapon":
            color = NEON_PINK
            # Draw a weapon icon
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(pulse_size), 2)
            pygame.draw.line(screen, color, (self.x - pulse_size, self.y), (self.x + pulse_size, self.y), 2)
            pygame.draw.line(screen, color, (self.x, self.y - pulse_size), (self.x, self.y + pulse_size), 2)
        elif self.type == "shield":
            color = NEON_BLUE
            # Draw a shield icon
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(pulse_size), 2)
            pygame.draw.arc(screen, color, (self.x - pulse_size, self.y - pulse_size, 
                                           pulse_size * 2, pulse_size * 2), 
                           math.pi/4, 3*math.pi/4, 2)
        elif self.type == "life":
            color = NEON_GREEN
            # Draw a heart icon
            pygame.draw.circle(screen, color, (int(self.x - pulse_size/2), int(self.y)), int(pulse_size/2), 2)
            pygame.draw.circle(screen, color, (int(self.x + pulse_size/2), int(self.y)), int(pulse_size/2), 2)
            points = [
                (self.x - pulse_size, self.y + pulse_size/3),
                (self.x, self.y + pulse_size),
                (self.x + pulse_size, self.y + pulse_size/3)
            ]
            pygame.draw.polygon(screen, color, points, 2)

# Particle effect class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 30
        self.color = color
        self.size = random.uniform(1, 3)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        return self.life <= 0
        
    def draw(self):
        alpha = int(255 * (self.life / 30))
        color = (self.color[0], self.color[1], self.color[2], alpha)
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (int(self.size), int(self.size)), int(self.size))
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.bullets = []
        self.asteroids = []
        self.powerups = []
        self.particles = []
        self.level = 1
        self.asteroids_count = 5
        self.game_over = False
        self.spawn_timer = 0
        self.font = pygame.font.SysFont('monospace', 24)
        self.title_font = pygame.font.SysFont('monospace', 48, bold=True)
        self.spawn_initial_asteroids()
        
    def spawn_initial_asteroids(self):
        for _ in range(self.asteroids_count):
            # Make sure asteroids don't spawn too close to the player
            while True:
                asteroid = Asteroid()
                dist = math.sqrt((asteroid.x - self.player.x)**2 + (asteroid.y - self.player.y)**2)
                if dist > 150:
                    self.asteroids.append(asteroid)
                    break
                    
    def update(self):
        if self.game_over:
            return
            
        self.player.update()
        
        # Update bullets
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
                
        # Update asteroids
        for asteroid in self.asteroids[:]:
            asteroid.update()
            
        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update()
            
        # Update particles
        for particle in self.particles[:]:
            if particle.update():
                self.particles.remove(particle)
                
        # Check bullet-asteroid collisions
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                dist = math.sqrt((bullet.x - asteroid.x)**2 + (bullet.y - asteroid.y)**2)
                if dist < asteroid.size * 15:
                    # Create explosion particles
                    for _ in range(20):
                        self.particles.append(Particle(asteroid.x, asteroid.y, NEON_GREEN))
                    
                    # Split asteroid or remove it
                    if asteroid.size > 1:
                        new_asteroids = asteroid.split()
                        self.asteroids.extend(new_asteroids)
                    
                    # Remove the asteroid and bullet
                    self.asteroids.remove(asteroid)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    
                    # Add score
                    self.player.score += (4 - asteroid.size) * 10
                    
                    # Chance to spawn powerup
                    if random.random() < 0.2:
                        self.powerups.append(PowerUp(asteroid.x, asteroid.y))
                    
                    break
                    
        # Check player-asteroid collisions
        if self.player.invincible == 0:
            for asteroid in self.asteroids[:]:
                dist = math.sqrt((self.player.x - asteroid.x)**2 + (self.player.y - asteroid.y)**2)
                if dist < self.player.size + asteroid.size * 15:
                    # Create explosion particles
                    for _ in range(30):
                        self.particles.append(Particle(self.player.x, self.player.y, NEON_BLUE))
                    
                    self.player.lives -= 1
                    self.player.invincible = 120  # 2 seconds of invincibility
                    
                    if self.player.lives <= 0:
                        self.game_over = True
                    
                    break
                    
        # Check player-powerup collisions
        for powerup in self.powerups[:]:
            dist = math.sqrt((self.player.x - powerup.x)**2 + (self.player.y - powerup.y)**2)
            if dist < self.player.size + powerup.size:
                if powerup.type == "weapon":
                    self.player.weapon_level = min(3, self.player.weapon_level + 1)
                elif powerup.type == "shield":
                    self.player.invincible = 180  # 3 seconds of invincibility
                elif powerup.type == "life":
                    self.player.lives = min(5, self.player.lives + 1)
                    
                # Create collection particles
                for _ in range(15):
                    self.particles.append(Particle(powerup.x, powerup.y, NEON_PINK))
                    
                self.powerups.remove(powerup)
                
        # Spawn new asteroids if needed
        if len(self.asteroids) == 0:
            self.level += 1
            self.asteroids_count += 2
            self.spawn_initial_asteroids()
            
    def draw(self):
        # Draw background
        screen.fill(BLACK)
        
        # Draw stars
        for i in range(100):
            x = (i * 123) % WIDTH
            y = (i * 321) % HEIGHT
            size = (i % 3) + 1
            brightness = 100 + (i % 155)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
            
        # Draw grid lines
        for i in range(0, WIDTH, 50):
            pygame.draw.line(screen, (20, 20, 40), (i, 0), (i, HEIGHT), 1)
        for i in range(0, HEIGHT, 50):
            pygame.draw.line(screen, (20, 20, 40), (0, i), (WIDTH, i), 1)
            
        # Draw game elements
        for asteroid in self.asteroids:
            asteroid.draw()
            
        for bullet in self.bullets:
            bullet.draw()
            
        for powerup in self.powerups:
            powerup.draw()
            
        for particle in self.particles:
            particle.draw()
            
        self.player.draw()
        
        # Draw UI
        # Score
        score_text = self.font.render(f"SCORE: {self.player.score}", True, NEON_BLUE)
        screen.blit(score_text, (10, 10))
        
        # Lives
        lives_text = self.font.render(f"LIVES: {self.player.lives}", True, NEON_GREEN)
        screen.blit(lives_text, (10, 40))
        
        # Level
        level_text = self.font.render(f"LEVEL: {self.level}", True, NEON_PINK)
        screen.blit(level_text, (10, 70))
        
        # Weapon level
        weapon_text = self.font.render(f"WEAPON: {self.player.weapon_level}", True, NEON_PURPLE)
        screen.blit(weapon_text, (10, 100))
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            game_over_text = self.title_font.render("GAME OVER", True, NEON_PINK)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            
            score_text = self.font.render(f"FINAL SCORE: {self.player.score}", True, NEON_BLUE)
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
            
            restart_text = self.font.render("PRESS R TO RESTART", True, NEON_GREEN)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 70))

# Main game loop
def main():
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game = Game()  # Restart the game
                elif event.key == pygame.K_SPACE:
                    new_bullets = game.player.shoot()
                    game.bullets.extend(new_bullets)
                    
        # Get pressed keys for continuous input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.player.rotate(-1)
        if keys[pygame.K_RIGHT]:
            game.player.rotate(1)
        if keys[pygame.K_UP]:
            game.player.accelerate()
        if keys[pygame.K_DOWN]:
            game.player.decelerate()
            
        # Auto-shoot when space is held
        if keys[pygame.K_SPACE]:
            new_bullets = game.player.shoot()
            game.bullets.extend(new_bullets)
            
        # Update game state
        game.update()
        
        # Draw everything
        game.draw()
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

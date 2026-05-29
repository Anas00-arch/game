import pygame
import random
import math

WIDTH, HEIGHT = 800, 700
FPS = 60
TILE_SIZE = 40 
SPEED = 4
GHOST_SPEED = 2

BLACK, WHITE, YELLOW = (10, 10, 20), (255, 255, 255), (255, 255, 0)
BLUE, RED, PINK, ORANGE, CYAN = (33, 33, 255), (255, 0, 0), (255, 182, 193), (255, 165, 0), (0, 255, 255)

MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],  
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,1],
    [1,0,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,0,1],
    [1,1,1,0,1,1,2,2,2,2,2,2,2,2,1,1,0,1,1,1],
    [1,2,2,0,0,0,2,1,1,2,2,1,1,2,0,0,0,2,2,1],
    [1,1,1,0,1,1,2,1,1,1,1,1,1,2,1,1,0,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Player:
    def __init__(self, x, y):
        self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
        self.rect = pygame.Rect(self.x + 5, self.y + 5, TILE_SIZE - 10, TILE_SIZE - 10)
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.angle = 0
        self.mouth_anim = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.next_dir = (-1, 0)
        elif keys[pygame.K_RIGHT]: self.next_dir = (1, 0)
        elif keys[pygame.K_UP]: self.next_dir = (0, -1)
        elif keys[pygame.K_DOWN]: self.next_dir = (0, 1)

        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            if self.check_collision(self.next_dir):
                self.dir = self.next_dir
                self.angle = {(1,0):0, (-1,0):180, (0,-1):90, (0,1):270}.get(self.dir, self.angle)

        if self.check_collision(self.dir):
            self.x += self.dir[0] * SPEED
            self.y += self.dir[1] * SPEED
            self.rect.topleft = (self.x + 5, self.y + 5)

    def check_collision(self, d):
        nx, ny = self.x + d[0]*SPEED, self.y + d[1]*SPEED
        for ox, oy in [(2,2), (TILE_SIZE-3, 2), (2, TILE_SIZE-3), (TILE_SIZE-3, TILE_SIZE-3)]:
            if MAZE[int((ny + oy)//TILE_SIZE)][int((nx + ox)//TILE_SIZE)] == 1:
                return False
        return True

    def draw(self, screen):
        self.mouth_anim = (self.mouth_anim + 5) % 40
        m = abs(20 - self.mouth_anim)
        center = (self.x + TILE_SIZE//2, self.y + TILE_SIZE//2)
        pygame.draw.circle(screen, YELLOW, center, TILE_SIZE//2 - 2)
        p1 = center
        p2 = (center[0] + math.cos(math.radians(self.angle - m)) * 22, center[1] - math.sin(math.radians(self.angle - m)) * 22)
        p3 = (center[0] + math.cos(math.radians(self.angle + m)) * 22, center[1] - math.sin(math.radians(self.angle + m)) * 22)
        pygame.draw.polygon(screen, BLACK, [p1, p2, p3])
        pygame.draw.circle(screen, BLACK, (center[0] + 5, center[1] - 10), 3)

class Ghost:
    def __init__(self, x, y, color):
        self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
        self.rect = pygame.Rect(self.x + 6, self.y + 6, TILE_SIZE - 12, TILE_SIZE - 12)
        self.color = color
        self.dir = (0, 0)

    def move(self, target_pos):
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            dirs = [(1,0), (-1,0), (0,1), (0,-1)]
            valid_dirs = [d for d in dirs if self.check_collision(d)]
            if valid_dirs:
                valid_dirs.sort(key=lambda d: math.hypot((self.x + d[0]*TILE_SIZE) - target_pos[0], (self.y + d[1]*TILE_SIZE) - target_pos[1]))
                self.dir = valid_dirs[0]

        if self.check_collision(self.dir):
            self.x += self.dir[0] * GHOST_SPEED
            self.y += self.dir[1] * GHOST_SPEED
            self.rect.topleft = (self.x + 6, self.y + 6)

    def check_collision(self, d):
        nx, ny = self.x + d[0]*GHOST_SPEED, self.y + d[1]*GHOST_SPEED
        for ox, oy in [(1,1), (TILE_SIZE-2, 1), (1, TILE_SIZE-2), (TILE_SIZE-2, TILE_SIZE-2)]:
            r, c = int((ny + oy)//TILE_SIZE), int((nx + ox)//TILE_SIZE)
            if MAZE[r][c] == 1: return False
        return True

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 10, self.rect.y + 10), 4)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 22, self.rect.y + 10), 4)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Impact", 45)
    
    player = Player(1, 1)
    ghosts = [Ghost(9, 6, RED)]
    pellets = [pygame.Rect(c*TILE_SIZE+18, r*TILE_SIZE+18, 5, 5) for r, row in enumerate(MAZE) for c, val in enumerate(row) if val == 0]
    score = 0
    state = "PLAY"
    
    spawned_pink = False
    spawned_orange = False

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if state in ["WIN", "LOSE"]: main(); return

        if state == "PLAY":
            for r, row in enumerate(MAZE):
                for c, val in enumerate(row):
                    if val == 1: pygame.draw.rect(screen, BLUE, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 2, 8)
            
            for p in pellets[:]:
                pygame.draw.circle(screen, WHITE, p.center, 3)
                if player.rect.colliderect(p): 
                    pellets.remove(p)
                    score += 10

            if score >= 150 and not spawned_pink:
                ghosts.append(Ghost(10, 5, PINK)) 
                spawned_pink = True
            if score >= 300 and not spawned_orange:
                ghosts.append(Ghost(9, 5, ORANGE))
                spawned_orange = True

            player.move()
            player.draw(screen)

            for g in ghosts:
                g.move((player.x, player.y))
                g.draw(screen)
                if g.rect.colliderect(player.rect): state = "LOSE"

            if not pellets: state = "WIN"
            
            score_txt = pygame.font.SysFont("Arial", 25).render(f"SCORE: {score}  |  GHOSTS: {len(ghosts)}", True, WHITE)
            screen.blit(score_txt, (10, 10))

        elif state == "WIN":
            txt = font.render("VICTORY! CHAMPION", True, YELLOW)
            screen.blit(txt, (WIDTH//2 - 200, HEIGHT//2))
            
        elif state == "LOSE":
            txt = font.render("GAME OVER - RETRY?", True, RED)
            screen.blit(txt, (WIDTH//2 - 180, HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
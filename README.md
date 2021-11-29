## helloPygame
[https://www.pygame.org/wiki/GettingStarted](https://www.pygame.org/wiki/GettingStarted)

[https://www.youtube.com/watch?v=f1amAQuVtc8](https://www.youtube.com/watch?v=f1amAQuVtc8)

<details>
  <summary>Details</summary>
  <p>
  
```python
import pygame
import os

# Pygame init
pygame.init()

# Screen
screen_width = 432
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Puzzle Bobble")

# Clock
clock = pygame.time.Clock()

# Background Image Load
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "resource/background/background.png"))
wall = pygame.image.load(os.path.join(current_path, "resource/wall/wall.png"))


# Bubble Images Load
bubble_images = [
    pygame.image.load(os.path.join(current_path, "resource/bubble/red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/black.png")).convert_alpha(),
]

# Pointer Image Load
pointer_image = pygame.image.load(os.path.join(current_path, "resource/pointer/pointer.png"))


# Game Loop
is_running = True

while is_running:
  clock.tick(60)
  
  for event in pygame.event.get():
    eventHandler(event)
    
  statusUpdate()
  
  print(screen)   # screen.bilt(image, (x, y))
  
  pygame.display.update()

# Game Quit
pygame.time.delay(5000)
pygame.quit()
```
  </p>
</details>

import pygame

pygame.init()

WIDTH, HEIGHT = 1500, 990
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Voting system")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)
DARK_GRAY = (23, 23, 23)
ALVIER_GREEN = (40, 190, 35)

#Load logo
logo = pygame.image.load("alvier_logo_white.png")
logo = pygame.transform.scale(logo, (120, 50))

# Typsnitt
pygame.font.init()
font = pygame.font.Font(None, 40)  # Standardtypsnitt, storlek 40

# Fråga och svar
question_text = "What's your favorite color?"
answers = ["Red", "Blue", "Green", "Yellow", "Purple"]

# Knappinställningar
button_width, button_height = 100, 50
button_spacing = 15
start_x = (WIDTH - button_width) // 6
start_y = HEIGHT // 2

running = True

while running:
    screen.fill(DARK_GRAY)

    #Place logo at top right corner
    screen.blit(logo, (WIDTH - 130, 10))

    #Question text
    question_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4 - 10, WIDTH // 2, 50)
    pygame.draw.rect(screen, ALVIER_GREEN, question_rect, border_radius=10)
    question_surface = font.render(question_text, True, WHITE)
    text_rect = question_surface.get_rect(center=question_rect.center)
    screen.blit(question_surface, text_rect)

    # Answers
    for i, answer in enumerate(answers):
        button_x = start_x + i * (WIDTH - button_width) // 6
        button_rect = pygame.Rect(button_x, start_y, button_width, button_height)

        pygame.draw.rect(screen, ALVIER_GREEN, button_rect, border_radius=10)
        text_surface = font.render(answer, True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    clock.tick(60) # Limits FPS to 60

pygame.quit()
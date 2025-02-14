import pygame

pygame.init()

WIDTH, HEIGHT = 1500, 990
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Voting system")

# Colors
WHITE = (235, 235, 235)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)
DARK_GRAY = (23, 23, 23)
ALVIER_GREEN = (38, 208, 124)

#Load logo
logo = pygame.image.load("Images/alvier_logo_white.png")
logo = pygame.transform.scale(logo, (200, 90))

#Load gear image
gear = pygame.image.load("Images/alvier_gear.png")
gear = pygame.transform.scale(gear, (120, 120))
gear_angle = 0

# Typsnitt
pygame.font.init()
font = pygame.font.Font(None, 40)  # Standardtypsnitt, storlek 40
font_q = pygame.font.Font(None, 80)  # Standardtypsnitt, storlek 40

# Questions and answers
question_text = "What's your favorite color?"
answers = ["Red", "Blue", "Green", "Yellow", "Purple"]

# Answer text-boxes
box_width, box_height = 230, 360  # Större rutor för längre svar
start_x = (WIDTH - (box_width * len(answers) + 20 * (len(answers) - 1))) // 2
start_y = 520

running = True

while running:
    screen.fill(DARK_GRAY)

    #Rotate the gear
    gear_angle -= 1
    rotated_gear = pygame.transform.rotate(gear, gear_angle)

    #Get center of gear and place place it at coordinates (x,y)
    gear_rect = rotated_gear.get_rect(center=(WIDTH - 120, 170))

    #Place images
    screen.blit(logo, (WIDTH - 220, 10))
    screen.blit(rotated_gear, gear_rect.topleft)

    #Question text
    question_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4 - 10, WIDTH // 2, 100)
    pygame.draw.rect(screen, DARK_GRAY, question_rect, border_radius=10)
    question_surface = font_q.render(question_text, True, WHITE)
    text_rect = question_surface.get_rect(center=question_rect.center)
    screen.blit(question_surface, text_rect)

    # Rektangel under knapparna
    rect_x = 100  
    rect_y = 500  # Liten marginal ovanför
    rect_width = 1300  # Täcker alla knappar + extra marginal
    rect_height = 400
    
    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height), border_radius=15)

    # Answers
    for i, answer in enumerate(answers):
        box_x = start_x + i * (box_width + 20)
        box_rect = pygame.Rect(box_x, start_y, box_width, box_height)

        pygame.draw.rect(screen, ALVIER_GREEN, box_rect, border_radius=10)
        text_surface = font.render(answer, True, WHITE)
        text_rect = text_surface.get_rect(center=box_rect.center)
        screen.blit(text_surface, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    clock.tick(60) # Limits FPS to 60

pygame.quit()

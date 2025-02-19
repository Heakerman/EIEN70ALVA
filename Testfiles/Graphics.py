import pygame
import threading

class Graphics(threading.Thread):
    def __init__(self):
        super().__init__() #Initialize the thread
        pygame.init()

        #Screen Setup
        self.WIDTH, self.HEIGHT = 1500, 990
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Voting system")

        #Colors
        self.WHITE = (235, 235, 235)
        self.BLACK = (0, 0, 0)
        self.PURPLE = (128, 0, 128)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (23, 23, 23)
        self.ALVIER_GREEN = (38, 208, 124)

        #Load images
        self.logo = pygame.image.load("Images/alvier_logo_white.png")
        self.logo = pygame.transform.scale(self.logo, (200, 90))

        self.gear = pygame.image.load("Images/alvier_gear.png")
        self.gear = pygame.transform.scale(self.gear, (120, 120))
        self.gear_angle = 0

        #Fonts
        pygame.font.init()
        self.font = pygame.font.Font(None, 40)  # Standardtypsnitt, storlek 40
        self.font_q = pygame.font.Font(None, 80)  # Standardtypsnitt, storlek 80

        #Questions and answers
        self.question_text = "What's your favorite color?"
        self.answers = ["Red", "Blue", "Green", "Yellow", "Purple"]

        #Answer text-boxes
        self.box_width, self.box_height = 230, 360  # Större rutor för längre svar
        self.start_x = (self.WIDTH - (self.box_width * len(self.answers) + 20 * (len(self.answers) - 1))) // 2
        self.start_y = 520

        self.running = True #Flag to control the thread loop

    def run(self):
        while self.running:
            self.screen.fill(self.DARK_GRAY)

            #Rotate the gear
            self.gear_angle -= 1
            rotated_gear = pygame.transform.rotate(self.gear, self.gear_angle)

            #Get center of gear and place place it at coordinates (x,y)
            gear_rect = rotated_gear.get_rect(center=(self.WIDTH - 120, 170))

            #Draw images
            self.screen.blit(self.logo, (self.WIDTH - 220, 10))
            self.screen.blit(rotated_gear, gear_rect.topleft)

            #Question text
            question_rect = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 4 - 10, self.WIDTH // 2, 100)
            pygame.draw.rect(self.screen, self.DARK_GRAY, question_rect, border_radius=10)
            question_surface = self.font_q.render(self.question_text, True, self.WHITE)
            text_rect = question_surface.get_rect(center=question_rect.center)
            self.screen.blit(question_surface, text_rect)

            #Background rectangle for buttons
            rect_x = 100  
            rect_y = 500  # Liten marginal ovanför
            rect_width = 1300  # Täcker alla knappar + extra marginal
            rect_height = 400
            
            pygame.draw.rect(self.screen, self.WHITE, (rect_x, rect_y, rect_width, rect_height), border_radius=15)

            # Answer boxes
            for i, answer in enumerate(self.answers):
                box_x = self.start_x + i * (self.box_width + 20)
                box_rect = pygame.Rect(box_x, self.start_y, self.box_width, self.box_height)

                pygame.draw.rect(self.screen, self.ALVIER_GREEN, box_rect, border_radius=10)
                text_surface = self.font.render(answer, True, self.WHITE)
                text_rect = text_surface.get_rect(center=box_rect.center)
                self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

            self.clock.tick(60) # Limits FPS to 60

        pygame.quit()

    def stop(self):
        self.running = False
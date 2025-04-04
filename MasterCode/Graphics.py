import pygame
import threading

class Graphics(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        pygame.init()

        self.monitor = monitor  # Reference to the Monitor instance

        # Screen Setup
        self.WIDTH, self.HEIGHT = 1920, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Voting system")

        # Colors
        self.WHITE = (235, 235, 235)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (23, 23, 23)
        self.ALVIER_GREEN = (38, 208, 124)

        # Load images
        self.logo = pygame.image.load("Images/alvier_logo_white.png")
        self.logo = pygame.transform.scale(self.logo, (200, 90))

        self.gear = pygame.image.load("Images/alvier_gear.png")
        self.gear = pygame.transform.scale(self.gear, (120, 120))
        self.gear_angle = 0

        # Fonts
        pygame.font.init()
        self.font = pygame.font.Font(None, 40)
        self.font_q = pygame.font.Font(None, 80)

        # Questions and answers
        self.question_text, self.answers = self.monitor.getQandA()
        self.monitor.reset_update_flag()

        # Answer text-boxes
        self.box_width, self.box_height = (self.WIDTH-220-10*4)//5, self.HEIGHT - 170
        self.start_x = 110
        self.start_y = 460

        self.running = True

    def run(self):
        while self.running:
            try:
                self.screen.fill(self.DARK_GRAY)

                if self.monitor.GraphUpdated:
                    # Update question and answers
                    self.question_text, self.answers = self.monitor.getQandA()
                    self.monitor.reset_update_flag()

                # Rotate the gear
                self.gear_angle -= 1
                rotated_gear = pygame.transform.rotate(self.gear, self.gear_angle)
                gear_rect = rotated_gear.get_rect(center=(self.WIDTH - 120, 170))

                # Draw images
                self.screen.blit(self.logo, (self.WIDTH - 220, 10))
                self.screen.blit(rotated_gear, gear_rect.topleft)

                # Question text
                question_rect = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 4 - 10, self.WIDTH // 2, 100)
                pygame.draw.rect(self.screen, self.DARK_GRAY, question_rect, border_radius=10)
                question_surface = self.font_q.render(self.question_text, True, self.WHITE)
                text_rect = question_surface.get_rect(center=question_rect.center)
                self.screen.blit(question_surface, text_rect)

                # Background rectangle for buttons
                rect_x = 100  
                rect_y = 450
                rect_width = self.WIDTH - 200
                rect_height = self.HEIGHT - 150
                pygame.draw.rect(self.screen, self.WHITE, (rect_x, rect_y, rect_width, rect_height), border_radius=15)

                # Answer boxes
                for i, answer in enumerate(self.answers):
                    box_x = self.start_x + i * (self.box_width + 10)
                    box_rect = pygame.Rect(box_x, self.start_y, self.box_width, self.box_height)
                    pygame.draw.rect(self.screen, self.ALVIER_GREEN, box_rect, border_radius=10)
                    text_surface = self.font.render(answer, True, self.WHITE)
                    text_rect = text_surface.get_rect(center=box_rect.center)
                    self.screen.blit(text_surface, text_rect)

                pygame.display.flip()
                self.clock.tick(60)

            except Exception as e:
                print(f"Error in run loop: {e}")
                self.running = False

        self.stop()

    def stop(self):
        """Stops the graphics thread."""
        if self.running:  # Prevent multiple calls
            print("Stopping graphics...")

            self.running = False  # Set flag first

            # Fill screen with black to visually indicate shutdown
            self.screen.fill((0, 0, 0))
            pygame.display.flip()

            # Process any remaining events to avoid crashes
            pygame.event.clear()

            # Small delay to allow Pygame to process the shutdown
            pygame.time.delay(100)

            # Quit Pygame
            pygame.quit()
            print("Graphics thread exited.")

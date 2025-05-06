import pygame

class Graphics:
    def __init__(self, monitor):
        pygame.init()

        self.monitor = monitor

        # Skärmkonfiguration
        self.WIDTH, self.HEIGHT = 1920, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Voting system")

        # Färger
        self.WHITE = (235, 235, 235)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (23, 23, 23)
        self.ALVIER_GREEN = (38, 208, 124)

        # Ladda bilder
        self.logo = pygame.image.load("Images/alvier_logo_white.png")
        self.logo = pygame.transform.scale(self.logo, (200, 90))

        self.gear = pygame.image.load("Images/alvier_gear.png")
        self.gear = pygame.transform.scale(self.gear, (120, 120))
        self.gear_angle = 0

        # Typsnitt
        pygame.font.init()
        self.font = pygame.font.SysFont("timesnewroman", 40)
        self.font_q = pygame.font.SysFont("timesnewroman", 70)

        # Hämta första frågan och svar
        self.question_text, self.answers = self.monitor.getQandA()
        self.monitor.reset_update_flag()

        # Dimensioner för svarsknappar
        self.box_width, self.box_height = (self.WIDTH - 220 - 10 * 4) // 5, self.HEIGHT - 170
        self.start_x = 110
        self.start_y = 460

        self.running = True

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        wrapped_lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word

        if current_line:
            wrapped_lines.append(current_line)

        return wrapped_lines

    def render(self):
        if self.monitor.GraphUpdated:
            self.question_text, self.answers = self.monitor.getQandA()
            self.monitor.reset_update_flag()

        self.screen.fill(self.DARK_GRAY)

        self.gear_angle -= 1
        rotated_gear = pygame.transform.rotate(self.gear, self.gear_angle)
        gear_rect = rotated_gear.get_rect(center=(self.WIDTH - 120, 170))

        self.screen.blit(self.logo, (self.WIDTH - 220, 10))
        self.screen.blit(rotated_gear, gear_rect.topleft)

        # Frågeruta
        question_rect = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 4 - 10, self.WIDTH // 2, 100)
        pygame.draw.rect(self.screen, self.DARK_GRAY, question_rect, border_radius=10)
        question_surface = self.font_q.render(self.question_text, True, self.WHITE)
        text_rect = question_surface.get_rect(center=question_rect.center)
        self.screen.blit(question_surface, text_rect)

        # Bakgrundsrektangel för svar
        pygame.draw.rect(self.screen, self.WHITE, (100, 450, self.WIDTH - 200, self.HEIGHT - 150), border_radius=15)

        # Rita svarsknappar
        for i, answer in enumerate(self.answers):
            box_x = self.start_x + i * (self.box_width + 10)
            box_rect = pygame.Rect(box_x, self.start_y, self.box_width, self.box_height)
            pygame.draw.rect(self.screen, self.ALVIER_GREEN, box_rect, border_radius=10)

            wrapped_lines = self.wrap_text(answer, self.font, self.box_width - 20)

            line_spacing = 10
            total_height = len(wrapped_lines) * self.font.get_height() + (len(wrapped_lines) - 1) * line_spacing
            start_y_text = box_rect.centery - total_height // 2

            for j, line in enumerate(wrapped_lines):
                text_surface = self.font.render(line, True, self.WHITE)
                text_rect = text_surface.get_rect(center=(box_rect.centerx, start_y_text + j * (self.font.get_height() + line_spacing)))
                self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def stop(self):
        if self.running:
            self.running = False
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            pygame.event.clear()
            pygame.time.delay(100)
            pygame.quit()
            print("Graphics stopped.")

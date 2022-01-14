import pygame

class Button():
    def __init__(self, x, y, width=100, height=30, color=pygame.Color('white'), scale=1, image=None):
        if image:
            self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
            self.rect = self.image.get_rect()
        else:
            self.image = image
            self.rect = pygame.Rect(x, y, width, height)
            self.color = color

        self.rect.topleft = (x, y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
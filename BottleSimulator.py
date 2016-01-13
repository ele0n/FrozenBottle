import pygame


class BottleSimulator:
    def __init__(self, x, y, scale=4):
        self.array = (x*y-(y-y % 2)/2)*[2*[0]]
        self.x = x
        self.y = y
        self.scale = scale
        self.screen = pygame.display.set_mode((x*20*scale, y*20*scale))
        pygame.display.set_caption("FrozenBottle")
        pygame.init()
        self.screen.fill((255, 255, 255))

        for i in range(y):
            if i % 2 == 0:
                for j in range(x):
                    idx = len(self.array)-1-(j+i*x-(i+i % 2)/2)
                    self.array[idx] = 10*scale+j*20*scale, 10*scale+i*scale*17
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (10*scale+j*20*scale,
                                       10*scale+i*17*scale), 10*scale, 0)
                    pygame.draw.circle(self.screen, (255, 255, 255),
                                       (10*scale+j*20*scale,
                                       10*scale+i*17*scale), 8*scale, 0)
            else:
                for j in range(x-1):
                    idx = len(self.array)-1-((x-1-j)+x*i-(i+i % 2)/2)
                    self.array[idx] = 20*scale+j*20*scale, 10*scale+i*17*scale
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (20*scale+j*20*scale,
                                       10*scale+i*17*scale),
                                       10*scale, 0)
                    pygame.draw.circle(self.screen, (255, 255, 255),
                                       (20*scale+j*20*scale,
                                       10*scale+i*17*scale),
                                       8*scale, 0)

        pygame.display.update()

    def send(self, i, r, g, b):
        pygame.draw.circle(self.screen, (r, g, b), (self.array[i][0],
                           self.array[i][1]), 8*self.scale, 0)
        pygame.display.update()

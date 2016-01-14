import pygame


class BottleSimulator(object):
    white = (255, 255, 255)
    black = (0, 0, 0)

    def __init__(self, cols, rows, resolution=(800, 600)):
        self.cols = cols
        self.rows = rows

        self.screen = pygame.display.set_mode(resolution)

        # radius is calculated relative to rows/columns
        self.radius = min((self.screen.get_width() // self.cols // 2,
                          self.screen.get_height() // self.rows // 2))

        # odd lines are missing 1 bottle
        odd = (rows - rows % 2) / 2
        self.bottles = [self.black] * ((rows*cols)-odd)

        pygame.display.set_caption("FrozenBottle")
        pygame.init()

        self.screen.fill(self.white)
        self.draw_bottles()

    def i_to_xy(self, i):
        # compensate for odd lines missing 1 bottle
        for k in range(1, i, 2):
            if i >= self.cols-1+self.cols*k:
                i += 1

        x = i % self.cols
        y = i // self.cols

        return x, y

    def draw_bottles(self):
        for i, color in enumerate(self.bottles):
            self.draw_bottle_i(i, color)

    def draw_bottle_i(self, i, color, border=5):
        x, y = self.i_to_xy(i)
        # print("Drawing %d to (%d,%d)" % (i, x, y))
        self.draw_bottle_xy(x, y, color, border)

    def draw_bottle_xy(self, x, y, color, border=5, virtual_exc=True):
        pos_x = self.radius + x*self.radius*2
        # bottles should "lay" on each other
        pos_y = self.radius + y*self.radius*2 - y*15

        # odd rows have one bottle less than even rows
        if y % 2 != 0:
            if x == self.cols-1:
                if virtual_exc:
                    raise Exception('No such bottle: (%d,%d)' % (x, y))
                return
            pos_x += self.radius

        # draw border
        pygame.draw.circle(self.screen, self.black, (pos_x, pos_y),
                           self.radius)
        # draw bottle bottom
        pygame.draw.circle(self.screen, color, (pos_x, pos_y),
                           self.radius-border*2)

        pygame.display.update()

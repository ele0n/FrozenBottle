import pygame
import threading


class BottleSimulator(threading.Thread):
    white = (255, 255, 255)
    black = (0, 0, 0)

    def __init__(self, cols, rows, resolution=(800, 600)):
        threading.Thread.__init__(self)
        self.cols = cols
        self.rows = rows

        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()

        # radius is calculated relative to rows/columns
        self.radius = min((self.screen.get_width() // self.cols // 2,
                          self.screen.get_height() // self.rows // 2))

        # odd lines are missing 1 bottle
        odd = (rows - rows % 2) / 2
        self.bottles = [self.black] * ((rows*cols)-odd)
        self.bottles_next = [self.black] * ((rows*cols)-odd)

        pygame.display.set_caption("FrozenBottle")
        pygame.init()

        self.screen.fill(self.white)

    @property
    def index_count(self):
        return self.xy_to_i(self.cols-1, self.rows-1) + 1

    def i_to_xy(self, i):
        # compensate for odd lines missing 1 bottle
        for k in range(1, i, 2):
            if i >= self.cols-1+self.cols*k:
                i += 1

        x = i % self.cols
        y = i // self.cols

        return x, y

    def xy_to_i(self, x, y):
        i = y*self.cols + x

        # compensate for odd lines missing 1 bottle
        for k in range(1, i, 2):
            if i >= self.cols-1+self.cols*k:
                i -= 1

        return i

    def draw_bottles(self, all=True):
        for i, color in enumerate(self.bottles):
            if all or self.bottles[i] != self.bottles_next[i]:
                self.draw_bottle_i(i, color, commit=True)

    def draw_bottle_i(self, i, color, border=5, commit=True):
        x, y = self.i_to_xy(i)
        # print("Drawing %d to (%d,%d)" % (i, x, y))
        self.draw_bottle_xy(x, y, color, border, commit=commit)

    def draw_bottle_xy(self, x, y, color, border=5, exc=True, commit=True):
        if exc and not 0 <= self.xy_to_i(x, y) < self.index_count:
            raise IndexError('No such bottle: (%d,%d)' % (x, y))

        pos_x = self.radius + x*self.radius*2
        # bottles should "lay" on each other
        pos_y = self.radius + y*self.radius*2 - y*15

        # odd rows have one bottle less than even rows
        if y % 2 != 0:
            pos_x += self.radius

        i = self.xy_to_i(x, y)
        self.bottles[i] = color

        if commit:
            # draw border
            pygame.draw.circle(self.screen, self.black, (pos_x, pos_y),
                               self.radius)
            # draw bottle bottom
            pygame.draw.circle(self.screen, color, (pos_x, pos_y),
                               self.radius-border*2)

            pygame.display.update()

    def get_color_i(self, i):
        return self.bottles[i]

    def get_color_xy(self, x, y):
        i = self.xy_to_i(x, y)
        return self.get_color_i(i)

    def commit(self):
        self.draw_bottles()

    def run(self):
        self.running = True
        self.draw_bottles(all=True)
        while self.running:
            self.clock.tick(10)

from BottleSimulator import BottleSimulator
import time


class Breakout(object):
    green = (0, 255, 0)

    def __init__(self):
        self.sim = BottleSimulator(7, 5)
        self.running = False

        self.sim.start()

    def reset_game(self):
        self.obstacles = {
            1:  self.green,
            2:  self.green,
            4:  self.green,
            5:  self.green,
        }
        self.last_pos = (0, 0)
        self.position = (0, 0)
        self.slider_pos = self.sim.cols // 2
        self.direction = -6
        self.clear()
        self.set_obstacles()
        self.set_slider(self.slider_pos)
        self.set_ball(self.start_position())
        self.sim.commit()

    def clear(self):
        for i in range(self.sim.index_count):
            self.sim.draw_bottle_i(i, self.sim.black, commit=False)

    def set_ball(self, pos):
        if self.sim.get_color_xy(*pos) != self.sim.black:
            i = self.sim.xy_to_i(*pos)
            if i in self.obstacles.keys():
                del self.obstacles[i]
            raise IndexError('Slider hit')
        self.last_pos = self.position
        self.position = pos
        self.sim.draw_bottle_xy(pos[0], pos[1], self.sim.white, commit=False)

    def set_slider(self, x_pos):
        if 1 <= x_pos <= self.sim.cols - 2:
            self.slider_pos = x_pos
            red = (255, 0, 0)
            for offset in range(-1, 2):
                self.sim.draw_bottle_xy(x_pos+offset, self.sim.rows-1, red, commit=False)

    def start_position(self):
        x = self.sim.cols // 2
        y = self.sim.rows - 2
        return x, y

    def roll(self):
        x = self.sim.cols
        directions = {-(x-1): x, -x: (x-1), (x-1): -x, x: -(x-1), (x-2): -(x-1), -(x-2): (x-1)}
        i = self.sim.xy_to_i(*self.position)
        # print("last pos:", self.position[0], self.position[1])

        success = False
        while not success:
            try:
                next_pos = self.sim.i_to_xy(i + self.direction)
                # bounce off the side
                if next_pos[0] + 2 < self.position[0] or \
                        next_pos[0] - 2 > self.position[0]:
                    self.direction *= -1
                    self.direction = directions[self.direction]
                else:
                    self.set_ball(next_pos)
                    success = True
            except IndexError, e:
                print(e)
                print(next_pos)

                # did ball touch bottom?
                if next_pos[1] == self.sim.rows:
                    print('GAME OVER')
                    self.stop()
                    time.sleep(2)
                    self.start()

                # print("direction", self.direction)
                # bounce off top/bottom
                if next_pos[1] == self.sim.rows - 1:
                    directions = {-6: 5, -7: 6, 6: -5, 7: -6, -5: 7, 5: -7}
                self.direction = directions[self.direction]

        # print("next pos:", next_pos[0], next_pos[1])

    def slider_ai(self):
        direction = 0
        if self.position[0] > self.slider_pos:
            direction = 1
        if self.position[0] < self.slider_pos:
            direction = -1

        if not 1 <= self.slider_pos + direction <= self.sim.cols - 2:
            direction = 0

        self.set_slider(self.slider_pos + direction)

    def set_obstacles(self):
        for i, color in self.obstacles.items():
            self.sim.draw_bottle_i(i, color, commit=False)

    def check_won(self):
        if len(self.obstacles) == 0:
            return True
        return False

    def start(self):
        self.running = True
        self.reset_game()
        time.sleep(1)
        while self.running:
            try:
                if self.check_won():
                    print("WON!")
                    self.stop()
                    time.sleep(2)
                    self.start()

                self.clear()
                # always draw obstacles and slider before ball!
                self.slider_ai()
                self.set_obstacles()
                self.roll()
                self.sim.commit()
                time.sleep(1)
            except KeyboardInterrupt:
                self.quit()
                break

    def stop(self):
        self.running = False

    def quit(self):
        self.stop()
        self.sim.running = False

if __name__ == '__main__':
    breakout = Breakout()
    breakout.start()

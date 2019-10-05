#!/usr/bin/env python

from PIL import Image, ImageDraw
import numpy
import sys

class Mandel:
    VIEWPORT = { 'x': (-2.5, 1), 'y': (-1.25, 1.25) }
    #VIEWPORT = { 'x': (-0.1, 0), 'y': (-1.04, -0.96) }
    WIDTH = 1200

    MAX_ITERATIONS = 48
    RAINBOW_GRADIENT_SCALE = 1.0

    viewport_width = VIEWPORT['x'][1] - VIEWPORT['x'][0]
    viewport_height = VIEWPORT['y'][1] - VIEWPORT['y'][0]
    aspect_ratio = viewport_width / viewport_height
    HEIGHT = int(WIDTH / aspect_ratio)

    RAINBOW_GRADIENT_SIZE = int(RAINBOW_GRADIENT_SCALE * MAX_ITERATIONS)

    def __init__(self):
        self.gradient = self.rainbow_gradient(self.RAINBOW_GRADIENT_SIZE)

    def draw(self):
        image = Image.new('RGB', (self.WIDTH, self.HEIGHT))
        draw = ImageDraw.Draw(image)
        self.draw_mandel(draw)
        #image.save('screenshots/...', 'PNG')
        image.show()

    def draw_mandel(self, draw):
        progress = 0
        tick_size = int(self.WIDTH * self.HEIGHT / 120)
        for pixel_x, pixel_y in self.for_each_pixel():
            progress = progress + 1
            if (progress == tick_size):
                print('.', end='', flush=True)
                progress = 0

            complex_x, complex_y = self.pixel_to_complex_coordinates(pixel_x, pixel_y)
            num_iterations = self.iterations_for(complex_x, complex_y)
            color = self.colorize(num_iterations)
            draw.point((pixel_x, pixel_y), fill=color)
        print()

    def iterations_for(self, x_offset, y_offset):
        x, y = (0, 0)
        for i in range(0, self.MAX_ITERATIONS):
            x, y = x * x - y * y + x_offset, 2 * x * y + y_offset
            if x * x + y * y > 2 * 2: return i
        return self.MAX_ITERATIONS

    def for_each_pixel(self):
        for y in range(0, self.HEIGHT):
            for x in range(0, self.WIDTH):
                yield [x, y]

    def pixel_to_complex_coordinates(self, x, y):
        x_range = self.VIEWPORT['x'][1] - self.VIEWPORT['x'][0]
        x_scaling_factor = self.WIDTH / x_range
        scaled_x = x / x_scaling_factor + self.VIEWPORT['x'][0]

        y_range = self.VIEWPORT['y'][1] - self.VIEWPORT['y'][0]
        y_scaling_factor = self.HEIGHT / y_range
        scaled_y = y / y_scaling_factor + self.VIEWPORT['y'][0]

        return scaled_x, scaled_y

    def colorize(self, iterations):
        color = self.gradient[iterations % self.RAINBOW_GRADIENT_SIZE]
        intensity = 0 if iterations == self.MAX_ITERATIONS else iterations / self.MAX_ITERATIONS
        return (int(color[0] * intensity), int(color[1] * intensity), int(color[2] * intensity))

    def rainbow_gradient(self, full_scale):
        if (full_scale % 12 != 0): raise Exception("full_scale must be a multple of 12")
        colors = numpy.empty(full_scale, dtype=object)

        # Define the bottom edge of each section of the gradient
        red_max_blue_increasing = int(full_scale * 0 / 6)
        blue_max_red_decreasing = int(full_scale * 1 / 6)
        blue_max_green_increasing = int(full_scale * 2 / 6)
        green_max_blue_decreasing = int(full_scale * 3 / 6)
        green_max_red_increasing = int(full_scale * 4 / 6)
        red_max_green_decreasing = int(full_scale * 5 / 6)

        scale = int(full_scale / 6)
        for i in range(0, scale): colors[red_max_blue_increasing + i] = (255, 0, int((i / scale) * 255))
        for i in range(0, scale): colors[blue_max_red_decreasing + i] = (int((1 - i / scale) * 255), 0, 255)
        for i in range(0, scale): colors[blue_max_green_increasing + i] = (0, int((i / scale) * 255), 255)
        for i in range(0, scale): colors[green_max_blue_decreasing + i] = (0, 255, int((1 - i / scale) * 255))
        for i in range(0, scale): colors[green_max_red_increasing + i] = (int((i / scale) * 255), 255, 0)
        for i in range(0, scale): colors[red_max_green_decreasing + i] = (255, int((1 - i / scale) * 255), 0)

        return colors

Mandel().draw()

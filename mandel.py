#!/usr/bin/env python

import arcade
import numpy
import time

class Mandel:
    WIDTH, HEIGHT = (1000, 500)
    MAX_ITERATIONS = 12
    RAINBOW_GRADIENT_SCALE = 12

    MANDELBROT_SCALE = { 'x': (-2.3, 1.2), 'y': (-1.6, 1.4) }

    def __init__(self):
        self.gradient = self.rainbow_gradient(self.RAINBOW_GRADIENT_SCALE)

    def draw(self):
        arcade.open_window(self.WIDTH, self.HEIGHT, "Mandelbrot")
        arcade.set_background_color([30, 30, 30])
        arcade.start_render()

        self.draw_mandel()

        arcade.finish_render()
        arcade.run()

    def draw_mandel(self):
        progress = 0
        tick_size = int(self.WIDTH * self.HEIGHT / 120)
        for pixel_x, pixel_y in self.for_each_pixel():
            progress = progress + 1
            if (progress == tick_size):
                print('.', end='', flush=True)
                progress = 0

            mandel_x, mandel_y = self.pixel_to_mandelbrot_scale(pixel_x, pixel_y)
            color = self.colorize(self.iterations_for(mandel_x, mandel_y))
            arcade.draw_point(pixel_x, pixel_y, color, 10)
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

    def pixel_to_mandelbrot_scale(self, x, y):
        x_range = self.MANDELBROT_SCALE['x'][1] - self.MANDELBROT_SCALE['x'][0]
        x_scaling_factor = self.WIDTH / x_range
        scaled_x = x / x_scaling_factor + self.MANDELBROT_SCALE['x'][0]

        y_range = self.MANDELBROT_SCALE['y'][1] - self.MANDELBROT_SCALE['y'][0]
        y_scaling_factor = self.HEIGHT / y_range
        scaled_y = y / y_scaling_factor + self.MANDELBROT_SCALE['y'][0]

        return scaled_x, scaled_y

    def colorize(self, iterations):
        color = self.gradient[iterations % self.RAINBOW_GRADIENT_SCALE]
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

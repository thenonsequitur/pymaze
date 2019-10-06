#!/usr/bin/env python

from PIL import Image, ImageDraw

class Mandel:
    VIEWPORT = { 'left': -2.5, 'top': -1.25, 'right': 1, 'bottom': 1.25 }
    #VIEWPORT = { 'left': -0.1, 'top': -1.04, 'right': 0, 'bottom': -0.96 }
    #VIEWPORT = { 'left': -0.7513, 'top': 0.1052, 'right': -0.7413, 'bottom': 0.1152 }
    ESCAPE_DEPTH = 1000

    CANVAS_HEIGHT = 900
    aspect_ratio = (VIEWPORT['bottom'] - VIEWPORT['top']) / (VIEWPORT['right'] - VIEWPORT['left'])
    CANVAS_WIDTH = int(CANVAS_HEIGHT / aspect_ratio)

    GRADIENT_SCALE = 960

    def __init__(self):
        self.gradient = self.rainbow_gradient()
        self.progress = 0
        self.progress_per_tick = int(self.CANVAS_HEIGHT / 120)

    def draw(self):
        image = Image.new('RGB', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        self.draw_mandel(image)
        self.save_image(image)
        image.show()

    def draw_mandel(self, image):
        draw = ImageDraw.Draw(image)
        for pixel_y in range(0, self.CANVAS_HEIGHT):
            for pixel_x in range(0, self.CANVAS_WIDTH):
                complex_coordinates = self.pixel_to_complex_coordinates(pixel_x, pixel_y)
                escape_iterations = self.calculate_escape_iterations(complex_coordinates)
                color = self.colorize(escape_iterations)
                draw.point((pixel_x, pixel_y), fill=color)
            self.show_progress()
        print()

    # recursive function, z[n] = z[n-1]^2 + C, with z[0] = 0 + 0i (i.e. origin of the complex plan)
    # z is a complex number with real component x and imaginary component y
    # the constant we add each iteration, C, corresponds to the point we are plotting
    def calculate_escape_iterations(self, complex_coordinates):
        z = complex(0, 0)
        for i in range(0, self.ESCAPE_DEPTH):
            if abs(z) > 2: return i
            z = z * z + complex_coordinates
        return 0

    def show_progress(self):
        self.progress = self.progress + 1
        if (self.progress == self.progress_per_tick):
            print('.', end='', flush=True)
            self.progress = 0

    def pixel_to_complex_coordinates(self, x, y):
        x_range = self.VIEWPORT['right'] - self.VIEWPORT['left']
        x_scaling_factor = self.CANVAS_WIDTH / x_range
        real = x / x_scaling_factor + self.VIEWPORT['left']

        y_range = self.VIEWPORT['bottom'] - self.VIEWPORT['top']
        y_scaling_factor = self.CANVAS_HEIGHT / y_range
        imag = y / y_scaling_factor + self.VIEWPORT['top']

        return complex(real, imag)

    def colorize(self, escape_iterations):
        intensity = escape_iterations / self.ESCAPE_DEPTH
        color = self.gradient[int(intensity * self.GRADIENT_SCALE)]
        return (int(color[0] * intensity), int(color[1] * intensity), int(color[2] * intensity))

    def rainbow_gradient(self):
        colors = [None] * self.GRADIENT_SCALE

        red_max_blue_increasing = int(self.GRADIENT_SCALE * 0 / 6)
        blue_max_red_decreasing = int(self.GRADIENT_SCALE * 1 / 6)
        blue_max_green_increasing = int(self.GRADIENT_SCALE * 2 / 6)
        green_max_blue_decreasing = int(self.GRADIENT_SCALE * 3 / 6)
        green_max_red_increasing = int(self.GRADIENT_SCALE * 4 / 6)
        red_max_green_decreasing = int(self.GRADIENT_SCALE * 5 / 6)

        sub_scale = int(self.GRADIENT_SCALE / 6)
        for i in range(0, sub_scale): colors[red_max_blue_increasing + i] = (255, 0, int((i / sub_scale) * 255))
        for i in range(0, sub_scale): colors[blue_max_red_decreasing + i] = (int((1 - i / sub_scale) * 255), 0, 255)
        for i in range(0, sub_scale): colors[blue_max_green_increasing + i] = (0, int((i / sub_scale) * 255), 255)
        for i in range(0, sub_scale): colors[green_max_blue_decreasing + i] = (0, 255, int((1 - i / sub_scale) * 255))
        for i in range(0, sub_scale): colors[green_max_red_increasing + i] = (int((i / sub_scale) * 255), 255, 0)
        for i in range(0, sub_scale): colors[red_max_green_decreasing + i] = (255, int((1 - i / sub_scale) * 255), 0)

        return colors

    def save_image(self, image):
        filename = "mandel-{left},{top}_{right},{bottom}_{scale:03d}_{escape:05d}_{width}x{height}".format(
            left=self.VIEWPORT['left'],
            top=self.VIEWPORT['top'],
            right=self.VIEWPORT['right'],
            bottom=self.VIEWPORT['bottom'],
            scale=self.GRADIENT_SCALE,
            escape=self.ESCAPE_DEPTH,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT)
        image.save(f'screenshots/{filename}.png', 'PNG')

Mandel().draw()

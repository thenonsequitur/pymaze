#!/usr/bin/env python

from PIL import Image, ImageDraw

class Mandel:
    COMPLEX_PLANE_VIEWPORT = { 'x': (-2.5, 1), 'y': (-1.25, 1.25) }
    #COMPLEX_PLANE_VIEWPORT = { 'x': (-0.1, 0), 'y': (-1.04, -0.96) }

    CANVAS_WIDTH = 1200
    x_range = COMPLEX_PLANE_VIEWPORT['x'][1] - COMPLEX_PLANE_VIEWPORT['x'][0]
    y_range = COMPLEX_PLANE_VIEWPORT['y'][1] - COMPLEX_PLANE_VIEWPORT['y'][0]
    aspect_ratio = x_range / y_range
    CANVAS_HEIGHT = int(CANVAS_WIDTH / aspect_ratio)

    MAX_ITERATIONS = 48

    RAINBOW_GRADIENT_SCALE = 1.0
    RAINBOW_GRADIENT_SIZE = int(RAINBOW_GRADIENT_SCALE * MAX_ITERATIONS)

    def __init__(self):
        self.gradient = self.rainbow_gradient(self.RAINBOW_GRADIENT_SIZE)
        self.progress = 0
        self.progress_per_tick = int(self.CANVAS_WIDTH * self.CANVAS_HEIGHT / 120)

    def draw(self):
        image = Image.new('RGB', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        self.draw_mandel(image)
        self.save_image(image)
        image.show()

    def draw_mandel(self, image):
        draw = ImageDraw.Draw(image)
        for pixel_x, pixel_y in self.for_each_pixel():
            complex_coords = self.pixel_to_complex_coordinates(pixel_x, pixel_y)
            num_iterations = self.count_iterations_at_coords(complex_coords)
            color = self.colorize(num_iterations)
            draw.point((pixel_x, pixel_y), fill=color)
            self.show_progress()
        print()

    # recursive function, z[n] = z[n-1]^2 + C, with z[0] = 0 + 0i (i.e. origin of the complex plan)
    # z is a complex number with real component x and imaginary component y
    # the constant we add each iteration, C, corresponds to the point we are plotting
    def count_iterations_at_coords(self, complex_coords):
        z = complex(0, 0)
        for i in range(0, self.MAX_ITERATIONS):
            if abs(z) > 2: return i
            z = z * z + complex_coords
        return self.MAX_ITERATIONS

    def for_each_pixel(self):
        for y in range(0, self.CANVAS_HEIGHT):
            for x in range(0, self.CANVAS_WIDTH):
                yield [x, y]

    def show_progress(self):
        self.progress = self.progress + 1
        if (self.progress == self.progress_per_tick):
            print('.', end='', flush=True)
            self.progress = 0

    def pixel_to_complex_coordinates(self, x, y):
        x_range = self.COMPLEX_PLANE_VIEWPORT['x'][1] - self.COMPLEX_PLANE_VIEWPORT['x'][0]
        x_scaling_factor = self.CANVAS_WIDTH / x_range
        real = x / x_scaling_factor + self.COMPLEX_PLANE_VIEWPORT['x'][0]

        y_range = self.COMPLEX_PLANE_VIEWPORT['y'][1] - self.COMPLEX_PLANE_VIEWPORT['y'][0]
        y_scaling_factor = self.CANVAS_HEIGHT / y_range
        imag = y / y_scaling_factor + self.COMPLEX_PLANE_VIEWPORT['y'][0]

        return complex(real, imag)

    def colorize(self, iterations):
        color = self.gradient[iterations % self.RAINBOW_GRADIENT_SIZE]
        intensity = 0 if iterations == self.MAX_ITERATIONS else iterations / self.MAX_ITERATIONS
        return (int(color[0] * intensity), int(color[1] * intensity), int(color[2] * intensity))

    def rainbow_gradient(self, full_scale):
        if (full_scale % 12 != 0): raise Exception("full_scale must be a multple of 12")
        colors = [None] * full_scale

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

    def save_image(self, image):
        filename = "mandel-{x0},{y0}_{x1},{y1}_{iterations}_{gradient}_{width}x{height}".format(
            x0=self.COMPLEX_PLANE_VIEWPORT['x'][0],
            y0=self.COMPLEX_PLANE_VIEWPORT['y'][0],
            x1=self.COMPLEX_PLANE_VIEWPORT['x'][1],
            y1=self.COMPLEX_PLANE_VIEWPORT['y'][1],
            iterations=self.MAX_ITERATIONS,
            gradient=self.RAINBOW_GRADIENT_SIZE,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT)
        image.save(f'screenshots/{filename}.png', 'PNG')

Mandel().draw()

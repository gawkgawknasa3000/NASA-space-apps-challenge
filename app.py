import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fast Orbit Simulation")

PURPLE = (160, 32, 240)  # Satellite color
GREY = (128, 128, 128)   # Moon color
BLUE = (100, 149, 237)    # Earth color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x + WIDTH / 2
        y = self.y + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x += WIDTH / 2
                y += HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

        # Display the name of the planet
        name_text = FONT.render(self.name, 1, WHITE)
        win.blit(name_text, (x - name_text.get_width() / 2, y - name_text.get_height() / 2))

    def update_position(self, earth):
        # Calculate distance to Earth
        distance_to_earth = math.sqrt(self.x ** 2 + self.y ** 2)
        if distance_to_earth == 0:
            return

        # Calculate orbital speed
        velocity = 35 / distance_to_earth  # Increase speed factor

        # Update velocities to create circular motion
        self.x_vel = -velocity * (self.y / distance_to_earth)
        self.y_vel = velocity * (self.x / distance_to_earth)

        # Update positions
        self.x += self.x_vel * 5  # Increase the speed multiplier
        self.y += self.y_vel * 5  # Increase the speed multiplier
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    # Create the Earth
    earth = Planet(0, 0, 16, BLUE, 1, "Earth")

    # Create the Moon orbiting the Earth
    moon = Planet(200, 0, 8, GREY, 0.01, "Moon")
    moon.y_vel = 10  # Much faster orbiting speed

    # Create the Satellite orbiting the Earth
    satellite = Planet(300, 0, 10, PURPLE, 0.01, "Satellite")
    satellite.y_vel = 15  # Much faster orbiting speed

    planets = [earth, moon, satellite]

    while run:
        clock.tick(100)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update positions of all planets
        for planet in planets:
            if planet != earth:
                planet.update_position(earth)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()

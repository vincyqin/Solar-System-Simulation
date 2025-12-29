import pygame, math, random

pygame.init()

# screen setup
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

# background stars
stars = [(random.randint(0, screen_width), random.randint(0, screen_height))for _ in range(100)]

# Sun's position
center_x, center_y = screen_width // 2, screen_height // 2

# Planets setup:
# name   : planet name
# desc   : short description
# color  : planet color in RGB
# radius : planet radius
# orbit  : distance from the Sun
# period : orbital period of the planet
# angle  : current angle along the orbit
planets = [
    {"name": "Mercury", "desc": "Closest planet to Sun", "color": (169,169,169), "radius": 4, "orbit": 50, "period": 88, "angle": 0},
    {"name": "Venus", "desc": "Second planet", "color": (255,215,0), "radius": 6, "orbit": 80, "period": 225, "angle": 0},
    {"name": "Earth", "desc": "Our home planet", "color": (0, 0, 255), "radius": 8, "orbit": 120, "period": 365, "angle": 0},
    {"name": "Mars", "desc": "The Red Planet", "color": (255, 0, 0), "radius": 6, "orbit": 160, "period": 687, "angle": 0},
    {"name": "Jupiter", "desc": "Largest planet", "color": (255,140,0), "radius": 14, "orbit": 210, "period": 4333, "angle": 0},
    {"name": "Saturn", "desc": "Planet with rings", "color": (210,180,140), "radius": 12, "orbit": 260, "period": 10759, "angle": 0},
    {"name": "Uranus", "desc": "Ice giant", "color": (0,255,255), "radius": 10, "orbit": 300, "period": 30687, "angle": 0},
    {"name": "Neptune", "desc": "Furthest planet", "color": (0,0,139), "radius": 10, "orbit": 340, "period": 60190, "angle": 0}
]

# Font
font = pygame.font.SysFont(None, 24)

# Controls of different views
show_orbits = True
paused = False
current_view = "solar"
moon_angle = 0

# Main loop
running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_o:
                show_orbits = not show_orbits

        # Mouse control
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_view == "solar":
                for planet in planets:
                    x = center_x + planet["orbit"] * math.cos(planet["angle"])
                    y = center_y + planet["orbit"] * math.sin(planet["angle"])
                    if planet["name"] == "Earth" and math.hypot(mouse_x - x, mouse_y - y) <= planet["radius"]:
                        current_view = "earth"
            elif current_view == "earth":
                current_view = "solar"

    # Background
    screen.fill((0, 0, 0))
    for sx, sy in stars:
        screen.set_at((sx, sy), (255, 255, 255))

    # Solar view's setting
    if current_view == "solar":
        # Draw Sun
        pygame.draw.circle(screen, (255, 255, 100), (center_x, center_y), 30)
        for i in range(50, 150, 10):
            alpha_surface = pygame.Surface((i*2, i*2), pygame.SRCALPHA)
            alpha_val = max(0, 150 - i*0.8)
            pygame.draw.circle(alpha_surface, (255, 255, 150, int(alpha_val)), (i, i), i)
            screen.blit(alpha_surface, (center_x - i, center_y - i))

        # Draw orbits
        if show_orbits:
            for planet in planets:
                pygame.draw.circle(screen, (100, 100, 100), (center_x, center_y), planet["orbit"], 1)

        # Draw planets
        for planet in planets:
            if not paused:
                planet["angle"] += 2*math.pi / planet["period"]

            x = center_x + planet["orbit"] * math.cos(planet["angle"])
            y = center_y + planet["orbit"] * math.sin(planet["angle"])
            pygame.draw.circle(screen, planet["color"], (int(x), int(y)), planet["radius"])

            # Hover info
            if math.hypot(mouse_x - x, mouse_y - y) <= planet["radius"]:
                info_surface = pygame.Surface((220, 50), pygame.SRCALPHA)
                info_surface.fill((0, 0, 0, 160))
                name_text = font.render(planet["name"], True, (255, 255, 255))
                desc_text = font.render(f"Period: {planet['period']} days", True, (200, 200, 200))
                info_surface.blit(name_text, (10, 5))
                info_surface.blit(desc_text, (10, 25))
                screen.blit(info_surface, (x + 15, y - 25))

        # Instructions
        instr = font.render("Press 'O' to toggle orbits, 'P' to pause, hover for info, click Earth to zoom.", True, (255, 255, 255))
        screen.blit(instr, (10, 10))
        
    # Earth view's setting
    elif current_view == "earth":
        # Draw Earth
        earth_radius = 50
        center_x, center_y = screen_width // 2, screen_height // 2
        pygame.draw.circle(screen, (0, 0, 255), (center_x, center_y), earth_radius)

        # Draw Moon
        moon_orbit = 100
        moon_radius = 15
        if not paused:
            moon_angle += 0.02
        moon_x = center_x + moon_orbit * math.cos(moon_angle)
        moon_y = center_y + moon_orbit * math.sin(moon_angle)
        pygame.draw.circle(screen, (200, 200, 200), (int(moon_x), int(moon_y)), moon_radius)

        # Moon info
        if math.hypot(mouse_x - moon_x, mouse_y - moon_y) <= moon_radius:
            info_surface = pygame.Surface((140, 30), pygame.SRCALPHA)
            info_surface.fill((0,0,0,160))
            moon_text = font.render("Moon", True, (255,255,255))
            info_surface.blit(moon_text, (10,5))
            screen.blit(info_surface, (moon_x + 15, moon_y - 15))

        # Instructions
        instr = font.render("Earth View | Click anywhere to return", True, (255, 255, 255))
        screen.blit(instr, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

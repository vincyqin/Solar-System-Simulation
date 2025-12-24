import pygame, math, random

pygame.init()

# Screen setup
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

# Background stars
stars = [(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(100)]

# Sun coordinates
center_x, center_y = screen_width // 2, screen_height // 2

# Planets (scaled radius and orbit)
# radius in pixels, orbit in pixels, period in Earth days (scaled to angular speed)
planets = [
    {"name": "Mercury", "desc": "Closest planet to Sun", "color": (169,169,169), "radius": 4, "orbit": 50, "period": 88, "angle": 0, "show_info": False},
    {"name": "Venus", "desc": "Second planet", "color": (255,215,0), "radius": 6, "orbit": 80, "period": 225, "angle": 0, "show_info": False},
    {"name": "Earth", "desc": "Our home planet", "color": (0, 0, 255), "radius": 8, "orbit": 120, "period": 365, "angle": 0, "show_info": False},
    {"name": "Mars", "desc": "The Red Planet", "color": (255, 0, 0), "radius": 6, "orbit": 160, "period": 687, "angle": 0, "show_info": False},
    {"name": "Jupiter", "desc": "Largest planet", "color": (255,140,0), "radius": 14, "orbit": 210, "period": 4333, "angle": 0, "show_info": False},
    {"name": "Saturn", "desc": "Planet with rings", "color": (210,180,140), "radius": 12, "orbit": 260, "period": 10759, "angle": 0, "show_info": False},
    {"name": "Uranus", "desc": "Ice giant", "color": (0,255,255), "radius": 10, "orbit": 300, "period": 30687, "angle": 0, "show_info": False},
    {"name": "Neptune", "desc": "Furthest planet", "color": (0,0,139), "radius": 10, "orbit": 340, "period": 60190, "angle": 0, "show_info": False}
]

# Font
font = pygame.font.SysFont(None, 24)

# Controls
show_orbits = True
paused = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Pause/Resume
                paused = not paused
            elif event.key == pygame.K_o:  # Toggle orbit display
                show_orbits = not show_orbits

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for planet in planets:
                x = center_x + planet["orbit"] * math.cos(planet["angle"])
                y = center_y + planet["orbit"] * math.sin(planet["angle"])
                if math.hypot(mouse_x - x, mouse_y - y) <= planet["radius"]:
                    planet["show_info"] = not planet.get("show_info", False)

    # Background
    screen.fill((0, 0, 0))
    for sx, sy in stars:
        screen.set_at((sx, sy), (255, 255, 255))

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
            planet["angle"] += 2*math.pi / planet["period"]  # angular speed proportional to period

        x = center_x + planet["orbit"] * math.cos(planet["angle"])
        y = center_y + planet["orbit"] * math.sin(planet["angle"])
        pygame.draw.circle(screen, planet["color"], (int(x), int(y)), planet["radius"])

        if planet.get("show_info", False):
            text_name = font.render(planet["name"], True, (255, 255, 255))
            text_desc = font.render(f"{planet['desc']} | Period: {planet['period']} days", True, (200, 200, 200))
            screen.blit(text_name, (x + 15, y - 10))
            screen.blit(text_desc, (x + 15, y + 10))

    # Instructions
    instr = font.render("Press 'O' to toggle orbits, 'P' to pause, click planet for info.", True, (255, 255, 255))
    screen.blit(instr, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

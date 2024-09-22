import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

font = pygame.font.SysFont(None, 32)

clock = pygame.time.Clock()

start_time = pygame.time.get_ticks()

time_up = 5

paused = False
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        counting_time = pygame.time.get_ticks() - start_time

        # change milliseconds into minutes, seconds, milliseconds
        counting_minutes = str(counting_time // 60000).zfill(2)
        counting_seconds = str(time_up - ((counting_time % 60000) // 1000)).zfill(2)
        # counting_millisecond = str(counting_time % 1000).zfill(3)

        

        # counting_string = "%s:%s:%s" % (
        #     counting_minutes,
        #     counting_seconds,
        #     counting_millisecond,
        # )

        if counting_seconds == "00":
            counting_string = "Time up"
            running = False
        
        else:
            counting_string = "%s:%s" % (
            counting_minutes,
            counting_seconds,
        )


        counting_text = font.render(str(counting_string), 1, (255, 255, 255))
        counting_rect = counting_text.get_rect(center=screen.get_rect().center)

    screen.fill((0, 0, 0))
    screen.blit(counting_text, counting_rect)

    pygame.display.update()

    clock.tick(60)

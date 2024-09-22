import pygame


time_up = 60
font = pygame.font.SysFont(None, 32)


def displayTimer():
    count_time = pygame.time.get_ticks() 
    minutes = str(count_time // 60000).zfill(2)
    seconds = str(time_up - ((count_time % 60000) // 1000)).zfill(2)

    display_timer = "%s:%s" % (
        minutes,
        seconds
    )

    return display_timer

    
    


import pygame
import time

# HERE pygame IS USED FOR LISTENING TO KEY PRESSES

def init():
  pygame.init()
  window = pygame.display.set_mode((400, 400))

def get_key(key_name):
  answer = False

  for event in pygame.event.get(): pass

  key_input = pygame.key.get_pressed()
  my_key = getattr(pygame, 'K_{}'.format(key_name))
  if key_input[my_key]:
    answer = True
  pygame.display.update()

  return answer

def control_input(drone):
    speed = 50
    lr, fb, ud, yw = 0, 0, 0, 0

    if get_key("w"):
        fb = speed
    elif get_key("s"):
        fb = -speed
    if get_key("a"):
        lr = -speed
    elif get_key("d"):
        lr = speed
    if get_key("SPACE"):
        ud = speed
    elif get_key("LCTRL"):
        ud = -speed
    if get_key("RIGHT"):
        yw = speed
    elif get_key("LEFT"):
        yw = -speed
    if get_key("t"):
        drone.takeoff()
    if get_key("q"):
        drone.land()
        time.sleep(4)
    return [lr, fb, ud, yw]

if __name__ == "__main__":
  init()
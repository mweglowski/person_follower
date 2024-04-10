import pygame

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

if __name__ == "__main__":
  init()
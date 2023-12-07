# 2-PLAYER-PONG
# - This is a graphical 2-Player Pong game.
# - The left player controls the left paddle and uses the 'q' and 'a' keys to control it.
# - The right player controls the right paddle and uses the 'p' and 'l' keys to control it.
# - There is ball that is initially directed to a player, the aim of a player is to hit the ball
#   using the paddle and to score points.
# - To score points, the ball has to hit the edge of the window of the other player. At the
#   same time the other player has to try and hit the ball so that it does not hit the edge
#   of their side of the window.
# - First player to reach 11 points wins the game.
# - The game stops when a player reaches 11 points.
# NOTE: TO MOVE THE LEFT PADDLE, PRESS DOWN Q AND A.
#       TO MOVE THE RIGHT PADDLE, PRESS DOWN P AND L.
# AUTHOR - RUSHABH SHAH

import pygame

# Main funtion of the game
def main():
   pygame.init()
   pygame.display.set_mode((500, 500))
   pygame.display.set_caption('Pong')   
   w_surface = pygame.display.get_surface() 
   game = Game(w_surface)
   game.play() 
   pygame.quit() 

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):

      # === objects ===
      self.background = pygame.image.load('background.jpg')
      self.winner = None
      self.surface = surface
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      left_paddle_x = self.surface.get_width() // 10
      right_paddle_x = self.surface.get_width() - left_paddle_x
      paddle_height = self.surface.get_height() // 2.5
      # === game specific objects ===
      self.small_ball = Ball('white', 10, [250, 250], [7, 7], self.surface)
      self.left_paddle = Paddle(left_paddle_x, paddle_height, 10, 50, 'white', self.surface)
      self.right_paddle = Paddle(right_paddle_x, paddle_height, 10, 50, 'white', self.surface)
      self.right_pointer = 0
      self.left_pointer = 0

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS)

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         elif event.type == pygame.KEYDOWN:
            self.handle_key_down(event)
         elif event.type == pygame.KEYUP:
            self.handle_key_up(event)     
   
   def handle_key_down(self, event):
      # Handle events when a key is pressed down
      # - self is the game to handle when a key is pressed down
      # - event is an arguement for an event
      if event.key == pygame.K_a:
         self.left_paddle.set_velocity(7)
      elif event.key == pygame.K_q:
         self.left_paddle.set_velocity(-7) 
      elif event.key == pygame.K_l:
         self.right_paddle.set_velocity(7)
      elif event.key == pygame.K_p:
         self.right_paddle.set_velocity(-7)      
         
   def handle_key_up(self, event):
      # Handle events when a key is released up
      # - self is the game to handle when a key is released up
      # - event is an arguement for an event      
      if event.key == pygame.K_a:
         self.left_paddle.set_velocity(0)
      elif event.key == pygame.K_q:
         self.left_paddle.set_velocity(0)
      elif event.key == pygame.K_l:
         self.right_paddle.set_velocity(0)
      elif event.key == pygame.K_p:
         self.right_paddle.set_velocity(0)

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      background = pygame.transform.scale(self.background, (500, 500))
      self.surface.blit(background, (0,0))
      self.small_ball.draw()
      self.left_paddle.draw()
      self.right_paddle.draw()
      self.draw_left_score()
      self.draw_right_score()
      if not self.continue_game:
         self.draw_winner_caption()
      pygame.display.update()

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      self.small_ball.move()
      self.left_paddle.move()
      self.right_paddle.move()
      self.small_ball.collide(self.left_paddle, self.right_paddle)
      
      if self.small_ball.touching_left():
         self.right_pointer += 1
      elif self.small_ball.touching_right():
         self.left_pointer += 1
   
   def draw_left_score(self):
      #  Function to draw the score box of the left player.
      # - self is the game to draw the left score

      string = str(self.left_pointer)
      font_size = 65
      font_name = 'Times New Roman'
      fg_color = pygame.Color('white')
      bg_color = None 
      font = pygame.font.SysFont(font_name, font_size)
      text_box = font.render(string, True, fg_color, bg_color)
      location = (0, 0)
      self.surface.blit(text_box, location)
      
   def draw_right_score(self):
      #  Function to draw the score box of the right player.
      # - self is the game to draw the right score
      string = str(self.right_pointer)
      font_size = 65
      font_name = 'Times New Roman'
      fg_color = pygame.Color('white')
      bg_color = None
      font = pygame.font.SysFont(font_name, font_size)
      text_box = font.render(string, True, fg_color, bg_color)
      h1 = self.surface.get_width()
      h2 = text_box.get_width()  
      location = (h1 - h2, 0)
      self.surface.blit(text_box, location)
   
   def draw_winner_caption(self):
      #  Function to draw the caption for the winner of the game.
      # - self is the game to draw the caption
      font_size = 60
      font_name = 'Aharoni'
      fg_color = pygame.Color('white')
      bg_color = None
      winner_string = self.winner + " Wins!"
      font = pygame.font.SysFont(font_name, font_size)
      text_box = font.render(winner_string, True, fg_color, bg_color)
      text_rect = text_box.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2))
      self.surface.blit(text_box, text_rect)
   
   def decide_continue(self):
      # To decide when the game ends i.e. when either player's score reaches 11.
      # - self is the game to decide continuation upon
      if self.left_pointer == 11 or self.right_pointer == 11:
         if self.left_pointer == 11:
            self.winner = "Left Player"
         else:
            self.winner = "Right Player"
         self.continue_game = False

class Ball:
   # An object in this class represents a ball that moves 
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
      
   def move(self):
      # Change the location of the ball by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the Dot
      size = self.surface.get_size()
      for i in range(0,2):
         self.center[i] = (self.center[i] + self.velocity[i])
         if self.center[i] <= self.radius or self.center[i] + self.radius >= size[i]:
            self.velocity[i] = -self.velocity[i]    
         
   def draw(self):
      # Draw the ball on the surface
      # - self is the ball
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
   
   def touching_left(self): # Helper function
      # Checks whether the ball is in contact with the left wall.
      return self.center[0] < self.radius
   
   def touching_right(self): # Helper function
      # Checks whether the ball is in contact with the right wall.
      return self.center[0] + self.radius > self.surface.get_width()
   
   def collide(self,left_paddle,right_paddle):
      # Function to rebound the ball upon hitting either paddles.
      if left_paddle.rect.collidepoint(self.center) and self.velocity[0]<0:
            self.velocity[0] = -self.velocity[0]
      elif right_paddle.rect.collidepoint(self.center) and self.velocity[0]>0:
            self.velocity[0] = -self.velocity[0]

class Paddle:
   # An object in this class represents a paddle that moves 
   
   def __init__(self, x, y, width, height, color, surface):
      self.rect = pygame.Rect(x, y, width, height)
      self.color = pygame.Color(color)
      self.surface = surface
      self.v_velocity = 0
      
   def draw(self):
      # Draw the paddle on the surface
      # - self is the paddle    
      pygame.draw.rect(self.surface, self.color, self.rect)
   
   def set_velocity(self, distance):
      # Sets the vertical velocity to the distance moved by the paddle
      # self is the paddle
      # distance is the units by which the paddle moves
      self.v_velocity = distance
   
   def move(self):
      # Moves the paddle upto certain points on the surface
      # self is the paddle
      self.rect.move_ip(0, self.v_velocity) # This moves the paddle in place!
      # Example: surface height = 500
      # right of rect was 495, we added 10, it could've been 505
      # BUT we can't go there, so we'll just assign 500 to bottom of the paddle and 0 to the top
      if self.rect.bottom >= self.surface.get_height():
         self.rect.bottom = self.surface.get_height()
      elif self.rect.top <= 0:
         self.rect.top = 0

main()

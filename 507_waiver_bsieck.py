"""
 Sample code for SI 507 Waiver Assignment
 University of Michigan School of Information

 MODIFIED BY: Brennan Sieck

 Based on "Pygame base template for opening a window" 
     Sample Python/Pygame Programs
     Simpson College Computer Science
     http://programarcadegames.com/
     http://simpson.edu/computer-science/
 
See README for the assignment for instructions to complete and submit this.

[ x ] accepting command line arguments
[ x ] searching wikipedia
[ x ] using nltk to parse the contents of wikipedia pages
[ x ] drawing balls with the most common adjectives extracted from wikipedia pages
[ x ] allowing the user to delete balls using the keyboard
[ x ] when all balls are deleted, display game over screen

"""
import sys
from collections import Counter
import pygame
import random
import wikipedia
import nltk
from nltk import word_tokenize,sent_tokenize
import test


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# READ COMMAND LINE ARGS

searchTerm = str(sys.argv[1])

print('Scraping Wikipedia pages related to '+ searchTerm +'...')

# SEARCH WIKIPEDIA

return_pos_array = []

page_results = wikipedia.search(searchTerm, 5)

for page in page_results:
    
    temp_page = wikipedia.page(page)
    page_content = temp_page.content
    # PARSE TEXT WITH NLTK

    tokens = nltk.word_tokenize(page_content)
    tagged = nltk.pos_tag(tokens)

    for j,k in tagged:
        if (k=="JJ"):
            return_pos_array.append(j)




# print(page_content)



counts = Counter(return_pos_array).most_common(6) 

temp_word_list = []

for j,k in counts:
    temp_word_list.append(j)
    

return_pos_dict = {"JJ": counts}

print(return_pos_dict)

# print(temp_word_list)
  


# You must construct a dictionary of this form from your wikipedia search
# See test.py for more details on the format requirements for the dictionary

# this test expects the following data structure
# {<POS_CODE1>: [(<WORD1_1>, <WORD1_1_FREQ>), (<WORD1_2>, <WORD1_2_FREQ>), ...],
#  <POS_CODE2>: [(<WORD2_1>,<WORD2_1_FREQ>), (<WORD2_2>: <WORD2_2_FREQ>), ...},
#   ... 
# }



# sample_pos_dict = {"JJ": [("happy", 5), ("sad", 4)], "NN": [("ball", 3), ("bat", 2)]}

# You must leave this line in your submission, and you must pass the test!
if test.test(return_pos_dict):
    print ("You passed this sample_pos_diction part of the test!")
else:
    print ("You didn't pass. Please try again")

# This is the temp word list for testing.
# You will need to **replace this** with words extracted from your wikipedia search.
# See README for more details.
word_list = temp_word_list

# The class that manages the balls shown on the screen in the game.
class BallManager:

    INIT_SPEED = 1
    current_index = 0

    def __init__(self):
        self.max_balls = 3
        self.active_balls = []
        for w in word_list: 
            self.active_balls.append(WordBall(w, self.INIT_SPEED))


    def create_ball(self, word):
        self.active_balls += WordBall(word, self.INIT_SPEED)

    def destroy_ball(self, word):
        for ball in self.active_balls:
            if(ball.word) == word:
                self.active_balls.remove(ball)
    
    def num_balls(self):
        return len(self.active_balls)

    def __str__(self):
        s = ''
        for b in self.active_balls:
            s += b.word + ", "
        return s

# The class for each ball showing on the screen.
# You can play around with size, color, font, etc. 
class WordBall:

    def __init__(self, word, speed):
        self.word = word
        self.x_pos = random.randint(0, pygame.display.Info().current_w)
        self.y_pos = 0
        self.height = 100
        self.width = 100
        self.speed = speed
        self.is_active = 1;

    def move_ball(self):
        self.y_pos += self.speed
        if (self.y_pos > pygame.display.Info().current_h - self.height):
            self.y_pos = 0

# Initialize game
pygame.init()

size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Type to Win")
clock = pygame.time.Clock()
 
# Loop until the user clicks the close button...

ball_manager = BallManager()

ball_font = pygame.font.Font(None, 36)
keys_font = pygame.font.Font(None, 60)
done = False
game_over = False
keys_typed = ''

# Main display loop
while not done:
    
    # Win condition (no more active balls)
    if (len(ball_manager.active_balls)==0):
        # Handle input events.
        key = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Render GAME OVER SCREEN
        game_over = True
        screen.fill(BLACK)

        text = keys_font.render('GAME OVER', 1, WHITE)
        textpos = text.get_rect()
        textpos.centerx = pygame.display.Info().current_w / 2
        textpos.centery = pygame.display.Info().current_h / 2
        screen.blit(text, textpos)

        # Update the screen with what we've drawn.
        pygame.display.flip()
     
        # Limit to 60 frames per second
        clock.tick(60)

    else :
        # Handle input events.
        key = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                key = event.unicode
                keys_typed += key




        # Manipulate game objects.
        for b in ball_manager.active_balls:
            b.move_ball()


        # Blank the screen
        screen.fill(WHITE)

        # Render game objects
        for ball in ball_manager.active_balls:
            if(ball.is_active):
                pygame.draw.ellipse(screen, RED, [ball.x_pos, ball.y_pos, ball.width, ball.height]) 
                text = ball_font.render(ball.word, 1, BLACK)
                textpos = text.get_rect()
                textpos.centerx = ball.x_pos + ball.width / 2
                textpos.centery = ball.y_pos + ball.height / 2
                screen.blit(text, textpos)
        

        # If a char is typed that matches the first char of a ball's word, destroy it
        for ball in ball_manager.active_balls:
            for char in keys_typed:
                if(ball.word[0] == char):
                    ball.is_active = 0
                    ball_manager.destroy_ball(ball.word)

                    



     
        text = keys_font.render('keys typed: ' + keys_typed, 1, GREEN)
        textpos = text.get_rect()
        textpos.centerx = pygame.display.Info().current_w / 2
        textpos.centery = pygame.display.Info().current_h - 30
        screen.blit(text, textpos)




        # Update the screen with what we've drawn.
        pygame.display.flip()
     
        # Limit to 60 frames per second
        clock.tick(60)

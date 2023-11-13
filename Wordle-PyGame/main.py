import pygame
import sys
import random
from words5 import *
from words6 import *
from words4 import *
from words7 import *
from words8 import *

pygame.init()

# Constants

WIDTH, HEIGHT = 1300, 700

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("Wordle-PyGame/assets/tabla5.png")
BACKGRONDPREGUNTA= pygame.image.load("Wordle-PyGame/assets/backgroundpregunta.jpg")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(216, 300))
ICON = pygame.image.load("Wordle-PyGame/assets/Icon.png")

pygame.display.set_caption("Wordle!")
pygame.display.set_icon(ICON)

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"

CORRECT_WORD = "true"

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

GUESSED_LETTER_FONT = pygame.font.Font("Wordle-PyGame/assets/FreeSansBold.otf", 35)
AVAILABLE_LETTER_FONT = pygame.font.Font("Wordle-PyGame/assets/FreeSansBold.otf", 15)


# Dibuja la pantalla de selección de dificultad
# Dibuja la pantalla de selección de dificultad
def draw_difficulty_selection():
    SCREEN.fill("white")
    SCREEN.blit(BACKGRONDPREGUNTA, BACKGROUND_RECT)

    if user_selected_difficulty is None:
        question_font = pygame.font.Font(None, 36)
        question_text = question_font.render("Seleccione la dificultad (entre 4 y 8 letras):", True, GREEN)
        question_rect = question_text.get_rect(center=(WIDTH // 2 +100,  30))
        SCREEN.blit(question_text, question_rect)

        input_font = pygame.font.Font(None, 36)
        input_text = input_font.render(difficulty_input, True, GREY)
        input_rect = input_text.get_rect(center=(WIDTH // 2 +100,  80))
        pygame.draw.rect(SCREEN, GREY, (input_rect.left - 10, input_rect.top - 10, input_rect.width + 20, input_rect.height + 20), 2)
        SCREEN.blit(input_text, input_rect)

    pygame.display.flip()


# Obtener la dificultad del usuario
difficulty_input = "4"  # Valor predeterminado
user_selected_difficulty = None



# Bucle de selección de dificultad
while user_selected_difficulty is None:
    draw_difficulty_selection()  # Dibuja la interfaz de selección de dificultad

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                selected_difficulty = int(difficulty_input)
                if 4 <= selected_difficulty <= 8:
                    user_selected_difficulty = selected_difficulty
                        
                    # Configura el juego según la dificultad seleccionada
                else:
                    print("Dificultad no válida. Debe ser entre 4 y 8 letras.")
            elif event.key == pygame.K_BACKSPACE:
                difficulty_input = difficulty_input[:-1]
            elif event.key in range(48, 58):  # Teclas numéricas
                difficulty_input += event.unicode
    if user_selected_difficulty is not None:
        break  # El usuario ha seleccionado la dificultad, sal del bucle


print(user_selected_difficulty)
SCREEN.fill("white")
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)



pygame.display.update()

LETTER_X_SPACING = 85
LETTER_Y_SPACING = 12
LETTER_SIZE = 75

# Global variables

guesses_count = 0

# guesses is a 2D list that will store guesses. A guess will be a list of letters.
# The list will be iterated through and each letter in each guess will be drawn on the screen.
guesses = [[]] * 6

current_guess = []
current_guess_string = ""
current_letter_bg_x = 8

# Indicators is a list storing all the Indicator object. An indicator is that button thing with all the letters you see.
indicators = []

game_result = ""

class Letter:
    def __init__(self, text, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(SCREEN, "white", self.bg_rect)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)
        pygame.display.update()



class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 57, 75)
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=(self.x+27, self.y+30))
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

# Drawing the indicators on the screen.

indicator_x, indicator_y = 700, 20

for i in range(3):
    for letter in ALPHABET[i]:
        new_indicator = Indicator(indicator_x, indicator_y, letter)
        indicators.append(new_indicator)
        new_indicator.draw()
        indicator_x += 60
    indicator_y += 100
    if i == 0:
        indicator_x = 730
    elif i == 1:
        indicator_x = 785

def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    game_decided = False
    for i in range(user_selected_difficulty):
        print("guess_to_check: ",guess_to_check)
        
        lowercase_letter = guess_to_check[i].text.lower()
        print("lowercase_letter", lowercase_letter)
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = GREEN
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = GREEN
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = YELLOW
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = YELLOW
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            for indicator in indicators:
                if indicator.text == lowercase_letter.upper():
                    indicator.bg_color = GREY
                    indicator.draw()
            guess_to_check[i].text_color = "white"
            game_result = ""
            game_decided = True
        guess_to_check[i].draw()
        print(guess_to_check)
        pygame.display.update()
    
    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 8

    if guesses_count == 6 and game_result == "":
        game_result = "L"

def play_again():
 

    # Puts the play again text on the screen.
    pygame.draw.rect(SCREEN, "white", (10, 600, 1000, 600))
    play_again_font = pygame.font.Font("Wordle-PyGame/assets/FreeSansBold.otf", 20)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 500))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 650))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    
    pygame.display.update()


    
    

def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
    SCREEN.fill("white")
    SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
    guesses_count = 0

    if user_selected_difficulty==4:
        CORRECT_WORD = random.choice(WORDS4)
    elif user_selected_difficulty==5:
        CORRECT_WORD = random.choice(WORDS)
    elif user_selected_difficulty==6:
        CORRECT_WORD = random.choice(WORDS6)
    elif user_selected_difficulty==7:
        CORRECT_WORD = random.choice(WORDS7)
    elif user_selected_difficulty==8:
        CORRECT_WORD = random.choice(WORDS8)     
    print(CORRECT_WORD) 
    
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    game_result = ""
    pygame.display.update()
    for indicator in indicators:
        indicator.bg_color = OUTLINE
        indicator.draw()

def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count*100+LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING


# print("Que dificultad deseas? escoge entre 4 y 8 letras")
# N=int(input())


# El usuario ha seleccionado la dificultad, ahora puedes configurar tu juego
# Utiliza user_selected_difficulty para configurar tu juego

# Bucle principal del juego
# Bucle del juego principal
while True:
    if game_result != "":
        
        play_again()  # Muestra el mensaje de "Jugar de nuevo"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    pregunta=True
                    user_selected_difficulty=None

                    # Bucle de selección de dificultad
                    while pregunta==True:
                        draw_difficulty_selection()  # Dibuja la interfaz de selección de dificultad

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    selected_difficulty = int(difficulty_input)
                                    if 4 <= selected_difficulty <= 8:
                                        user_selected_difficulty = selected_difficulty
                                            
                                        # Configura el juego según la dificultad seleccionada
                                    else:
                                        print("Dificultad no válida. Debe ser entre 4 y 8 letras.")
                                elif event.key == pygame.K_BACKSPACE:
                                    difficulty_input = difficulty_input[:-1]
                                elif event.key in range(48, 58):  # Teclas numéricas
                                    difficulty_input += event.unicode
                        if user_selected_difficulty is not None:
                            pregunta=False  # El usuario ha seleccionado la dificultad, sal del bucle
                    print(user_selected_difficulty)
                    reset()  # Reinicia el juego
                else:
                    if len(current_guess_string) == user_selected_difficulty and ((current_guess_string.lower() in WORDS) or (current_guess_string.lower() in WORDS4)):
                        # print("wordcurrent: " ,current_guess)
                        print(user_selected_difficulty)
                        check_guess(current_guess)  # Verifica la conjetura del usuario
                        # print("current string : " , current_guess_string.lower())

                        
                   
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()  # Borra la última letra ingresada
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(current_guess_string) < user_selected_difficulty:
                        create_new_letter()  # Crea una nueva letra en la conjetura

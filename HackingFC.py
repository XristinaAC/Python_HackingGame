from uagame import Window
from time import sleep
from random import randint, choice

def create_window():
    window = Window('Hacking', 600, 500)
    window.set_font_name('couriernew')
    window.set_font_size(18)
    window.set_font_color('green')
    window.set_bg_color('black')
    return window

def display_line(window, string, location, string_height):
    sleep_time = 0.3

    window.draw_string(string, location[0], location[1])
    window.update()
    sleep(sleep_time)
    location[1] = location[1] + string_height

#Creating the games's header
def display_header(window, location, attempts, string_height):
    header_list = ['DEBUG MODE',str(attempts)+' ATTEMPT(S) LEFT', '']

    for header_line in header_list:
        display_line(window, header_line, location, string_height)

def embed_password(password, size):
    fill = '!@#$%^*()-+=~[]{}'
    embedding = ''
    password_size = len(password)
    split_index = randint(0, size - password_size)

    for index in range(0, split_index):
        embedding = embedding + choice(fill)

    embedding = embedding + password
    split_index = size - len(embedding)

    for index in range(0, split_index):
        embedding = embedding + choice(fill)

    return embedding

def display_password_list(window, location, string_height):
    with open('PasswordList.txt') as f:
        password_list = [line[:-1] for line in f]
    f.close()

    for password in password_list:
        size = (20 - len(password)) + len(password)
        embe_password = embed_password(password, size)
        display_line(window, embe_password, location, string_height)

    display_line(window, '', location, string_height)

    password = randint(0, len(password_list)-1)
    return password_list[password]

#Prompt the player for a password guess
def prompt_user(window, prompt, location):
    user_input = window.input_string(prompt, location[0], location[1])

    return user_input

def display_hint(window, password, guess, location, string_height):
    display_line(window, guess+' INCORRECT', location, string_height)
    correct_letters = 0

    for index in range(len(guess)):
        if len(guess) <= len(password) and (password[index] == guess[index]):
            correct_letters += 1

    hint = str(correct_letters)+ '/'+str(len(password))+' IN MATCHING POSITIONS'
    display_line(window, hint, location, string_height)


def check_warning(window, attempts_left, string_height):
    if attempts_left == 1:
        warning = '*** LOCKOUT WARNING ***'
        pos_x = window.get_width() - window.get_string_width(warning)
        pos_y = window.get_height() - string_height
        window.draw_string(warning, pos_x, pos_y)

def get_guesses(window, password, location, attempts_left,string_height):
    attempts_left = attempts_left - 1
    guess = prompt_user(window, 'ENTER PASSWORD >', location)
    location[1] = location[1] + string_height

    line_x = window.get_width()//2
    line_y = 0
    location_h = [line_x,line_y]

    while guess != password and attempts_left > 0:
        window.draw_string(str(attempts_left), location[0], string_height)
        check_warning(window, attempts_left, string_height)

        display_hint(window, password, guess, location_h, string_height)

        guess = prompt_user(window, 'ENTER PASSWORD >', location)
        location[1] = location[1] + string_height

        attempts_left = attempts_left - 1

    window.clear()

    return guess

def check_password(guess,password):
    if guess == password:
        outcome_list = [guess,'','EXITING DEBUG MODE','', 'LOGIN SUCCESSFUL - WELCOME BACK','']
        exit_message = 'PRESS ENTER TO CONTINUE'
        outcome_tuple = (outcome_list, exit_message)
    else:
        outcome_list = [guess,'','LOGIN FAILURE - TERMINAL LOCKED', '','PLEASE CONTACT AN ADMINISTRATOR','']
        exit_message = 'PRESS ENTER TO EXIT'
        outcome_tuple = (outcome_list, exit_message)

    return outcome_tuple

def display_outcome(window, outcome,string_height):
    #Display the player's password guess
    outcome_height = (len(outcome[0]) + 1) * string_height
    y_space = window.get_height() - outcome_height
    line_y = y_space // 2
    location = [0,line_y]

    #Displaying the rest of the outcome
    for outcome_elem in outcome[0]:
        x_space = window.get_width() - window.get_string_width(outcome_elem)
        line_x = x_space // 2
        location[0] = line_x
        display_line(window, outcome_elem, location, string_height)

    x_space = window.get_width() - window.get_string_width(outcome[1])
    line_x = x_space // 2

    location[0] = line_x

    prompt_user(window, outcome[1], location)

def end_game(window, guess, password,string_height):
    outcome = check_password(guess,password)
    display_outcome(window, outcome,string_height)

    window.close()

def main():
    location = [0,0]
    attempts = 4

    window = create_window()
    string_height = window.get_font_height()

    display_header(window,location, attempts, string_height)
    password = display_password_list(window, location, string_height)
    guess    = get_guesses(window, password, location, attempts,string_height)
    end_game(window, guess, password,string_height)

main()

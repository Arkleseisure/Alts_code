import pygame
from pygame import freetype
import os
import time
import copy

screen_width = 1400
screen_height = 700

match_display_width = screen_width * 0.9


WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
OXFORD_BLUE = [0, 33, 71]

background_colour = BLACK
text_colour = WHITE

game_time = 180

# creates a pygame window in the center of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill(background_colour)
pygame.display.set_caption("Alts")

absolute_path = os.path.dirname(os.path.abspath(__file__))

'''
Parent class for many different objects which are rectangular and may have text in them

width: width of the box
height: height of the box
x: x coordinate of the top left of the box (using pygame's grid... top left of screen is (0, 0), and each unit is 1 pixel across)
y: y coordinate of the top left of the box
colour: RGB value of the background of the box, 0-255 for each colour
text: text which appears in the center of the box
font: font the text appears in
font_size: size of the font
font_colour: RGB value, 0-255 for each like the background
bold: boolean determining whether the text is bold
italic: boolean determining whether the text is italic
'''
class RectangleSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, x=0, y=0, colour=[0,0,0], text='', font='Calibri', font_size=40, font_colour=[0,0,0], bold=False, italic=False, image='', name='', left_align=False):
        super().__init__()

        # creates pygame surface object onto which the label can be placed
        self.image = pygame.Surface([width, height])
        if name:
            self.name = name
        else:
            self.name = text

        # sets the position of the sprite
        self.rect = self.image.get_rect()
        if left_align:
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.x = x - width//2
            self.rect.y = y - height//2

        # draws the background colour onto the image
        pygame.draw.rect(self.image, colour, [0, 0, width, height])
        self.colour = colour
        if text:
            self.font = font
            self.font_size = font_size
            self.font_colour = font_colour
            self.bold = bold
            self.italic = italic
            self.text = text
            # creates a surface with the text on it
            font = pygame.freetype.SysFont(font, font_size, bold=bold, italic=italic)
            print_image, rect = font.render(text, font_colour)

            # sticks this surface to the image such that it is centralized
            text_width, text_height = print_image.get_size()
            self.image.blit(print_image, ((width - text_width)//2, (height - text_height)//2))

        if image:
            button_image = pygame.image.load(absolute_path + '/' + image + '.png')
            button_image = pygame.transform.scale(button_image, [width, height])
            self.image.blit(button_image, (0, 0))
            self.image.set_colorkey(WHITE)


'''
Class for any buttons
x, y: same as for the square class
width, height: width and height of the button
colour: colour of the background of the button, RGB 0-255
text: text in the button
image: image in the button
'''
class Button(RectangleSprite):
    def __init__(self, x, y, width=screen_width//10, height=screen_height//10, colour=[100, 100, 100], text='', font='Calibri', font_size=40, font_colour=[0,0,0], bold=False, italic=False, image='', left_align=False, name=''):
        super().__init__(width=width, height=height, x=x, y=y, colour=colour, text=text, font=font, font_size=font_size, font_colour=font_colour, bold=bold, italic=italic, image=image, left_align=left_align)
        self.width = width
        self.height = height
        if name:
            self.name = name
        else:
            self.name = text

    # returns True if the given x, y coordinates are within the button, False if not
    def is_clicked(self, x, y):
        return self.rect.x < x < self.rect.x + self.width and self.rect.y < y < self.rect.y + self.height
     

'''
Class to hold the blueprint for drawing the clock
Most elements are the same as the Rectangle Sprite class, but it also has the update and get_text functions 
so that it can keep on changing with as the timer ticks down
'''
class Clock(RectangleSprite):
    def __init__(self, width, height, x, y, colour, time_remaining, font_size, left_align=False):
        super().__init__(width, height, x, y, colour, self.get_text(time_remaining), font_size=font_size, left_align=left_align, bold=True)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.colour = colour
        self.font_size = font_size
        self.left_align = left_align
        self.name = 'clock'

    # gets the text to be displayed given a certain number of seconds remaining on the clock
    def get_text(self, time_remaining):
        minutes = str(int(round(time_remaining) // 60))
        if time_remaining < 0:
            seconds = '00'
        elif round(time_remaining) % 60 < 9.5:
            seconds = '0' + str(round(time_remaining) % 60)
        else:
            seconds = str(round(time_remaining) % 60)
        return minutes + ':' + seconds

    def update(self, time_remaining):
        # creates a surface with the text on it
        text = self.get_text(time_remaining)
        font = pygame.freetype.SysFont('Calibri', self.font_size, bold=True)
        print_image, rect = font.render(text, BLACK)

        # sticks this surface to the image such that it is centralized
        self.image.fill(self.colour)
        text_width, text_height = print_image.get_size()
        self.image.blit(print_image, ((self.width - text_width)//2, (self.height - text_height)//2))


# prints text to the screen
def print_screen(text, x, y, size, colour, surface=screen, left_align=True, font_type="Calibri"):
    # turns the text into a pygame surface
    font = pygame.freetype.SysFont(font_type, size, True)
    print_image, rect = font.render(text, colour)

    # blits the new text surface onto the given surface and updates the screen
    if not left_align:
        text_width, text_height = print_image.get_size()
        surface.blit(print_image, (x - text_width//2, y - text_height//2))
    else:
        surface.blit(print_image, (x, y))
    return print_image.get_size()


def print_title(colour):
    title_size = 125
    print_screen('ALTS', screen_width//2, screen_height*0.15, title_size, colour, left_align=False)


def print_match_set(matches, y):
    for i in range(len(matches)):
        if matches[i]:
            print_screen(str(matches[i].teams[0].team_number) + 'v' + str(matches[i].teams[1].team_number), (i + 1) * match_display_width//(len(matches) + 1) + (screen_width - match_display_width)//2, y, size=45, colour=text_colour, left_align=False)


def get_team_and_match_sprites(num_teams, num_sides):
    # adds the text for changing number of teams and number of sides
    x = screen_width*0.75
    y = screen_height * 0.125
    vertical_gap = screen_height * 0.03
    text_size = screen_height * 0.03
    teams = RectangleSprite(screen_width * 0.15, vertical_gap, x, y, background_colour, 'Teams: ' + str(num_teams), font_size=text_size, font_colour=text_colour, name='teams', left_align=False)
    y += vertical_gap
    texts = {
        1: 'Full Ice',
        2: 'Half Ice',
        3: 'Third Ice',
    }
    text = 'Matches: ' + texts.get(num_sides, str(num_sides))
    matches = RectangleSprite(screen_width * 0.15, vertical_gap, x, y, background_colour, text, font_size=text_size, font_colour=text_colour, name='matches', left_align=False)

    # adds button to change number of teams and number of sides
    change = Button(x + screen_width*0.12, y - vertical_gap//2, screen_width * 0.1, screen_height * 0.07, text='Change', font_size=32, bold=True, left_align=False, name='change')

    return teams, matches, change


def create_sprites(num_teams, num_sides):
    # creates the highlights for the current matches
    highlight_length = match_display_width * num_sides//(num_sides + 1)
    highlight_height = screen_height * 0.17
    highlight_width = screen_height * 0.02
    highlight_x = (screen_width - highlight_length)//2
    highlight_y = (screen_height - highlight_height)//2
    highlight_colour = [150, 150, 205]
    top_highlight = RectangleSprite(highlight_length, highlight_width, highlight_x, highlight_y,  colour=highlight_colour, left_align=True)
    bottom_highlight = RectangleSprite(highlight_length, highlight_width, highlight_x, highlight_y + highlight_height - highlight_width, colour=highlight_colour, left_align=True)

    # creates the items that appear on the bottom line of the screen
    bottom_line_y = screen_height * 0.8
    bottom_line_height = screen_height * 0.1
    bottom_line_spacing = screen_width * 0.03
    bottom_line_font_size = screen_height * 0.06
    clock_width = screen_width//10
    x = screen_width//2 - clock_width//2
    clock = Clock(clock_width, bottom_line_height, x, bottom_line_y, colour=highlight_colour, time_remaining=game_time, font_size=bottom_line_font_size, left_align=True)
    x -= 3 * bottom_line_spacing + 3 * bottom_line_height
    pause = Button(x, bottom_line_y, bottom_line_height, bottom_line_height,  image='pause', left_align=True, name='pause')
    x += bottom_line_height + bottom_line_spacing
    play = Button(x, bottom_line_y, bottom_line_height, bottom_line_height, image='play', left_align=True, name='play')
    x += bottom_line_height + bottom_line_spacing
    skip = Button(x, bottom_line_y, bottom_line_height, bottom_line_height, image='skip', left_align=True, name='skip')
    x += bottom_line_height + 2 * bottom_line_spacing + clock_width
    change_matches = Button(x, bottom_line_y, height=bottom_line_height, width=screen_width*0.2, text='Change match', font_size=bottom_line_font_size, bold=True, left_align=True, name = 'change match')
    restart = Button(screen_width*0.04, screen_height*0.07, screen_width*0.14, screen_height * 0.115, image='restart', left_align=True, name='restart')

    teams, matches, change = get_team_and_match_sprites(num_teams, num_sides) 

    # creates a group to draw the background features to the screen.
    background_group = pygame.sprite.Group()
    background_group.add(top_highlight, bottom_highlight, clock, teams, matches)
    button_group = pygame.sprite.Group()
    button_group.add(pause, play, skip, change, restart, change_matches)

    return background_group, button_group

# waits until a button is clicked and then returns the name of the button clicked.
def get_button_click(button_group, down_click=False):
    for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONUP and not down_click) or (event.type == pygame.MOUSEBUTTONDOWN and down_click):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in button_group:
                if button.is_clicked(mouse_x, mouse_y):
                    return button.name
        elif event.type == pygame.QUIT:
            return 'quit'


# draws a display which shows a question with various possible answers, then returns the answer chosen
def draw_question_box(question, answers):
    # parameters of the question box
    box_width = screen_width*0.45
    box_height = screen_height*0.75
    box_colour = [50, 50, 50]
    box_x = screen_width//2
    box_y = screen_height//2

    # creates the question box along with the groups for drawing to the screen and detecting button clicks
    box = RectangleSprite(box_width, box_height, box_x, box_y, box_colour, left_align=False)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(box)
    buttons = pygame.sprite.Group()

    # question space is the quantity of the box held by the question, question_spaceing is the gap between lines in the question
    # for questions long enough that they don't just fit on one line
    question_space = box_height//3
    question_size = 42
    question_spaceing = question_size * 1.1
    y = (question_space - question_spaceing * (len(question) - 1))//2
    # prints the question onto the box
    for part in question:
        print_screen(part, box_width//2, y, size=question_size, colour=BLACK, surface=box.image, left_align=False)
        y += question_spaceing

    # parameters for displaying the question and answers
    if len(answers) >= 5:
        grid_height = 5
        grid_width = len(answers)//5
        if len(answers) % 5 != 0:
            grid_width += 1
    else:
        grid_height = len(answers)
        grid_width = 1
    button_vertical_gap = (box_height - question_space)//grid_height
    button_horizontal_gap = box_width//grid_width
    x = box_x - (grid_width - 1) * button_horizontal_gap//2
    y = box_y - box_height//2 + question_space + button_vertical_gap//2
    button_colour = [100, 100, 100]

    buttons_done = 0
    # creates buttons for each of the answers
    for answer in answers:
        new_button = Button(x, y, button_horizontal_gap * 0.7, button_vertical_gap * 0.7, button_colour, text=answer, left_align=False)
        all_sprites.add(new_button)
        buttons.add(new_button)
        buttons_done += 1
        if buttons_done % 5 == 0:
            x += button_horizontal_gap
            y -= 5 * button_vertical_gap
        y += button_vertical_gap


    # creates the exit button to exit the question box
    exit_size = box_width * 0.07
    exit_x = box_x + box_width//2 - exit_size
    exit_y = box_y - box_height//2
    exit = Button(exit_x, exit_y, exit_size, exit_size, image='exit', name='exit', left_align=True)
    all_sprites.add(exit)
    buttons.add(exit)

    # draws everything to the screen
    all_sprites.draw(screen)
    pygame.display.update()

    # gets the answer clicked on
    answer = False
    while not answer:
       answer = get_button_click(buttons)
    return answer

'''
Draws a box which gives the user the ability to increase/decrease parameters with arrows
Inputs:
params: dictionary with the prompt as a key and the value as the value, e.g: {'sides': 2}
param_min_max: dictionary with the prompt as a key and the minimum and maximum values in a list as the value, e.g {'sides': [1, 4]}
'''
def draw_arrow_box(params, param_min_max):
    # copies the original parameters so that if the user wants to just exit without changing anything, the values return to the originals
    original_params = copy.deepcopy(params)

    # parameters of the question box
    box_width = screen_width*0.45
    box_height = screen_height*0.75
    box_colour = [50, 50, 50]
    box_x = screen_width//2
    box_y = screen_height//2

    # creates the question box
    box = RectangleSprite(box_width, box_height, box_x, box_y, box_colour, left_align=False)

    background_sprites = pygame.sprite.Group()
    background_sprites.add(box)

    # creates the exit button to exit the question box
    exit_size = box_width * 0.07
    exit_x = box_x + box_width//2 - exit_size
    exit_y = box_y - box_height//2
    exit = Button(exit_x, exit_y, exit_size, exit_size, image='exit', name='exit', left_align=True)

    # function to draw the box to the screen
    def draw_screen():
        # sprite groups to draw things to the screen
        background_sprites.draw(screen)
        buttons = pygame.sprite.Group()

        # sets up the parameters for displaying the values on the screen
        vertical_gap = box_height//(len(params) + 1)
        arrow_width = screen_width*0.02
        arrow_height = screen_height*0.05
        text_arrow_gap = arrow_width//2
        text_size = 40
        y = box_y - box_height//2 + vertical_gap//2

        # loops through each of the parameters being changed and draws them along with their arrows to the screen
        for param in params.keys():
            # adds the text to the screen
            text = param + ':'
            text_width, text_height = print_screen(text, box_x, y, text_size, text_colour, left_align=False)
            y += vertical_gap//2
            text =  str(params[param]) + ' '
            text_width, text_height = print_screen(text, box_x, y, text_size * 2, text_colour, left_align=False)
            # creates the arrow buttons
            arrow_x = box_x + text_width//2 + text_arrow_gap
            new_up_arrow = Button(arrow_x, y - arrow_height//2, arrow_width, arrow_height, image='up_arrow', name=param + 'u')
            new_down_arrow = Button(arrow_x, y + arrow_height//2, arrow_width, arrow_height, image='down_arrow', name=param + 'd')
            y += vertical_gap//2

            # adds the buttons to the sprite groups
            buttons.add(new_up_arrow, new_down_arrow)

        # adds the enter and exit buttons so that the user can exit once they have entered what they want
        enter = Button(box_x, y, text='ENTER')
        buttons.add(enter)
        buttons.add(exit)

        # updates the screen
        buttons.draw(screen)
        pygame.display.flip()
        return buttons


    # allows the user to enter their values for each of the parameters
    quit = False
    exited = False
    finished = False
    while not finished:
        buttons = draw_screen()
        button_clicked = get_button_click(buttons)
        if not button_clicked:
            pass
        elif button_clicked == 'quit':
            finished = True
            quit = True
        elif button_clicked == 'exit':
            finished = True
            exited = True
            params = copy.deepcopy(original_params)
        elif button_clicked == 'ENTER':
            finished = True
        elif button_clicked[-1] == 'u' and button_clicked[:-1] in params:
            param = button_clicked[:-1]
            if param_min_max[param][1] > params[param]:
                params[param] += 1
        elif button_clicked[-1] == 'd' and button_clicked[:-1] in params:
            param = button_clicked[:-1]
            if param_min_max[param][0] < params[param]:
                params[param] -= 1

    return exited, quit
  

# allows the user to change the teams which are playing each other
def get_match_change(sides, team_list, num_sim_matches):
    quit = False
    def draw_box():
        all_sprites.draw(screen)
        pygame.display.flip()

    # code for dragging a match button around
    def drag(button):
        # Ensures that the button is at the end of the group, and is hence drawn last. 
        # This means that it will appear above other buttons it is dragged over.
        all_sprites.remove(button)
        all_sprites.add(button)
        original_mouse_x, original_mouse_y = pygame.mouse.get_pos()
        original_sprite_x = button.rect.x
        original_sprite_y = button.rect.y

        # loop that moves the button with the user's mouse while they hold the button clicked
        click_down = True
        while click_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button.rect.x = original_sprite_x + mouse_x - original_mouse_x
            button.rect.y = original_sprite_y + mouse_y - original_mouse_y

            # if the button is outside the box, keeps it inside
            if button.rect.x < box_x - box_width//2:
                button.rect.x = box_x - box_width//2
            elif button.rect.x > box_x + box_width//2 - button.width:
                button.rect.x = box_x + box_width//2 - button.width
            if button.rect.y < box_y - box_height//2:
                button.rect.y = box_y - box_height//2
            elif button.rect.y > box_y + box_height//2 - button.height:
                button.rect.y = box_y + box_height//2 - button.height
            draw_box()

            # checks if the mouse has been lifted
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    click_down = False

        return mouse_x, mouse_y

    def swap_buttons(button1, button2):
        # swaps the positions of the buttons
        swap_x = button1.rect.x
        swap_y = button1.rect.y
        button1.rect.x = button2.rect.x
        button1.rect.y = button2.rect.y
        button2.rect.x = swap_x
        button2.rect.y = swap_y

        # sets the variables for the sizes of the buttons
        font_size_1 = button1.font_size
        font_size_2 = button2.font_size
        width1 = button1.width
        height1 = button1.height
        width2 = button2.width
        height2 = button2.height
        button1.width = width2
        button1.height = height2
        button2.width = width1
        button2.height = height1

        # changes the sizes of the buttons
        button1.image = pygame.Surface([width2, height2])
        button2.image = pygame.Surface([width1, height1])
        pygame.draw.rect(button1.image, button1.colour, [0, 0, width2, height2])
        pygame.draw.rect(button2.image, button2.colour, [0, 0, width1, height1])

        # creates a surface with the text on it
        font1 = pygame.freetype.SysFont(button1.font, font_size_2, bold=button1.bold, italic=button1.italic)
        font2 = pygame.freetype.SysFont(button2.font, font_size_1, bold=button2.bold, italic=button2.italic)
        print_image1, rect = font1.render(button1.text, button1.font_colour)
        print_image2, rect = font2.render(button2.text, button2.font_colour)

        # sticks this surface to the image such that it is centralized
        text_width, text_height = print_image1.get_size()
        button1.image.blit(print_image1, ((width2 - text_width)//2, (height2 - text_height)//2))
        text_width, text_height = print_image2.get_size()
        button2.image.blit(print_image2, ((width1 - text_width)//2, (height1 - text_height)//2))  

        
        # updates the slot lists with the correct values
        if button1 in button_slots:
            if button2 in button_slots:
                button_slots[button_slots.index(button1)], button_slots[button_slots.index(button2)] = button2, button1
                team_slots[button_slots.index(button1)], team_slots[button_slots.index(button2)] = team_slots[button_slots.index(button2)], team_slots[button_slots.index(button1)]
            else:
                button_slots[button_slots.index(button1)] = button2
                for team in team_list:
                    try:
                        if team.team_number == int(button2.text):
                            team_slots[button_slots.index(button2)] = team
                    except ValueError:
                        pass
        elif button2 in button_slots:
            button_slots[button_slots.index(button2)] = button1
            for team in team_list:
                try:
                    if team.team_number == int(button1.text):
                        team_slots[button_slots.index(button1)] = team
                except ValueError:
                    pass

    # parameters of the question box
    box_width = screen_width*0.45
    box_height = screen_height*0.75
    box_colour = [50, 50, 50]
    box_x = screen_width//2
    box_y = screen_height//2

    # creates the question box
    box = RectangleSprite(box_width, box_height, box_x, box_y, box_colour, left_align=False)
    all_sprites = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    all_sprites.add(box)
    
    # creates the exit button to exit the question box
    exit_size = box_width * 0.07
    exit_x = box_x + box_width//2 - exit_size
    exit_y = box_y - box_height//2
    exit = Button(exit_x, exit_y, exit_size, exit_size, image='exit', name='exit', left_align=True)
    all_sprites.add(exit)
    buttons.add(exit)

    # creates a save button to save the changes made
    save = Button(box_x, box_y + box_height//3, box_width//5, box_height//6, bold=True, text='SAVE')
    all_sprites.add(save)
    buttons.add(save)


    # adds the parameters for the buttons with teams currently playing in matches
    match_spacing = box_width//num_sim_matches
    x = box_x - box_width//2 + match_spacing//2
    match_button_y = box_y - box_height * 0.3
    game_spacing = match_spacing * 0.4
    match_button_size = min(game_spacing * 0.9, (match_button_y - (box_y - box_height//2)) * 1.8)
    team_numbers = []
    # slots hold which teams are in which match positions
    button_slots = []
    team_slots = []
    # adds the buttons for the teams currently playing in matches
    for match in sides:
        team1_button = Button(x - game_spacing//2, match_button_y, match_button_size, match_button_size, text=str(match.teams[0].team_number))
        team2_button = Button(x + game_spacing//2, match_button_y, match_button_size, match_button_size, text=str(match.teams[1].team_number))
        team_numbers.append(match.teams[0].team_number)
        team_numbers.append(match.teams[1].team_number)
        all_sprites.add(team1_button, team2_button)
        buttons.add(team1_button, team2_button)

        # adds the teams and buttons to the slots so that it's easier to update sides at the end
        button_slots.append(team1_button)
        button_slots.append(team2_button)
        team_slots.append(match.teams[0])
        team_slots.append(match.teams[1])
        x += match_spacing

    barrier_space = box_height * 0.04
    barrier_height = barrier_space * 0.8

    # adds the parameters for the buttons for the teams not playing in matches
    num_buttons = len(team_list) - 2 * num_sim_matches
    if num_buttons < 10:
        grid_width = num_buttons
        grid_height = 1
    elif num_buttons % 10 == 0:
        grid_width = 10
        grid_height = num_buttons // 10
    else:
        grid_width = 10
        grid_height = num_buttons//10 + 1

    available_height = save.rect.y - match_button_y - match_button_size//2 - barrier_space

    # figures out width and x spacing of the buttons
    match_button_size_to_space_ratio = match_button_size/((box_width - grid_width * match_button_size)/(grid_width + 1))
    if match_button_size_to_space_ratio < 0:
        match_button_size_to_space_ratio = 1000
    x_button_to_space_ratio = min(9, match_button_size_to_space_ratio)
    available_x_slots = x_button_to_space_ratio * grid_width + grid_width + 1
    x_space_size = box_width/available_x_slots
    button_x_spacing = x_space_size * (x_button_to_space_ratio + 1)
    button_width = x_button_to_space_ratio*x_space_size
    x = box_x - box_width//2 + x_space_size + x_button_to_space_ratio * x_space_size//2

    # figures out the y spacing of the buttons
    x_width_size_to_space_ratio = (grid_height + 2) * x_space_size * x_button_to_space_ratio/(available_height - grid_height * x_space_size * x_button_to_space_ratio)
    if x_width_size_to_space_ratio < 0:
        x_width_size_to_space_ratio = 1000
    y_button_to_space_ratio = min(9, x_width_size_to_space_ratio)
    available_y_slots = y_button_to_space_ratio * grid_height + grid_height + 2
    y_space_size = available_height/available_y_slots
    button_y_spacing = y_space_size * (y_button_to_space_ratio + 1)
    button_height = y_button_to_space_ratio * y_space_size
    y = match_button_y + match_button_size//2 + barrier_space + 2 * y_space_size + y_button_to_space_ratio * y_space_size//2
    teams_done = 0

    # loops through the team list to get the teams which are not currently playing in matches
    for team in team_list:
        if team.team_number not in team_numbers:
            team_button = Button(x, y, button_width, button_height, text=str(team.team_number))
            team_numbers.append(team.team_number)
            all_sprites.add(team_button)
            buttons.add(team_button)

            # shifts the x and y for the next button
            teams_done += 1
            x += button_x_spacing
            if teams_done % 10 == 0:
                x = box_x - box_width//2 + x_space_size + x_button_to_space_ratio * x_space_size//2
                y += button_y_spacing
                if teams_done//10 == grid_height - 1:
                    x += (10 - (num_buttons - teams_done)) * button_x_spacing//2


    barrier_y = match_button_y + match_button_size//2 + barrier_space//2 + y_space_size
    barrier_sprite_left = RectangleSprite(box_width//5, barrier_height, x = box_x - box_width*0.4, y=barrier_y)
    barrier_sprite_right = RectangleSprite(box_width//5, barrier_height, x = box_x + box_width*0.4, y=barrier_y)
    quote_sprite = RectangleSprite(box_width*0.6, barrier_height, x=box_x, y=barrier_y, colour=box_colour, text='"Keep the puck on the ice" - Sasha Webb', font_size=barrier_height)
    all_sprites.add(barrier_sprite_left, barrier_sprite_right, quote_sprite)


    # allows the user to change the teams around until they save their work or exit
    answer = ''
    while not (answer == 'exit' or answer == 'quit' or answer == 'SAVE'):
        draw_box()
        if answer:
            for button1 in buttons:
                if button1.name == answer:
                    # allows user to drag the button around with their mouse
                    original_x, original_y = button1.rect.x, button1.rect.y
                    final_x, final_y = drag(button1)

                    # if the button lands on another button, swaps their places
                    button_swapped = False
                    for button2 in buttons:
                        if button2.is_clicked(final_x, final_y) and button2 != button1:
                            button1.rect.x = original_x
                            button1.rect.y = original_y
                            swap_buttons(button1, button2)
                            button_swapped = True
                            break

                    if not button_swapped:
                        button1.rect.x = original_x
                        button1.rect.y = original_y
                    break

        answer = get_button_click(buttons, down_click=True)

    if answer == 'quit':
        quit = True
    elif answer == 'SAVE':
        # updates the sides with the new matches
        for i in range(len(team_slots)//2):
            sides[i].update(team_slots[2*i], team_slots[2*i + 1])
    return sides, quit
    


# runs the clock in parallel while the rest of the code is running
def clock(timer_running, time_remaining):
    initial_time = time_remaining[0]
    start_time = time.time()
    # steadily decreases the time remaining while the timer is running and the time left is greater than 0.
    while time_remaining[0] > 0 and timer_running[0]:
        current_time = time.time()
        time_remaining[0] = initial_time - (current_time - start_time)


# draws the main screen with the mathces on it.
def draw_screen(prev_matches, matches, next_matches, background_group, button_group):
    # draws background
    screen.fill(background_colour)
    background_group.draw(screen)

    # prints the title
    print_title(text_colour)

    # draws the buttons to the screen
    button_group.draw(screen)

    # prints out the current matches
    print_match_set(prev_matches, screen_height//3)
    print_match_set(matches, screen_height//2)
    print_match_set(next_matches, 2 * screen_height//3)

    # updates the screen
    pygame.display.flip()


def menu():
    num_teams = 10
    num_sides = 3
    text_size = 60

    # values for the dimensions of the various buttons
    arrow_x = screen_width * 0.78
    arrow_width = screen_width*0.02
    arrow_height = screen_height*0.05
    player_width = screen_width//3
    player_height = screen_height * 0.8

    # creates the buttons
    left_hockey_man = Button(0, (screen_height - player_height)//2, player_width, player_height, image='player_left', left_align=True)
    right_hockey_man = Button(screen_width - player_width, (screen_height - player_height)//2, player_width, player_height, image='player_right', left_align=True)
    left_hockey_man.image.set_colorkey(BLACK)
    right_hockey_man.image.set_colorkey(BLACK)
    up_arrow_1 = Button(arrow_x, screen_height*0.4 - arrow_height, arrow_width, arrow_height, image='up_arrow', left_align=True)
    up_arrow_2 = Button(arrow_x, screen_height*0.6 - arrow_height, arrow_width, arrow_height, image='up_arrow', left_align=True)
    down_arrow_1 = Button(arrow_x, screen_height*0.4, arrow_width, arrow_height, image='down_arrow', left_align=True)
    down_arrow_2 = Button(arrow_x, screen_height*0.6, arrow_width, arrow_height, image='down_arrow', left_align=True)
    enter = Button(screen_width//2, screen_height*0.8, text='ENTER')

    # creates a pygame sprite group for the buttons, to enable them to be managed more easily
    button_group = pygame.sprite.Group()
    button_group.add(enter, left_hockey_man, right_hockey_man, up_arrow_1, up_arrow_2, down_arrow_1, down_arrow_2)

    # draws the menu
    def display_menu(num_teams, num_sides, button_group, colour):
        screen.fill(background_colour)
        button_group.draw(screen)
        print_title(colour)
        print_screen('Number of teams: ' + str(num_teams), screen_width//2, screen_height*0.4, text_size, colour, left_align=False)
        texts = {
            1: 'Full Ice',
            2: 'Half Ice',
            3: 'Third Ice',
        }
        text = 'Number of matches: ' + texts.get(num_sides, str(num_sides))
        print_screen(text, screen_width//2, screen_height*0.6, text_size, colour, left_align=False)       
        pygame.display.flip()

    # gets the input number of teams and sides
    def do_input(num_teams=num_teams, num_sides=num_sides):
        menu_complete = False
        quit = False
        for event in pygame.event.get():
            # gets the user's clicks
            if event.type == pygame.MOUSEBUTTONUP:
                # finds the position of the mouse when the user unclicks
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # checks which button was clicked
                if enter.is_clicked(mouse_x, mouse_y):
                    menu_complete = True
                elif up_arrow_1.is_clicked(mouse_x, mouse_y):
                    num_teams += 1
                elif down_arrow_1.is_clicked(mouse_x, mouse_y) and num_teams > num_sides * 2:
                    num_teams -= 1
                elif up_arrow_2.is_clicked(mouse_x, mouse_y) and num_sides < num_teams // 2:
                    num_sides += 1
                elif down_arrow_2.is_clicked(mouse_x, mouse_y) and num_sides > 1:
                    num_sides -= 1

            # checks if the user has clicked on the cross to quit the program
            elif event.type == pygame.QUIT:
                menu_complete = True
                quit = True
        return menu_complete, num_teams, num_sides, quit

    # performs the animation to fade the menu screen into view
    def fade_in(num_teams=num_teams, num_sides=num_sides):
        num_steps = 150
        quit = False
        # loops for a set number of steps 
        for i in range(num_steps):
            # changes the colour of the text progressively from the background colour to the designated text colour
            colour = [background_colour[j] + (text_colour[j] - background_colour[j]) * i//num_steps for j in range(3)]

            # changes how seethrough the buttons are so that they appear to fade in
            for button in button_group:
                button.image.set_alpha(i * 255//num_steps)

            # checks for user input
            menu_complete, num_teams, num_sides, quit = do_input(num_teams, num_sides)
            if menu_complete:
                return menu_complete, num_teams, num_sides, quit

            # draws the result to the screen
            display_menu(num_teams, num_sides, button_group, colour)
        return menu_complete, num_teams, num_sides, quit

    # fades the menu in
    menu_complete, num_teams, num_sides, quit = fade_in()

    # keeps the menu until the user exits
    while not menu_complete and not quit:
        display_menu(num_teams, num_sides, button_group, colour=text_colour)
        menu_complete, num_teams, num_sides, quit = do_input(num_teams, num_sides)

    return num_teams, num_sides, quit

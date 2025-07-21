import pygame
import os
import math
import pygame_textinput

pygame.font.init()


# ----------VARIABLES--------------------------------

WIDTH, HEIGHT = 480, 700

GRAPH_HEIGHT = 480
POINTS_PLOTED = 80  #default value #integer divisors of graph height
RATIO_PIXELS_TO_POINTS = int(GRAPH_HEIGHT//POINTS_PLOTED)
EXTRA_VALUES_TO_PLOT_ON_THE_SIDES = 10

NUMBER_OF_LINES = 32 # default value
SPACE_IN_BETWEEN_GRAPH_LINES = int(GRAPH_HEIGHT//NUMBER_OF_LINES)


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MathQuest_v1.0")


WHITE = (240, 240, 240)
BLACK = (0,0,0)
GRAY = (140,140,140)
RED = (255, 50, 50)
BLUE = (0, 200, 50)

range_inputed = 'Range'
number_of_lines_inputed = '# of lines'

GRAPH_FONT = pygame.font.SysFont('arial', 8)
USER_FONT = pygame.font.SysFont('arial', 30)

BOTTONS_STATES = {'box_for_input_active' : False, 'function_range_button_active' : False, 'number_of_lines_button_active' : False }
BOTTON_COLORS = {'box_for_input_color' : WHITE, 'function_range_button_color' : WHITE, 'number_of_lines_button_color' : WHITE}

input_rect = pygame.Rect(15, GRAPH_HEIGHT + 15, 400, 50)
go_botton =  pygame.Rect(350, GRAPH_HEIGHT + 15,110, 50)
function_range_input_rect = pygame.Rect(15, GRAPH_HEIGHT+80, WIDTH//2 -25, 50)
graph_number_of_lines_input_rect = pygame.Rect(WIDTH//2 +10, GRAPH_HEIGHT+80, WIDTH//2 -30, 50)

FPS = 60
clock = pygame.time.Clock()


ESPACIO_ENTRE_PIXELES_PARA_VALORES = 1
# Generate the x and y values and store them in a list of tuples
x_pixels = [x for x in range(0, WIDTH+1,ESPACIO_ENTRE_PIXELES_PARA_VALORES)]
x_values = [x for x in range(-POINTS_PLOTED - EXTRA_VALUES_TO_PLOT_ON_THE_SIDES, POINTS_PLOTED + EXTRA_VALUES_TO_PLOT_ON_THE_SIDES)]

# Use zip to create the third list with tuples of (x_pixel, x_value)
x_related_values_and_pixels = list(zip(x_pixels, x_values))


# Generate the x and y values and store them in a list of tuples
y_pixels = [x for x in range(0, WIDTH+1,ESPACIO_ENTRE_PIXELES_PARA_VALORES)]
y_values = [x for x in range(-POINTS_PLOTED, POINTS_PLOTED+10)]

# Use zip to create the third list with tuples of (x_pixel, x_value)
y_related_values_and_pixels = list(zip(y_pixels, reversed(y_values)))

# Print the result to see the list of tuples

graph_paired_values = list(zip(x_values, y_values))



#-----------FUNCTIONS----------------------------------

def draw_window():
    global POINTS_PLOTED
    global NUMBER_OF_LINES
    global SPACE_IN_BETWEEN_GRAPH_LINES
    SPACE_IN_BETWEEN_GRAPH_LINES = int(GRAPH_HEIGHT//NUMBER_OF_LINES)
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, GRAY,(0, GRAPH_HEIGHT, WIDTH, HEIGHT-(GRAPH_HEIGHT)))  #COSA GRIS DE ABAJO(MENU)
    for x in range(0, WIDTH + 1, SPACE_IN_BETWEEN_GRAPH_LINES):  # Draw vertical grid lines
        pygame.draw.line(WIN, GRAY, (x, 0), (x, GRAPH_HEIGHT))

    for y in range(0, GRAPH_HEIGHT + 1, SPACE_IN_BETWEEN_GRAPH_LINES):  # Draw horizontal grid lines
        if y == 240:
             pygame.draw.line(WIN, BLACK, (0, y), (WIDTH, y))
        else:
            pygame.draw.line(WIN, GRAY, (0, y), (WIDTH, y))
        if y %(NUMBER_OF_LINES/16) == 0: #numbers in horizontal lines
                line_indication_number = round(POINTS_PLOTED - (y/SPACE_IN_BETWEEN_GRAPH_LINES)*((POINTS_PLOTED*2)/NUMBER_OF_LINES), 2)
                graph_y_numbers = GRAPH_FONT.render(str(line_indication_number), 1, BLACK)
                WIN.blit(graph_y_numbers, (WIDTH//2 + 5, y-3))
    for x in range(0, WIDTH + 1, SPACE_IN_BETWEEN_GRAPH_LINES):  # Draw vertical lines numbers 
        if x %(NUMBER_OF_LINES/16) == 0:
            line_indication_number = round(-POINTS_PLOTED + (x/SPACE_IN_BETWEEN_GRAPH_LINES)*((POINTS_PLOTED*2)/NUMBER_OF_LINES), 2)
            graph_x_numbers = GRAPH_FONT.render(str(line_indication_number), 1, BLACK)
            WIN.blit(graph_x_numbers, (x, GRAPH_HEIGHT//2 + 7))    

    pygame.draw.line(WIN, BLACK, (240, 0), (240, GRAPH_HEIGHT))
    

def get_function():
    function_input = input("What function do you want to draw?")
    return str(function_input)


def f(x, y,  function_inputed):
    try:
        return eval(str(function_inputed), {'x':x, 'y':y})
    except ZeroDivisionError:
        return 'ZeroDivisionError'



def test_all_graphing_points(function_inputed):
    global x_values
    global y_values
    interval_in_between_points_plotted = (POINTS_PLOTED/80)  # == a 2*points_plotted /160, para sacar cada cuanto tiene que plottear un valor 
    final_points_to_be_tested_in_graph = []
    points_to_be_drawn = []

    for i in range(int(((POINTS_PLOTED*2)*1.1 )/ interval_in_between_points_plotted)):
        value = round(float((-POINTS_PLOTED)*1.1) + i * interval_in_between_points_plotted, 5)
        final_points_to_be_tested_in_graph.append(value)

    for x in final_points_to_be_tested_in_graph:
        for y in final_points_to_be_tested_in_graph:
            skip_current_y = False
            z= 0 
            z_value_1 = (f(x-interval_in_between_points_plotted,y-interval_in_between_points_plotted, function_inputed))
            z_value_2 = (f(x-interval_in_between_points_plotted,y, function_inputed)) 
            z_value_3 = (f(x,y-interval_in_between_points_plotted, function_inputed))
            z_value_4 = (f(x,y, function_inputed))
            z_values = [ z_value_2, z_value_2, z_value_3, z_value_4]
            for values in z_values:
                if values == 'ZeroDivisionError':
                   skip_current_y = True
                   break
            
            if skip_current_y:
                continue

            z = math.copysign(1, z_value_1) + math.copysign(1, z_value_2) + math.copysign(1, z_value_3) + math.copysign(1, z_value_4)
           
            if z > -4 and z < 4:
               points_to_be_drawn.append((x, y)) 
            
    return points_to_be_drawn
                

def draw_function(points_to_be_drawn):
    global POINTS_PLOTED
    RATIO_PIXELS_TO_POINTS = (GRAPH_HEIGHT/POINTS_PLOTED)
    # pixels_being_drawn = []   __PARA CHECAR VALORES DE PIXELES DIBUJADOS UNCOMMENT______
    for point in points_to_be_drawn:
        x_point = (point[0])
        y_point = (point[1])
        x_pixel = int(((RATIO_PIXELS_TO_POINTS / 2) * x_point) + (WIDTH / 2))
        y_pixel = int(((-RATIO_PIXELS_TO_POINTS / 2) * y_point) + WIDTH / 2)
        #  pixels_being_drawn.append(f"{x_pixel-1}, {y_pixel}")
        pygame.draw.rect(WIN, RED, (x_pixel-1, y_pixel, 3, 3))
    

def draw_graphics_under_plane (box_input_color = BOTTON_COLORS['box_for_input_color'], function_inputed = 'function_inputed'):  
    global BOTTON_COLORS       
    global input_rect                
    pygame.draw.rect(WIN, GRAY,(0, GRAPH_HEIGHT, WIDTH, GRAPH_HEIGHT)) #FONDO GRIS
    pygame.draw.line(WIN, BLACK, (0, GRAPH_HEIGHT), (WIDTH, GRAPH_HEIGHT)) 

    function_surface = USER_FONT.render(str(function_inputed), 1, BLACK)  # FUNCTION FOR DRAWING INPUT BOX
    input_rect.w = max(100, function_surface.get_width() +10) # primero tomamos lo ancho que debe ser
    pygame.draw.rect(WIN, BOTTON_COLORS['box_for_input_color'], input_rect) #despues dibujamos rectangulo
    WIN.blit(function_surface, (input_rect.x+5, input_rect.y+5)) #y al final el texto
    box_width = input_rect.w


    pygame.draw.rect(WIN, BLUE, go_botton)     #DRAWING "GO" BUTTON
    text_surface_go = USER_FONT.render("Draw f()", 1, BLACK) # render at position stated in arguments
    WIN.blit(text_surface_go, (go_botton.x+5, go_botton.y+5))  # set width of textfield so that text cannot get outside of user's text input
    

    pygame.draw.rect(WIN, BOTTON_COLORS['function_range_button_color'], function_range_input_rect) # BOTON PARA RANGO DE FUNCION
    range_surface = USER_FONT.render(str(range_inputed), 1, BLACK) # render at position stated in arguments
    WIN.blit(range_surface, (function_range_input_rect.x+5, function_range_input_rect.y+5))  # set width of textfield so that text cannot get outside of user's text input
    input_rect.w = max(100, range_surface.get_width()+10)

    pygame.draw.rect(WIN,BOTTON_COLORS['number_of_lines_button_color'], graph_number_of_lines_input_rect)#BOTON PARA LINEAS EN GRAFICA
    lines_surface_text = USER_FONT.render(str(number_of_lines_inputed), 1, BLACK) # render at position stated in arguments
    WIN.blit(lines_surface_text, (graph_number_of_lines_input_rect.x+5, graph_number_of_lines_input_rect.y+5))  # set width of textfield so that text cannot get outside of user's text input
    input_rect.w = max(100, lines_surface_text.get_width()+10)

    return box_width
    

#-------------MAIN--------------------------------------
def main():

    global BOTTONS_STATES
    global BOTTON_COLORS
    global POINTS_PLOTED
    global NUMBER_OF_LINES
    global SPACE_IN_BETWEEN_GRAPH_LINES
    global x_values
    global y_values

    global range_inputed
    global number_of_lines_inputed
    order_to_draw_new_function_given = False
    running = True
    points_to_be_drawn = []
    function_inputed = "Click here to enter function"

    function_is_being_drawed = False
    global input_rect

    while running:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
    
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if  go_botton.collidepoint(event.pos):
                    order_to_draw_new_function_given = True
                    for key in BOTTONS_STATES:
                        BOTTONS_STATES[key] = False
            
                elif input_rect.collidepoint(event.pos):
                    BOTTONS_STATES['box_for_input_active'] = True
                    BOTTONS_STATES['function_range_button_active'] = False
                    BOTTONS_STATES['number_of_lines_button_active'] = False

                elif function_range_input_rect.collidepoint(event.pos):
                    BOTTONS_STATES['function_range_button_active'] = True
                    BOTTONS_STATES['number_of_lines_button_active'] = False
                    BOTTONS_STATES['box_for_input_active'] = False
                
                elif graph_number_of_lines_input_rect.collidepoint(event.pos):
                    BOTTONS_STATES['number_of_lines_button_active'] = True
                    BOTTONS_STATES['box_for_input_active'] = False
                    BOTTONS_STATES['function_range_button_active'] = False
                    
                else:
                    for key in BOTTONS_STATES:
                        BOTTONS_STATES[key] = False
                        
            if keys_pressed[pygame.K_RETURN]:
                order_to_draw_new_function_given = True
                for key in BOTTONS_STATES:
                     BOTTONS_STATES[key] = False

            if event.type == pygame.KEYDOWN and BOTTONS_STATES['function_range_button_active'] :  #BOTON PARA RANGO
                if event.key == pygame.K_BACKSPACE:
                    range_inputed = range_inputed[:-1]
    
                elif event.key != pygame.K_RETURN:
                    range_inputed += event.unicode

            if event.type == pygame.KEYDOWN and BOTTONS_STATES['number_of_lines_button_active']:  #BOTON PARA LINEAS EN GRAFICA
                if event.key == pygame.K_BACKSPACE:
                    number_of_lines_inputed = number_of_lines_inputed[:-1]
                elif event.key != pygame.K_RETURN:
                    number_of_lines_inputed += event.unicode

            if event.type == pygame.KEYDOWN and BOTTONS_STATES['box_for_input_active']:
                if event.key == pygame.K_BACKSPACE: # Check for backspace
                    function_inputed = function_inputed[:-1] # get text input from 0 to -1 i.e. end.
                elif event.key != pygame.K_RETURN:
                    function_inputed += event.unicode       # Unicode standard is used for string formation
            
        if BOTTONS_STATES['box_for_input_active'] :
           BOTTON_COLORS['box_for_input_color'] = RED
        else:
            BOTTON_COLORS['box_for_input_color'] = WHITE 

        if BOTTONS_STATES['function_range_button_active']:
            BOTTON_COLORS['function_range_button_color'] = RED
        else:
            BOTTON_COLORS['function_range_button_color'] = WHITE 
        
        if BOTTONS_STATES['number_of_lines_button_active']:
            BOTTON_COLORS['number_of_lines_button_color'] = RED
        else:
            BOTTON_COLORS['number_of_lines_button_color'] = WHITE 
    
        draw_window()
        if function_is_being_drawed == True:
            draw_function(points_to_be_drawn)

    
        input_rect[2] = (draw_graphics_under_plane(BOTTON_COLORS['box_for_input_color'], function_inputed))
        pygame.display.update()
    
        if order_to_draw_new_function_given:
            if  function_inputed == '':
                function_inputed = 'x'
            if range_inputed == '':
                range_inputed = '80'
            if number_of_lines_inputed == '':
               number_of_lines_inputed = '32'

            POINTS_PLOTED = int(range_inputed)
            NUMBER_OF_LINES = int(number_of_lines_inputed)
            x_values = [x for x in range(-POINTS_PLOTED - EXTRA_VALUES_TO_PLOT_ON_THE_SIDES, POINTS_PLOTED + EXTRA_VALUES_TO_PLOT_ON_THE_SIDES)]
            y_values = [x for x in range(-POINTS_PLOTED, POINTS_PLOTED+10)]

            points_to_be_drawn = test_all_graphing_points(function_inputed)
            order_to_draw_new_function_given = False
            function_is_being_drawed = True
        

        if keys_pressed[pygame.K_r]:
            function_is_being_drawed = False
            function_inputed = ''
            range_inputed = '80'
            number_of_lines_inputed = '32'
    
        
        if not order_to_draw_new_function_given:
            pygame.time.delay(50)
            
        

    

if __name__ == "__main__":
    main()
 
    



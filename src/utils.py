import pygame

def draw_text(text, font, color, surface, x, y):
    """
    Draws text on the given surface.
    """
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def handle_gesture(gesture, options, current_selection):
    """
    Handles gesture input for menu navigation.
    :param gesture: The gesture detected ("click" or "pause").
    :param options: The list of menu options.
    :param current_selection: The current selected option index.
    :return: The updated selected option index and action.
    """
    action = None
    if gesture == "click":
        action = current_selection  # Return the index of the selected menu option
    elif gesture == "pause":
        current_selection = (current_selection + 1) % len(options)  # Cycle through the options
    return current_selection, action

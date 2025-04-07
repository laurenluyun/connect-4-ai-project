class Button():
    def __init__(self, position, text_input, font, base_color, hovering_color):
        self.x_position = position[0]
        self.y_position = position[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rectangle = self.text.get_rect(center=(self.x_position, self.y_position))

    def update_button(self, screen):
        screen.blit(self.text, self.text_rectangle)

    def check_for_button_input(self, position):
        if position[0] in range(self.text_rectangle.left, self.text_rectangle.right) and position[1] in range(self.text_rectangle.top, self.text_rectangle.bottom):
            return True
        return False

    def change_button_color(self, position):
        if position[0] in range(self.text_rectangle.left, self.text_rectangle.right) and position[1] in range(self.text_rectangle.top, self.text_rectangle.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
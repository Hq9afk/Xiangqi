import pygame as p


class Button:
    def __init__(self, x, y, width, height, name, img, on_click_function=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click_function = on_click_function
        self.img = {
            "normal": img[0],
            "hover": img[1],
            "click": img[2],
            "active": img[3],
        }
        self.state = "normal"
        self.is_press = False
        self.name = name  # was 'type'

    def get_state(self, game_start, game_state):
        # Start button: always active unless already clicked
        if self.name == "start":
            return "active" if not game_start else "hidden"
        # Swap: active before game starts, hidden after
        if self.name == "swap":
            return "active" if not game_start else "hidden"
        # Return: hidden before game starts, active after
        if self.name == "return":
            return "active" if game_start else "hidden"
        # Undo/Redo logic
        if self.name == "undo":
            return "active" if game_state.move_log else "normal"
        if self.name == "redo":
            return "active" if getattr(game_state, "pastMoveStorage", []) else "normal"
        return "normal"

    def process(self, screen, game_start, game_state):
        click_position = p.mouse.get_pos()
        self.state = self.get_state(game_start, game_state)

        # Skip drawing and interaction if hidden
        if self.state == "hidden":
            return

        interactive = self.state in ("active", "hover")

        if interactive:
            if self.x <= click_position[0] <= self.x + self.width and self.y <= click_position[1] <= self.y + self.height:
                self.state = "hover"
                if p.mouse.get_pressed()[0]:
                    if not self.is_press:
                        self.state = "click"
                        self.is_press = True
                        if self.on_click_function:
                            self.on_click_function()
                else:
                    self.is_press = False
            else:
                self.is_press = False
        else:
            self.is_press = False

        # Fallback: if image for state does not exist, use 'active'
        img_to_draw = self.img.get(self.state) or self.img.get("active")
        if img_to_draw:
            screen.blit(img_to_draw, (self.x, self.y))

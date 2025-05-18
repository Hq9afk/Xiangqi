import pygame as p


class Button:
    def __init__(self, x, y, width, height, name, img, onClickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        self.img = {
            "normal": img[0],
            "hover": img[1],
            "click": img[2],
            "active": img[3],
        }
        self.state = "normal"
        self.isPress = False
        self.name = name  # was 'type'

    def get_state(self, gameStart, gameState):
        # Start button: always active unless already clicked
        if self.name == "start":
            return "active" if not gameStart else "hidden"
        # Swap: active before game starts, hidden after
        if self.name == "swap":
            return "active" if not gameStart else "hidden"
        # Return: hidden before game starts, active after
        if self.name == "return":
            return "active" if gameStart else "hidden"
        # Undo/Redo logic
        if self.name == "undo":
            return "active" if gameState.moveLog else "normal"
        if self.name == "redo":
            return "active" if getattr(gameState, "pastMoveStorage", []) else "normal"
        return "normal"

    def process(self, screen, gameStart, gameState):
        clickPosition = p.mouse.get_pos()
        self.state = self.get_state(gameStart, gameState)

        # Skip drawing and interaction if hidden
        if self.state == "hidden":
            return

        interactive = self.state in ("active", "hover")

        if interactive:
            if self.x <= clickPosition[0] <= self.x + self.width and self.y <= clickPosition[1] <= self.y + self.height:
                self.state = "hover"
                if p.mouse.get_pressed()[0]:
                    if not self.isPress:
                        self.state = "click"
                        self.isPress = True
                        if self.onClickFunction:
                            self.onClickFunction()
                else:
                    self.isPress = False
            else:
                self.isPress = False
        else:
            self.isPress = False

        # Fallback: if image for state does not exist, use 'active'
        img_to_draw = self.img.get(self.state) or self.img.get("active")
        if img_to_draw:
            screen.blit(img_to_draw, (self.x, self.y))

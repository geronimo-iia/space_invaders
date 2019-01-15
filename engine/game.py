import pygame as pg


class AbstractGame:
    """ This base class define game class behaviour main loop"""
    def __init__(self, screen, fps=60):
        self.fps = fps
        self.screen = screen
        self.clock = pg.time.Clock()
        self.start_game = pg.time.get_ticks()
        self.running = True

    def process_events(self):
        """Process events (keystrokes, mouse clicks, etc)."""
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                # stop main loop and return
                self.running = False
                return
            # propagate event
            self.handle_event(event)

    def handle_event(self, event):
        """Handle event"""
        pass

    def update(self, dt):
        """Update object positions, check for collisions"""
        pass

    def render(self):
        """Draw the current frame."""
        pass

    def on_start(self):
        """
        Called when game start.
        """
        pass

    def on_exit(self):
        """
        Called when game exiting.
        """
        pass

    def main(self):
        """
        Main game loop which run until self.running is false.
        """
        self.on_start()

        while self.running:
            dt = self.clock.tick(self.fps)
            self.process_events()
            if self.running:
                self.update(dt)
            if self.running:
                self.render()
            if self.running:
                # pause if application is hidden or iconified
                while not pg.display.get_active():
                    pg.time.wait(100)
                    pg.event.pump()

        self.on_exit()

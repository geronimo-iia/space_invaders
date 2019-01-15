from .game import *


class Scene:

    def __init__(self, game, screen=None, active: bool=False):
        self._active = active
        self._game = game
        self.screen = screen if screen else game.screen

    def handle_event(self, event):
        """Handle Event"""
        return True

    def update(self, dt) -> bool:
        """
        Update logic.
        :param dt: delta time since last update
        :return: True to propagate 'update' to other Scene, False to stop
        """
        return True

    def render(self):
        """Render scene"""
        return True

    @property
    def activated(self):
        """
        :return: True if scene is activated
        """
        return self._active

    def activate(self):
        """
        Activate scene and call
        """
        if not self._active:
            self._active = True
            self.on_activate()

    def disable(self):
        """
        Disable scene.
        """
        if self._active:
            self._active = False
            self.on_disabled()

    def on_disabled(self):
        """
        Handle disable event.
        """
        pass

    def on_activate(self):
        """
        Handle activation.
        """
        pass


class GameScene(AbstractGame):
    """
    This class define game as a composition of scene.
    Scene will be processed in reversed order (last in first).
    """
    def __init__(self, screen, fps=60):
        AbstractGame.__init__(self, screen, fps)
        self.scenes: [Scene] = []

    def handle_event(self, event):
        """Propagate event to all active scene until one response False."""
        for scene in self.scenes[::-1]:
            if scene.activated:
                if not scene.handle_event(event):
                    break

    def update(self, dt):
        """
        Update all active scene until one response False.
        """
        for scene in self.scenes[::-1]:
            if scene.activated:
                if not scene.update(dt):
                    break

    def render(self):
        """
        Render all active scene until one response False.
        """
        for scene in self.scenes[::-1]:
            if scene.activated:
                if not scene.render():
                    break
        pg.display.flip()

    def enable_only(self, scene: Scene):
        """
        Enable only specified scene
        :param scene:
        :return:
        """
        for s in self.scenes:
            if scene != s:
                s.disable()
        scene.activate()

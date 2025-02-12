from contextlib import contextmanager
from ..math import Matrix44
from .node import NodeType
from .parent import ParentNode
from ..window import Window, Monitor, Keys, KeyEvent
from ..core import get_window
from ..core import initialize as pwp_initialize
from .fsm import FiniteStateMachine

__scene__ = []
__next_scene = None
__drop_scene = None

class Scene(FiniteStateMachine, ParentNode):
    window_attrs: dict = {}

    def __init__(self, window: Window = None, **kwargs):
        ParentNode.__init__(self)
        FiniteStateMachine.__init__(self, **kwargs)
        self._wnd = window if window else get_window()
        if not self._wnd:
            raise RuntimeError("No window context for Scene")
        if not issubclass(self._wnd.__class__, Window):
            raise ValueError("Invalid window context for Scene")
        self._width, self._height = self._wnd.size
        self.projection = Matrix44.identity()
        self.view = Matrix44.identity()

    @contextmanager
    def with_projection(self, matrix: Matrix44):
        tmp = self.projection
        self.projection = matrix
        yield self.projection
        self.projection = tmp

    @contextmanager
    def projection2d(self):
        with self.with_projection(Matrix44.orthogonal_projection(0, self._width, 0, self._height, -1.0, 1.0)):
            yield self.projection

    @contextmanager
    def projection3d(self, fov: float = 45.0, near: float = 0.1, far: float = 1000.0):
        with self.with_projection(Matrix44.perspective_projection(fov, float(self._width) / float(self._height), near, far)):
            yield self.with_view

    @contextmanager
    def with_view(self, matrix: Matrix44):
        tmp = self.view
        self.view = matrix
        yield self.view
        self.view = tmp

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def add_child(self, node: NodeType):
        node.scene = self
        self.children.append(node)

    def enter(self):
        pass

    def reenter(self):
        pass

    def background(self):
        pass

    def exit(self):
        pass

    def event(self, e):
        pass

    def step(self, delta):
        pass

    def draw(self):
        for child in self.children:
            child.draw()

def push_scene(scene: Scene):
    global __next_scene
    if __next_scene is not None:
        raise RuntimeError("Next scene already queued")
    __next_scene = scene

def drop_scene():
    global __scene__, __drop_scene
    if __drop_scene is not None:
        raise RuntimeError("Drop scene already queued")
    __drop_scene = __scene__[-1:]

def main_scene():
    global __scene__, __drop_scene
    __drop_scene = __scene__[1:]

def get_scene():
    if not __scene__:
        raise RuntimeError("No active Scene")
    return __scene__[0]

def main(cls):
    global __scene__, __drop_scene, __next_scene
    if __scene__:
        raise RuntimeError("There can only be one @initial_scene")
    wnd = pwp_initialize(**cls.window_attrs)
    scn = cls()
    __scene__.append(scn)
    scn.enter()
    for dt in wnd.loop():
        if not __scene__:
            wnd.quit()
        for e in wnd.events():
            scn.event(e)
        scn.step(dt)
        scn.draw()
        if __drop_scene:
            if isinstance(__drop_scene, list):
                for _scn in reversed(__drop_scene):
                    _scn.exit()
            elif isinstance(__drop_scene, Scene):
                __drop_scene.exit()
            else:
                raise RuntimeError("Invalid Scene")
            __scene__ = __scene__[:-len(__drop_scene)]
            if __scene__:
                scn = __scene__[-1]
                scn.reenter()
            __drop_scene = None
        if __next_scene:
            if isinstance(__next_scene, Scene):
                if __scene__:
                    __scene__[-1].background()
                __scene__.append(__next_scene)
                scn = __next_scene
                scn.enter()
                __next_scene = None
            else:
                raise RuntimeError("Invalid Scene")
    return cls
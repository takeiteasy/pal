from contextlib import contextmanager
from ..math import Matrix44
from .node import NodeType
from .parent import ParentNode
from ..window import Window, Monitor, Keys, KeyEvent
from ..core import get_window
from ..core import initialize as pwp_initialize
from typing import Optional

__scene__ = None

class Scene(ParentNode):
    def __init__(self, window: Window = None):
        global __scene__
        if not __scene__:
            __scene__ = self
        ParentNode.__init__(self)
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
        yield
        self.projection = tmp

    @contextmanager
    def projection2d(self):
        with self.with_projection(Matrix44.orthogonal_projection(0, self._width, 0, self._height, -1.0, 1.0)):
            yield

    @contextmanager
    def projection3d(self, fov: float = 45.0, near: float = 0.1, far: float = 1000.0):
        with self.with_projection(Matrix44.perspective_projection(fov, float(self._width) / float(self._height), near, far)):
            yield

    @contextmanager
    def with_view(self, matrix: Matrix44):
        tmp = self.view
        self.view = matrix
        yield
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

    def exit(self):
        pass

    def event(self, e):
        pass

    def step(self, delta):
        pass

    def draw(self):
        for child in self.children:
            child.draw()

def get_scene():
    if not __scene__:
        raise RuntimeError("No active Scene")
    return __scene__

def initial_scene(cls,
                  width: Optional[int] = 640,
                  height: Optional[int] = 480,
                  title: Optional[str] = "pwp",
                  frame_limit: Optional[int | str] = None,
                  versions: Optional[tuple[int, int, bool]] = None,
                  monitor: Optional[Monitor] = None,
                  shared: Optional[Window] = None,
                  hints: Optional[dict] = None,
                  escape_key: Optional[Keys] = Keys.ESCAPE):
    global __scene__
    if __scene__:
        raise RuntimeError("There can only be one @initial_scene")
    pwp_initialize(width=width,
                   height=height,
                   title=title,
                   frame_limit=frame_limit,
                   versions=versions,
                   monitor=monitor,
                   shared=shared,
                   hints=hints)
    __scene__ = cls()
    __scene__.enter()
    wnd = get_window()
    for dt in wnd.loop():
        for e in wnd.events():
            if escape_key and isinstance(e, KeyEvent):
                if e.key == escape_key:
                    wnd.quit()
            __scene__.event(e)
        __scene__.step(dt)
        __scene__.draw()
    return cls
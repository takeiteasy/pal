from contextlib import contextmanager
from ..math import Matrix44
from .node import NodeType
from .parent import ParentNode
from quickwindow import Window, get_quick_window

class Scene(ParentNode):
    def __init__(self, window: Window = None):
        super().__init__()
        self._wnd = window if window else get_quick_window()
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
        self.projection = Matrix44.orthogonal_projection(0, self._width, 0, self._height, -1.0, 1.0)
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
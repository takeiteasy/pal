from .window import ManagedWindow, FrameLimiter, Monitor, Window, Keys
from .window.window import init_glfw
from .window import glfw as api
from typing import Optional
from raudio import initialize as raudio_initialize
from raudio import shutdown as raudio_shutdown
from atexit import register
from contextlib import contextmanager

__initialized = False
__window__ = None

def get_window():
    global __window__
    if not __window__:
        raise RuntimeError("Window not initialized")
    return __window__

class QuickWindow(ManagedWindow, FrameLimiter):
    def __init__(self, width: int, height: int, title: str, limit: Optional[int | float] = None, **kwargs):
        ManagedWindow.__init__(self, width, height, title, **kwargs)
        FrameLimiter.__init__(self, limit)

    def loop(self):
        while not self.should_close:
            self.poll_events()
            yield self.limit()
            self.swap_buffers()

def initialize(versions: Optional[tuple[int, int, bool]] = None):
    global __initialized
    if __initialized:
        raise RuntimeError("pal already initialized")
    init_glfw()
    raudio_initialize()
    register(lambda: raudio_shutdown())
    if not versions:
        versions = (3, 3, True), (3, 2, True), (3, 1, False), (3, 0, False)
    else:
        if not isinstance(versions, list):
            versions = [versions]
    for vermaj, vermin, iscore in versions:
        try:
            Window.hint()
            Window.hint(context_version=(vermaj, vermin))
            if iscore:
                Window.hint(forward_compat=True)
                Window.hint(opengl_profile=Window.CORE_PROFILE)
            break
        except (api.PlatformError, api.VersionUnavailableError, ValueError) as e:
            iscore_str = 'CORE' if iscore else ''
            print("%s.%s %s: %s" % (vermaj, vermin, iscore_str, e))
    else:
        raise SystemExit("Proper OpenGL 3.x context not found")
    __initialized = True

@contextmanager
def quick_window(width: Optional[int] = 640,
                 height: Optional[int] = 480,
                 title: Optional[str] = "pal",
                 frame_limit: Optional[int | str] = None,
                 versions: Optional[tuple[int, int, bool]] = None,
                 monitor: Optional[Monitor] = None,
                 shared: Optional[Window] = None,
                 hints: Optional[dict] = None,
                 escape_key: Optional[Keys] = None):
    global __window__
    if __window__ is not None:
        raise RuntimeError("Window already initialized")
    if not __initialized:
        initialize(versions)
    __window__ = QuickWindow(width=width,
                             height=height,
                             title=title,
                             frame_limit=frame_limit,
                             monitor=monitor,
                             shared=shared,
                             hints=hints,
                             callbacks=None,
                             escape_key=escape_key)
    yield __window__

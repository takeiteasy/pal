import pwp
from typing import override

class TestScene(pwp.Scene):
    @override
    def enter(self):
        pass

    @override
    def event(self, e):
        pass

    @override
    def step(self, delta):
        pass

with pwp.quick_window() as wnd:
    scn = TestScene()
    scn.enter()
    for dt in wnd.loop():
        for e in wnd.events():
            pass
        scn.step(dt)
        scn.draw()
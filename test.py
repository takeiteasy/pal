import pwp
from typing import override

class TestScene(pwp.Scene):
    @override
    def enter(self):
        pass

    @override
    def event(self, e):
        print(e)

    @override
    def step(self, delta):
        pass

with pwp.quick_window() as wnd:
    scn = TestScene()
    scn.enter()
    for dt in wnd.loop():
        for e in wnd.events():
            scn.event(e)
        scn.step(dt)
        scn.draw()
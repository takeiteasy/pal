import pwp
from typing import override
from sys import exit

from pwp.graphics.shader.default import default_vertex_shader, default_fragment_shader

class TestScene(pwp.Scene):
    @override
    def enter(self):
        x = pwp.VertexShader(default_vertex_shader)
        print(x)
        print(x.attributes)
        exit(0)
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
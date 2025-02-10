import pwp
from typing import override

@pwp.main
class TestScene(pwp.Scene):
    @override
    def enter(self):
        y = pwp.DefaultShader()
        z = pwp.DefaultShader()
        assert y.id == z.id
        pass

    @override
    def event(self, e):
        print(e)

    @override
    def step(self, delta):
        pass
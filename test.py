import pwp
import numpy as np
from OpenGL import GL
from pwp.math import *

def test_shader():
    from pwp.graphics.shader.glsl import (AttributeBlock, UniformBlock,
                                          ShaderInterface, FragmentShaderOutputBlock,
                                          samplerBuffer, texelFetch, vec2,
                                          vec3, vec4, mat4)
    from pwp.graphics.shader import VertexStage, FragmentStage

    class VsAttrs(AttributeBlock):
        position = vec3()
        texcoord = vec2()

    class VsUniforms(UniformBlock):
        projection = mat4()
        modelview = mat4()

    class VsOut(ShaderInterface):
        gl_Position = vec4()
        out_texcoords = vec2()

    def vertex(attr: VsAttrs, uniforms: VsUniforms) -> VsOut:
        return VsOut(gl_Position=uniforms.projection * uniforms.modelview * vec4(attr.position, 1.0),
                     out_texcoords=attr.texcoord)

    class FsUniforms(UniformBlock):
        in_buffer = samplerBuffer()

    class FsOut(FragmentShaderOutputBlock):
        out_color = vec4()

    def fragment(vs_out: VsOut, uniforms: FsUniforms) -> FsOut:
        return FsOut(out_color=texelFetch(uniforms.in_buffer, int(vs_out.out_texcoords.x * 32.0) + int(vs_out.out_texcoords.y * 32.0) * 32))

    return VertexStage(vertex), FragmentStage(fragment)

@pwp.main
class TestScene(pwp.Scene):
    window_attrs = {'escape_key': pwp.Keys.ESCAPE}

    def enter(self):
        self.program = pwp.Program(list(test_shader()))
        data, indices = pwp.create_cube((5.,5.,5.,), st=True, dtype=np.float32)
        flat_data = data[indices]
        shaped_data = flat_data.view(dtype=[('position', np.float32, 3,),('texcoord', np.float32, 2,),])
        self.vb = pwp.VertexBuffer(shaped_data)
        self.pipeline = pwp.Pipeline(self.program)
        self.mesh = pwp.Mesh(self.pipeline, **self.vb.pointers)
        dtype = np.float32
        data = np.random.random_sample((512,512,4))
        data = data.astype(np.float32)
        self.tb = pwp.TextureBuffer(data)
        #bt = BufferTexture(tb)
        self.bt = self.tb.texture
        self.bt.active_unit = self.program.in_buffer
        self.bt.bind()
        self.delta = None

    def event(self, e):
        print(e)

    def step(self, delta):
        self.delta = delta

    def draw(self):
        aspect = float(self.width) / float(self.height)
        projection = Matrix44.perspective_projection(90., aspect, 1., 100., np.float32)
        model_view = Matrix44.from_translation([0.,0.,-8.], np.float32)
        GL.glClearColor(0.2, 0.2, 0.2, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        rotation = Matrix44.from_y_rotation(math.pi * self.delta, np.float32)
        model_view = model_view * rotation
        self.mesh.render(projection=projection, modelview=model_view)

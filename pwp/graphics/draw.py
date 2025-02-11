from OpenGL import GL
import numpy as np
from .object import DescriptorMixin
from .shader import Program, StaticProgram
from .texture import Texture
from .buffer.vertex_array import VertexArray
from .buffer.buffer_pointer import BufferPointer
from .buffer.buffer import TextureBuffer

class DrawCall(DescriptorMixin):
    def __init__(self,
                 program: Program | StaticProgram,
                 indices=None,
                 primitive=GL.GL_TRIANGLES,
                 **pointers):
        self._pointers = pointers
        self._properties = set([])
        self._program = program
        self.primitive = primitive
        self.indices = indices
        self._vertex_array = VertexArray()
        self._rebuild = True

    def __setattr__(self, name, value):
        if name[0] != '_':
            self._properties.add(name)
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name in self._properties:
            del self._properties[name]
        object.__delattr__(self, name)

    def _build(self):
        # TODO: make this more efficient, don't just clear all pointers
        self._vertex_array.clear()
        # assign our pointers to the vertex array
        for name, pointer in self._pointers.items():
            if not isinstance(pointer, BufferPointer):
                raise ValueError('Must be a buffer pointer')
            attribute = self._program.attributes.get(name)
            if attribute:
                self._vertex_array[attribute.location] = pointer
        self._rebuild = False

    def _set_uniforms(self, **uniforms):
        for name, value in uniforms.items():
            if hasattr(self._program, name):
                if isinstance(value, TextureBuffer):
                    value = value.texture
                if isinstance(value, Texture):
                    unit = getattr(self._program, name)
                    if unit is not None:
                        Texture.active_unit = unit
                        value.bind()
                else:
                    setattr(self._program, name, value)

    def draw(self, **uniforms):
        self._set_uniforms(**uniforms)
        with self._program:
            properties = dict((name, getattr(self, name)) for name in self._properties)
            self._set_uniforms(**properties)
            if self.indices is not None:
                self._vertex_array.render_indices(self.indices, self.primitive)
            else:
                self._vertex_array.render(self.primitive)
            for name in self._properties:
                value = getattr(self, name)
                if isinstance(value, Texture):
                    unit = getattr(self._program, name)
                    if unit is not None:
                        Texture.active_unit = unit
                        value.unbind()


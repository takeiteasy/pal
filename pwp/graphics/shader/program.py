from OpenGL import GL
import numpy as np
from .variables import ProgramVariable, Attribute, Uniform
from ..object import ManagedObject, BindableObject, DescriptorMixin
from ..proxy import Integer32Proxy
from ..proxy import Proxy
from pyglsl import Stage, VertexStage, FragmentStage
from .shader import Shader, VertexShader, FragmentShader, WrappedShader
from typing import Callable, Any

type ShaderSource = Shader | Stage

"""
TODO: https://www.opengl.org/registry/specs/ARB/separate_shader_objects.txt
TODO: https://www.opengl.org/registry/specs/ARB/shading_language_include.txt
TODO: https://www.opengl.org/registry/specs/ARB/sampler_objects.txt
"""

class ProgramProxy(Proxy):
    def __init__(self, property, dtype=None):
        super(ProgramProxy, self).__init__(
            getter=GL.glGetProgramiv, getter_args=[property],
            dtype=dtype, prepend_args=['_handle'],
        )


class VariableStore(DescriptorMixin, dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, name, value):
        self[name] = value

    def __setitem__(self, index, value):
        if not isinstance(value, ProgramVariable):
            raise ValueError('Attempted to set to a non-ProgramVariable, use the ProgramVariable.data setter instead')
        super(VariableStore, self).__setitem__(index, value)


class Program(DescriptorMixin, BindableObject, ManagedObject):
    _create_func = GL.glCreateProgram
    _delete_func = GL.glDeleteProgram
    _bind_func = GL.glUseProgram
    _current_program = Integer32Proxy(GL.GL_CURRENT_PROGRAM, bind=False)

    active_attribute_max_length = ProgramProxy(GL.GL_ACTIVE_ATTRIBUTE_MAX_LENGTH)
    active_attributes = ProgramProxy(GL.GL_ACTIVE_ATTRIBUTES)
    active_uniform_max_length = ProgramProxy(GL.GL_ACTIVE_UNIFORM_MAX_LENGTH)
    active_uniforms = ProgramProxy(GL.GL_ACTIVE_UNIFORMS)
    link_status = ProgramProxy(GL.GL_LINK_STATUS, dtype=np.bool)
    delete_status = ProgramProxy(GL.GL_DELETE_STATUS, dtype=np.bool)

    def __init__(self, shaders: list[ShaderSource]):
        super(Program, self).__init__()
        self._uniforms = {}
        self._attributes = {}
        self._loaded = False
        for i, shader in enumerate(shaders):
            if isinstance(shader, Stage):
                if isinstance(shader, VertexStage):
                    shader = VertexShader(shader)
                elif isinstance(shader, FragmentStage):
                    shader = FragmentShader(shader)
                else:
                    assert False
            elif isinstance(shader, Shader):
                if isinstance(shader, WrappedShader):
                    self._attributes |= shader.attributes
                    self._uniforms |= shader.uniforms
            else:
                raise ValueError("Invalid Shader type")
            self._attach(shader)
            shaders[i] = shader
        self._link()
        for shader in shaders:
            self._detach(shader)
        self._loaded = True

    @property
    def attributes(self):
        return self._attributes

    @property
    def uniforms(self):
        return self._uniforms

    def __getattr__(self, name):
        # only load variables if the program is loaded and the attribute is unknown
        try:
            if self._loaded:
                if not self._uniforms or not self._attributes:
                    self._load_variables()
                stores = [self.__dict__['_uniforms'], self.__dict__['_attributes']]
                for store in stores:
                    if name in store:
                        return store[name].__get__(store, store.__class__)
        except:
            pass
        raise AttributeError

    def __setattr__(self, name, value):
        try:
            if self._loaded:
                if name not in self.__dict__:
                    if not self._uniforms or not self._attributes:
                        self._load_variables()
        except:
            pass
        return super(Program, self).__setattr__(name, value)

    def _attach(self, shader):
        GL.glAttachShader(self._handle, shader.handle)

    def _detach(self, shader):
        GL.glDetachShader(self._handle, shader.handle)

    def _link(self):
        GL.glLinkProgram(self._handle)
        if not self.link_status:
            raise ValueError(self.log)
        # linking sets the program as active
        # ensure we unbind the program
        self.unbind()

    @property
    def valid(self):
        return bool(GL.glValidateProgram(self._handle))

    @property
    def log(self):
        return GL.glGetProgramInfoLog(self._handle)

class StaticProgram:
    version = "330 core"
    vertex_source = None
    vertex_functions = None
    fragment_source = None
    fragment_functions = None
    id = None

    @classmethod
    def __init__(cls):
        if not cls.id:
            p = Program([VertexStage(cls.vertex_source,
                                     version=cls.version,
                                     library=cls.vertex_functions),
                         FragmentStage(cls.fragment_source,
                                       version=cls.version,
                                       library=cls.fragment_functions)])
            cls.attributes = p.attributes
            cls.uniforms = p.uniforms
            cls.id = p.handle
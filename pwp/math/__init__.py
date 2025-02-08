# -*- coding: utf-8 -*-

from .euler import *
from .integer import *
from .trig import *
from .matrix33 import *
from .matrix44 import *
from .vector2 import *
from .vector3 import *
from .vector4 import *


# because of circular imports, we cannot put these inside each module
# so insert them here
setattr(matrix33, 'Matrix33', Matrix33)
setattr(matrix44, 'Matrix44', Matrix44)
setattr(quaternion, 'Quaternion', Quaternion)
setattr(vector2, 'Vector2', Vector2)
setattr(vector3, 'Vector3', Vector3)
setattr(vector4, 'Vector4', Vector4)


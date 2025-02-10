# Play With Python

> [!WARNING]
> Work in progess, working title

```python
import pwp

@pwp.main
class TestScene(pwp.Scene):
    def enter(self):
        pass

    def event(self, e):
        print(e)

    def step(self, delta):
        pass
```

## Acknowledgements

Some parts of this code are forked from the projects listed below, big thanks to the authors!

### [pyrr](https://github.com/adamlwgriffiths/Pyrr/) + [OMGL](https://github.com/adamlwgriffiths/OMGL) [BSD 2-clause license]

### [shaderdef](https://github.com/nicholasbishop/shaderdef/) [GPL-3.0 license]

### [pyglfw](https://github.com/pyglfw/pyglfw/) [Zlib license]

### [raudio](https://github.com/raysan5/raudio) [Zlib license]

## Requirements 
```
multipledispatch==1.0.0
numpy==2.2.2
pillow==11.1.0
PyOpenGL==3.1.9
six==1.17.0
transitions==0.9.2
attrs==25.1.0
pyaudiolib==0.0.1
```

## LICENSE
```
Play With Python

Copyright (C) 2025 George Watson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

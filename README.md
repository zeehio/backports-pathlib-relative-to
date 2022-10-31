# backports-pathlib-relative-to

Backports the `relative_to` method with its `walk_up`
argument from python 3.12 back to 3.7.

## Installation

```
python -m pip install backports-pathlib-relative-to
```

## Usage

```python
from backports.pathlib import pathlib

p = pathlib.Path("/a")
p.relative_to("/c", walk_up=True)
```

import pathlib
from pathlib import Path
from pathlib import PurePosixPath
from pathlib import PureWindowsPath

def _relative_to(self, *other, walk_up=False):
    """Return the relative path to another path identified by the passed
    arguments.  If the operation is not possible (because this is not
    related to the other path), raise ValueError.
    The *walk_up* parameter controls whether `..` may be used to resolve
    the path.
    """
    # For the purpose of this method, drive and root are considered
    # separate parts, i.e.:
    #   Path('c:/').relative_to('c:')  gives Path('/')
    #   Path('c:/').relative_to('/')   raise ValueError
    if not other:
        raise TypeError("need at least one argument")
    parts = self._parts
    drv = self._drv
    root = self._root
    if root:
        abs_parts = [drv, root] + parts[1:]
    else:
        abs_parts = parts
    other_drv, other_root, other_parts = self._parse_args(other)
    if other_root:
        other_abs_parts = [other_drv, other_root] + other_parts[1:]
    else:
        other_abs_parts = other_parts
    num_parts = len(other_abs_parts)
    casefold = self._flavour.casefold_parts
    num_common_parts = 0
    for part, other_part in zip(casefold(abs_parts), casefold(other_abs_parts)):
        if part != other_part:
            break
        num_common_parts += 1
    if walk_up:
        failure = root != other_root
        if drv or other_drv:
            failure = casefold([drv]) != casefold([other_drv]) or (failure and num_parts > 1)
        error_message = "{!r} is not on the same drive as {!r}"
        up_parts = (num_parts-num_common_parts)*['..']
    else:
        failure = (root or drv) if num_parts == 0 else num_common_parts != num_parts
        error_message = "{!r} is not in the subpath of {!r}"
        up_parts = []
    error_message += " OR one path is relative and the other is absolute."
    if failure:
        formatted = self._format_parsed_parts(other_drv, other_root, other_parts)
        raise ValueError(error_message.format(str(self), str(formatted)))
    path_parts = up_parts + abs_parts[num_common_parts:]
    new_root = root if num_common_parts == 1 else ''
    return self._from_parsed_parts('', new_root, path_parts)


pathlib.PurePosixPath.relative_to = _relative_to
pathlib.PureWindowsPath.relative_to = _relative_to


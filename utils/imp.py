import types
import typing
from importlib import import_module
from pkgutil import walk_packages


def import_recursive(pkg: typing.Type[types.ModuleType]) -> typing.Sequence[typing.Type[types.ModuleType]]:
    """
    递归导入指定包下所有模块

    :param pkg:
    :return:
    """
    modules = []
    for finder, name, is_pkg in walk_packages(pkg.__path__):
        mod = import_module('.'.join((pkg.__name__, name)))
        modules.append(mod)
        if is_pkg:
            import_recursive(mod)
    return modules
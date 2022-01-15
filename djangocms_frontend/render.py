import importlib
from .settings import framework, theme


render_path = f"{theme}.renderer"


class _Empty:
    pass


def render_factory(name):
    mod = importlib.import_module(render_path)
    if hasattr(mod, framework):
        mod = getattr(mod, framework)
        cls = f"Render{name}"
        if hasattr(mod, cls):
            return getattr(mod, cls)
    return _Empty



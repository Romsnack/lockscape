"""Load bin/lockscape as a module (it has no .py suffix) so tools can run scenes headlessly."""
import importlib.machinery
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load():
    loader = importlib.machinery.SourceFileLoader("lockscape", str(ROOT / "bin/lockscape"))
    spec = importlib.util.spec_from_loader("lockscape", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod

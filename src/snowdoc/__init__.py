import warnings
warnings.filterwarnings("ignore", message=".*is not a Python type.*Pydantic will allow any object with no validation.*")
from importlib.metadata import version as _v
__all__ = ["__version__"]
__version__ = _v("snowdoc")

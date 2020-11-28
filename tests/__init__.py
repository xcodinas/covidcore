try:
    from deletos_api.tests.test_api import suite
except ImportError:
    from .test_api import suite

__all__ = ['suite']

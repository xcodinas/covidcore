try:
    from covidcore.tests.test_covidcore import suite
except ImportError:
    from .test_covidcore import suite

__all__ = ['suite']

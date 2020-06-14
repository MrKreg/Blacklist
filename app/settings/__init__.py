import sys

try:
    from app.settings.local import *
except ImportError:
    from app.settings.common import *

if 'test' in sys.argv:
    from app.settings.tests import *

from clldutils.path import Path
from clld.tests.util import TestWithApp

import cdk


class Tests(TestWithApp):
    __cfg__ = Path(cdk.__file__).parent.joinpath('..', 'development.ini').resolve()
    __setup_db__ = False

    def est_home(self):
        res = self.app.get('/', status=200)

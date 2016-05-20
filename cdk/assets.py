from clld.web.assets import environment
from clldutils.path import Path

import cdk


environment.append_path(
    Path(cdk.__file__).parent.joinpath('static').as_posix(), url='/cdk:static/')
environment.load_path = list(reversed(environment.load_path))

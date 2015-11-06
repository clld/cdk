from clld.web.assets import environment
from path import path

import cdk


environment.append_path(
    path(cdk.__file__).dirname().joinpath('static'), url='/cdk:static/')
environment.load_path = list(reversed(environment.load_path))

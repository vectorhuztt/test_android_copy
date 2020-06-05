import json
import os

import yaml

curpath = os.path.abspath(os.path.dirname(__file__))
yaml_path = curpath.split('app\\')[0] + 'conf\\user_info.yaml'
info = json.dumps(yaml.load(open(yaml_path, 'r').read()))
print(json.loads(info)['userinfo']['AnyPhone'])
import os
import pathlib
import re

path = pathlib.Path('test/main')
for stage in os.listdir(path):
    if not re.fullmatch(r's\d', stage):
        continue
    for test in os.listdir(path / stage):
        if test.startswith('__'): continue
        with open(path / stage / test, encoding='utf-8') as test_file:
            code = test_file.read()
        for method in re.findall(r'def test_[^(]+', code):
            print(f'{test}/{method[4:]}')
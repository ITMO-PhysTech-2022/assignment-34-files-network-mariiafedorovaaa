import pytest

import inspect
import json
import sys
from decorator import decorator

from tasks.core.command import BasicCommand
from tasks.core.globals import main, pool, data

from test.common.test import create, timeout, root_directory
from test.common.mock.fs import tmpcd, tmpreplace
from test.main.process import spawn
from test.main.base import config, cleanup, show_transform


class TestConfig:
    @pytest.mark.parametrize('prefix', ['$', '@', ':('])
    def test_prefix(self, prefix):
        process = spawn(auto_exit=False)
        with tmpcd(root_directory()), tmpreplace('tasks/config.json') as config_file:
            config_file.write(json.dumps(config(False, -1, prefix), indent=2))
            with process:
                spec_run = timeout(process.handler, 5)
                spec_run.__name__ = 'run.exit'
                runner = create(spec_run, '1.1#config.prefix')
                runner.run(runner.manual('exit', 1).returns([f'{prefix} ']))

            cleanup(runner, process)

    @pytest.mark.parametrize('margin', [0, 3, 10])
    @pytest.mark.parametrize('show', [
        lambda x, y: x + y,
        lambda x, y: f"{x}:{y}"
    ])
    def test_display(self, show, margin):
        process = spawn()
        show_src = inspect.getsource(show).strip().removesuffix(',')

        with tmpcd(root_directory()), tmpreplace('tasks/config.json') as config_file:
            config_file.write(json.dumps(config(True, margin, '$'), indent=2))
            with process:
                spec_run = timeout(process.handler, 5)
                spec_run.__name__ = 'run.cursor.show'
                runner = create(spec_run, '1.1#config.display')
                runner.multitest(
                    runner.manual(f'exec main.commands["show"] = {show_transform(show_src)}', 1).just_returns(),
                    runner.manual('exec data.lines = [""] * 100', 1).just_returns(),

                    runner.manual('exec data.cursor = (0, 0)', 1).just_returns(),
                    runner.manual('home', 1).returns([f'$  > {show(0, margin)}\n']),
                    runner.manual('exec data.cursor = (50, 0)', 1).just_returns(),
                    runner.manual('home', 1).returns([f'$  > {show(50 - margin, 50 + margin)}\n']),
                    runner.manual('exec data.cursor = (97, 0)', 1).just_returns(),
                    runner.manual('home', 1).returns([f'$  > {show(97 - margin, min(97 + margin, 99))}\n']),
                )

            cleanup(runner, process)

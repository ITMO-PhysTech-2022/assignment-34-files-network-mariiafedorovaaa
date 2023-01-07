from __future__ import annotations
from decorator import decorator

from tasks.core import data, main


@decorator
def requires_data(cmd, *args):
    if not data:
        main.report('No data currently in use')
        return
    return cmd(*args)


def greedy(cmd):
    cmd.__greedy__ = True
    return cmd
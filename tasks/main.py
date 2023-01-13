import inspect

from tasks.core import main, pool
from tasks.driver import COMMANDS

# --------------- Задание 1.1 --------------- #

l = []
with open("config.json", encoding="utf-8") as utu:
    l = json.loads(utu.read())
utu.close()
DISPLAY = l.get('display').get('show')
DISPLAY_MARGIN = l.get('display').get('margin')
PREFIX = l.get('prefix')


if __name__ == '__main__':
    main.configure(
        display=DISPLAY,
        display_margin=DISPLAY_MARGIN,
        base_prefix=PREFIX,
        commands=COMMANDS
    )
    while True:
        main.execute(pool.next())

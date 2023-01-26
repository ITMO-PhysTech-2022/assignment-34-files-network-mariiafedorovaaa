def _cmd_macro(name: str):
    script = []
    with pool.scope():
        while True:
            command = pool.next()
            if command == 'stop':
                break
            script.append(command)
    main.macros[name] = script


def _cmd_repeat(macro: str, times: int):
    if macro not in main.macros:
        return main.report(f'Нет макро с именем {macro}')

    for _ in range(times):
        pool.put(main.macros[macro])


def _cmd_execute(filename: str):
    if not os.path.exists(filename):
        return main.report(f'Файл {filename} не существует')
    t = open(filename).readlines()
    for i in range(len(t)):
        t[i].lstrip()
        t[i].removesuffix('\n')


# --------------- Задание 2.* --------------- #

def _cmd_use(*names: str):
    with pool.scope(), main.use_vars(names):
        while True:
            command = pool.next()
            if command == 'stop':
                break
            main.execute(command)


def _cmd_set_int(name: str, value: int):
    main.vars[name] = value


def _cmd_set_str(name: str, value: str):
    main.vars[name] = value


def _cmd_set_cmd(name: str):
    with pool.scope():
        command = pool.next()
        main.vars[name] = main.execute(command, silent=True)


def _cmd_set_eval(name: str):
    with pool.scope():
        command = pool.next()
        main.vars[name] = eval(command.format_map(main.var_formatter))


def _cmd_get(name: str):
    if name not in main.vars:
        return main.report(f'Нет переменной с именем {name}')
    return main.vars[name]


def _cmd_if_eval():
    with pool.scope():
        expression, command = pool.next(), pool.next()
        value = eval(expression.format_map(main.var_formatter))
        if value:
            main.execute(command)
#!/usr/bin/env python3
"""CLI entrypoint for all python modules.
"""

from argparse import ArgumentParser, Action
import asyncio

from inspect import get_annotations, iscoroutinefunction, signature
from importlib import import_module
import logging
import pkgutil

import src

logger = logging.getLogger(__package__)
logging.basicConfig(level=logging.ERROR)


def get_parser() -> ArgumentParser:
    src_parser = ArgumentParser(description=src.__doc__)
    src_parser.set_defaults(cli_entrypoint=lambda: src_parser.print_help)

    class RootLogLevelAction(Action):
        def __call__(self, parser, namespace, values, option_string=None) -> None:
            logger.setLevel(logging.getLevelNamesMapping()[values])

    src_parser.add_argument(
        '--log-level',
        action=RootLogLevelAction,
        choices=logging.getLevelNamesMapping().keys(),
        default='ERROR',
    )

    stack = [(src, src_parser)]

    while stack:
        module, parser = stack.pop()
        parser.set_defaults(**{module.__package__.replace('.', '_'): True})

        if hasattr(module, 'cli_entrypoint'):
            parser.set_defaults(cli_entrypoint=module.cli_entrypoint)

            for flag, annotation in get_annotations(module.cli_entrypoint).items():
                if flag == 'return':
                    continue
                parameter = signature(module.cli_entrypoint).parameters[flag]
                flag = flag.replace('_', '-')
                parser.add_argument(
                    f'--{flag}' if parameter.kind == parameter.KEYWORD_ONLY else flag,
                    default=parameter.default,
                    help=f'default: {parameter.default}'
                    if parameter.default is not parameter.empty else None,
                    type=annotation)

        if hasattr(module, 'logger'):
            _module = module

            class LogLevelAction(Action):
                def __call__(self, parser, namespace, values, option_string=None) -> None:
                    _module.logger.setLevel(logging.getLevelNamesMapping()[values])

            parser.add_argument(
                '--log-level',
                action=LogLevelAction,
                choices=logging.getLevelNamesMapping().keys(),
                default='ERROR',
            )

        if module.__name__ == module.__package__:
            # This is a package.
            subparsers = parser.add_subparsers()
            for _, name, _ in pkgutil.iter_modules(path=module.__path__):
                submodule = import_module(f'{module.__package__}.{name}')
                subparser = subparsers.add_parser(name=name, description=submodule.__doc__)
                subparser.set_defaults(cli_entrypoint=lambda: subparser.print_help)
                stack.append((submodule, subparser))

    return src_parser


def main() -> None:
    args = vars(get_parser().parse_args())
    cli_entrypoint = args['cli_entrypoint']
    ks = signature(cli_entrypoint).parameters.keys()
    if iscoroutinefunction(cli_entrypoint):
        asyncio.run(cli_entrypoint(**{k: args[k] for k in ks}))
    else:
        cli_entrypoint(**{k: args[k] for k in ks})


if __name__ == '__main__':
    main()

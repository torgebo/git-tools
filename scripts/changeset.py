#!/usr/bin/env python3
'''Compute list of files that have changed in a Git repo.

By default it will compute all files in `index` that have changed
since branching out from master.

The full file list consists of:
- indexed files changed from main branch
- unstaged files changed from main branch

Additionally we should be able to filter on whether files are
staged or not.
'''
from functools import wraps
from typing import Callable, Generator, List, Optional
import argparse
import logging
import logging.handlers
import re
import subprocess
import sys


log = logging.getLogger(__name__)


def _log_call(f: Callable) -> Callable:
    @wraps(f)
    def _run_call(*args, **kwargs):
        name: Optional[str] = None
        if hasattr(f, "__name__"):
            name = getattr(f, "__name__")
        elif hasattr(f, "__class__"):
            o = getattr(f, "__class__")
            name = getattr(o, "__name__", None)
        log.warning(
            "executing function `%s` with params %s and %s",
            name, args, kwargs
        )
        return f(*args, **kwargs)

    return _run_call


@_log_call
def changeset(commit1: str, commit2: Optional[str]) -> str:
    commits = [commit1]
    if commit2:
        commits.append(commit2)
    try:
        proc: subprocess.CompletedProcess = subprocess.run(
            ['git', 'diff', '--name-only', *commits],
            capture_output=True,
            encoding='utf-8',
            check=True,
            shell=False,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr, file=sys.stderr)
        raise e

    out = proc.stdout
    return out.strip()


@_log_call
def common_ancestor(commit1: str, commit2: str) -> str:
    try:
        proc: subprocess.CompletedProcess = subprocess.run(
            ['git', 'merge-base', commit1, commit2],
            encoding='utf-8',
            capture_output=True,
            check=True,
            shell=False,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr, file=sys.stderr)
        raise e

    out = proc.stdout
    return out.strip()


@_log_call
def _parse_filelist(filelines: str) -> List[str]:
    if not filelines:
        return []
    names: List[str] = filelines.split('\n')
    return names


@_log_call
def _parse_xargs(filelist: List[str]) -> str:
    return ' '.join(filelist)


@_log_call
def _arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Process some integers.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--main-commit', default='master',
        help='First commit reference.')
    parser.add_argument(
        '--compare-commit', default='HEAD',
        help='Second commit reference.')
    args = parser.parse_args()
    return args


@_log_call
def _filter_names(filelist: List[str], regexp=None) -> Generator[str, None, None]:
    for name in filelist:
        if not regexp:
            yield name


def main(
        main_commit: str,
        compare_commit: str,
        inc_indexed=True,
        regexp=None,
) -> str:
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.handlers.SysLogHandler(),
            logging.StreamHandler(sys.stderr)
        ],
    )
    branch_base = common_ancestor(main_commit, compare_commit)
    #import pdb; pdb.set_trace()
    filelines = changeset(branch_base, compare_commit)
    file_list = _parse_filelist(filelines)
    file_list = list(_filter_names(file_list))
    xargs_list = _parse_xargs(file_list)
    print(xargs_list, file=sys.stdout)
    return xargs_list


if __name__ == '__main__':
    args = _arg_parser()
    print("args:", args.main_commit, args.compare_commit)
    main(args.main_commit, args.compare_commit)


__all__ = [
    "changeset",
    "main",
]

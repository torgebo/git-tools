#!/usr/bin/env python3
from __future__ import annotations
import re
import readline
import string
import subprocess


class BranchFmt:

    @classmethod
    def from_str(cls, branch_name: str) -> BranchFmt:
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class NameDescNum(BranchFmt):
    name: str
    desc: str
    num: int

    fmt: str = "{name:s}/{desc:s}/{num:d}"

    def __init__(self, name: str, desc: str, num: int):
        self.name = name
        self.desc = desc
        self.num = num

    @property
    def allowed_chars(self):
        return string.ascii_letters + string.digits + "-_"

    @staticmethod
    def validate_alpha(str_segm: str):
        _string_segments = set()
        s = set(str_segm)
        allowed = self.allowed_chars
        if not s.issubset(set(allowed)):
            raise ValueError(
                str_segm + " contains illegal characters, must be one of" +
                allowed)

    @classmethod
    def from_str(cls, branch_name) -> NameDescNum:
        segments = branch_name.split("/")
        if len(segments) != 3:
            raise ValueError
        name = segments[0]
        desc = segments[1]
        self.validate_alpha(name)
        self.validate_alpha(desc)
        num = int(segments[2])
        return cls(name, desc, num)

    def __str__(self) -> str:
        return self.fmt.format(name=self.name, desc=self.desc, num=self.num)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.desc}, {self.num})"


def get_current_branch():
    """Get the current branch name."""
    completed_process = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        check=True,
        capture_output=True,
    )
    branch_name = str(completed_process.stdout, encoding="utf-8").strip()
    return branch_name


def prompt():
    happy = False
    while not happy:
        branch_name = input("please enter branch name : ")
        response_happy: str = 'o'
        cur_branch = get_current_branch()
        while response_happy not in ('y', 'n'):
            response_happy = input((
                "\nAre you sure you want to create\n"
                "new branch '{branch_name:s}'\n"
                "checked out from '{cur_branch:s}'? y/n ").format(
                    branch_name=branch_name,
                    cur_branch=cur_branch,
                ))
        happy = (response_happy.lower() == 'y')

    print(("\nChecking out new branch '{branch_name:s}'"
           "from '{cur_branch:s}'").format(
               branch_name=branch_name,
               cur_branch=cur_branch,
           ))


if __name__ == "__main__":
    prompt()

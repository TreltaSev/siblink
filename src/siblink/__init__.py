from siblink.Config import Config
from pyucc import colors, console, symbols
from typing import List

__git__ = "git+https://github.com/TreltaSev/siblink.git"


@console.register("info")
def info(*values, **optional):
  # [info]
  buff: List[str] = []
  buff.append(f"{colors.white}[{colors.vibrant_blue}info{colors.white}]{symbols.reset}")
  # [info] {*values}
  buff.extend(values)
  console.cprint(*buff)


@console.register("error")
def error(*values, **optional):
  time: str = optional.get("time")
  console.cprint(f"{colors.chex('#FF3F30', 'background')} ERROR {symbols.reset}{colors.chex('#aaaaaa')} {time}{symbols.reset}{colors.chex('#FF3F30', 'foreground')}", *values)


@console.register("warn")
def warn(*values, **optional):
  time: str = optional.get("time")
  console.cprint(f"{colors.chex('#FF7300', 'background')} WARN {symbols.reset}{colors.chex('#aaaaaa')} {time}{symbols.reset}{colors.chex('#FF7300', 'foreground')}", *values)


@console.register("success")
def success(*values, **optional):
  time: str = optional.get("time")
  console.cprint(f"{colors.chex('#71ff71', 'background')}   OK   {symbols.reset}{colors.chex('#aaaaaa')} {time}{symbols.reset}{colors.chex('#71ff71', 'foreground')}", *values)


@console.register(identifier="start")
def start(*values, **_):
  # [starting]
  buff: List[str] = []
  buff.append(f"{colors.white}[{colors.vibrant_blue}starting{colors.white}]{symbols.reset}")
  # [starting] {*values}
  buff.extend(values)
  console.cprint(*buff)


@console.register(identifier="done")
def done(*values, **_):
  # [done]
  buff: List[str] = []
  buff.append(f"{colors.white}[{colors.vibrant_green}done{colors.white}]{symbols.reset}")
  # [done] {*values}
  buff.extend(values)
  console.cprint(*buff)


@console.register(identifier="fail")
def fail(*values, **_):
  # [fail]
  buff: List[str] = []
  buff.append(f"{colors.white}[{colors.vibrant_red}fail{colors.white}]{symbols.reset}")
  # [fail] {*values}
  buff.extend(values)
  console.cprint(*buff)

from siblink.Config import Config
from pyucc import colors, console, symbols


__git__ = "git+https://github.com/TreltaSev/siblink.git"


@console.register("info")
def info(*values, **optional):
  time: str = optional.get("time")
  console.cprint(f"{colors.chex('#305EFF', 'background')}  INFO  {symbols.reset}{colors.chex('#aaaaaa')} {time}{symbols.reset}", *values)


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

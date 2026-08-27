# -*- coding: utf-8 -*-
"""给所有生成器的文件操作套一层有上限的重试。

## 为什么需要它

`build.sh` 开头会 `rm -rf ../rpg && cp -r ../_orig ../rpg`，一次性造出两千多个
文件；紧接着四十来个生成器开始密集读写它们。在这台机器上，Windows 的实时扫描
跟在后面追，被扫到的那一刻文件操作会返回
`OSError: [Errno 22] Invalid argument` —— **每次挂在不同的文件、不同的生成器**，
所以看起来像"某个生成器有 bug"，实际上和生成器无关。

排查记录（免得下次又从头查一遍）：

* 不是路径问题 —— 同一个路径、同样的相对写法，单独跑必定成功；
* 不是权限问题 —— 文件可写，`stat` 正常；
* 不是句柄耗尽 —— 实测连开 3000 个不关闭的写句柄照样全部成功；
* 复制之后停 5 秒能压低概率，但**压不住** —— 连试四次，四次都挂。

所以正解不是"等久一点"，而是"撞上了就重试"。

## 为什么不写进各个生成器

会失败的操作散落在四十来个生成器里（migrate / opt_spawn / add_pact / add_squad /
drop_legacy_mob_factions 都撞过），逐个改既啰嗦又一定会漏。
`sitecustomize` 由 Python 启动时自动导入，一处生效、全线覆盖 ——
代价是它要能被找到，所以 `build.sh` 里导出了 `PYTHONPATH=_tools`。

## 边界：只重试"这一刻不行"的那几种

只有 `EINVAL / EACCES / EBUSY` 会重试 —— 它们的共同点是"过一会儿可能就好了"。
**`ENOENT`（文件不存在）不在其中**，所以"路径写错了"这类真错误仍然当场抛出，
不会被重试掩盖成卡顿。

读也要重试：一开始我只包了写，理由是"读失败是真的读不到"。实测证明这个判断
太窄 —— 扫描窗口同样会让读返回 EINVAL。而真正读不到的文件给的是 ENOENT，
本来就不在重试名单里，所以放开读并不会掩盖任何真问题。

**重试有上限**：六次之后仍然失败就照常抛出去，并把 errno 与路径打到 stderr。
一直重试等于把"磁盘满了"这类真故障伪装成卡顿。
"""

import builtins
import errno
import functools
import io
import os
import sys
import time

# 退避序列（秒）。总共不到 3 秒，够躲过一次扫描窗口，又不至于让真故障拖很久。
_BACKOFF = (0.05, 0.1, 0.2, 0.4, 0.8, 1.2)

# 只有这些才值得重试。ENOENT / ENOSPC 之类重试多少次都是同一个结果。
_TRANSIENT = frozenset((errno.EINVAL, errno.EACCES, errno.EBUSY))

_io_open = io.open
_builtin_open = builtins.open


def _open(real, file, *a, **kw):
    """带重试的 open。

    它是被 `functools.partial` 包起来交出去的，**不能**直接换成普通函数：
    `pathlib` 把 `io.open` 存成类属性，而内置函数不实现描述符协议、不会被绑定；
    普通 Python 函数会，于是 `self._accessor.open(self, mode, ...)` 的参数会
    整体错位一位，`mode` 收到一个 WindowsPath。partial 对象不是描述符，安全。
    """
    last = None
    for i, wait in enumerate((0,) + _BACKOFF):
        if wait:
            time.sleep(wait)
        try:
            fh = real(file, *a, **kw)
            if i:
                sys.stderr.write("[io-retry] 第 %d 次重试后成功：%s\n" % (i, file))
            return fh
        except OSError as e:
            if e.errno not in _TRANSIENT:
                raise
            last = e
    sys.stderr.write("[io-retry] 放弃：errno=%s path=%s\n"
                     % (last.errno if last else "?", file))
    raise last


io.open = functools.partial(_open, _io_open)
builtins.open = functools.partial(_open, _builtin_open)

# ---------------------------------------------------------------------------
# 目录遍历：既要重试，更要**不许静默**
# ---------------------------------------------------------------------------
# `os.walk` 默认 `onerror=None`，意思是**遇到 OSError 就当那个目录不存在**，
# 一声不吭地少列几个文件。这个包里有 22 处 os.walk，没有一处传 onerror。
#
# 于是扫描干扰会变成这样一条链：walk 少列出几个文件 -> 某个生成器少处理几个
# 函数 -> opt_guard 少插几道守卫 -> opt_runtime_hotpaths 找不到本该被拆出来的
# deep_seek/g0 -> 构建失败。而且**每次少的不是同一批**，所以看起来像
# "构建不确定"。实测守卫数会在 25/162/13 与 31/214/19 之间跳。
#
# 这里做两件事：listdir/scandir 走同一套重试；walk 的 onerror 默认改成抛出。
# 宁可当场炸，也不要悄悄少做一半工作 —— 后者会一路伪装成别的问题。
_listdir, _scandir, _walk = os.listdir, os.scandir, os.walk


def _retry_call(fn, *a, **kw):
    last = None
    for wait in (0,) + _BACKOFF:
        if wait:
            time.sleep(wait)
        try:
            return fn(*a, **kw)
        except OSError as e:
            if e.errno not in _TRANSIENT:
                raise
            last = e
    raise last


def _walk_loud(top, topdown=True, onerror=None, followlinks=False):
    if onerror is None:
        def onerror(e):
            raise e
    return _walk(top, topdown, onerror, followlinks)


os.listdir = functools.partial(_retry_call, _listdir)
os.scandir = functools.partial(_retry_call, _scandir)
os.walk = _walk_loud

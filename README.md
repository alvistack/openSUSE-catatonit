## catatonit ##

[![Build Status](https://github.com/openSUSE/catatonit/actions/workflows/ci.yml/badge.svg)](https://github.com/openSUSE/catatonit/actions/workflows/ci.yml)

A container init that is so simple it's effectively brain-dead. This is a
rewrite of [initrs][initrs] in C, because we found that it is not possible to
statically compile Rust binaries without using musl. That was, in turn, a
reimplementation of other container inits like `tini` and `dumb-init`.

The reason for re-implementing `docker-init` is because it appears as though
all of the other implementations do not handle signals as correctly as they
should. In particular, they all appear to make use of `sigwait(2)` (`tini` does
a `sigtimedwait(2)` for an interval and then will do a `waitpid(2)` even if it
didn't detect a `SIGCHLD`). `catatonit` uses `signalfd(2)`, which [has its own
warts][signalfd-broken], but the improvements over `sigwait(2)` are significant
in terms of stability. Ideally we would just write a patch for the other
projects to use `signalfd(2)` rather than creating a new project, but after
some time spent looking at `tini` and `dumb-init` we felt that such patches
would be closer to full rewrites.

In addition, the purpose of `catatonit` is to only support the key usage by
`docker-init` which is `/dev/init -- <your program>`. With few exceptions, no
other features will be added.

[initrs]: https://github.com/cyphar/initrs
[signalfd-broken]: https://ldpreload.com/blog/signalfd-is-useless

### Usage ###

catatonit has identical usage to other basic `docker-init`'s -- you give it the
command and list of arguments to that command.

If you install `catatonit` to `/usr/bin/docker-init`, `docker run --init` will
use `catatonit` as its container pid1. Alternatively, you can configure the
Docker daemon to use `catatonit` without deleting any previously installed
`/usr/bin/docker-init` by using `--init-path` (or adding an `init-path` setting
in `/etc/docker/daemon.json`). Podman has similar options.

Catatonit supports a very limit subset of features, in order to keep the code
as simple as possible:

* If catatonit is not pid1 (in other words, you are not in a PID namespace), it
  will try to use the sub-reaper support in the kernel to act as a
  "pseudo-init" for the process you requested.

* You can pass `-g` if you want signals to be forwarded to the entire process
  group of your spawned process (otherwise it's just forwarded to the process
  spawned).

* If you wish to use catatonit as a convenient pause container (do not spawn a
  child process nor do any signal handling), you can pass `-P`.

If you want to include `catatonit` in your images, you can conveniently add it
to your Dockerfile as an entrypoint:

```dockerfile
# Runs "catatonit -- /my/amazing/script --with --args"
ENTRYPOINT ["catatonit", "--"]

# or if you use --rewrite or other cli flags
# ENTRYPOINT ["catatonit", "--rewrite", "2:3", "--"]

CMD ["/my/amazing/script", "--with", "--args"]
```

### Installation ###

catatonit uses autotools for building, so building is a fairly standard:

```
% ./autogen.sh
% ./configure
% make
% sudo make install
```

Note that this install the `catatonit` binary to `/usr/bin/catatonit`. If you
want to use `docker run --init` you may need to symlink `/usr/bin/docker-init`
to `catatonit` or configure Docker to use `catatonit`.

### License ###

catatonit is licensed under the GNU General Public License version 2 or later.

```
catatonit: a container init so simple it's effectively brain-dead
Copyright (C) 2018-2023 SUSE LLC

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

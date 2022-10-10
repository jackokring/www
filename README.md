# Generic Server

Place the directory structure at `/var/www` and run `config/initialize.sh` to perform all the default run requirements. This will add an application shortcut `server.desktop` for the current user.

## Apache/PHP

The default server is copied from `config` to the available sites and enabled. The necessary `apt install` is performed. The server root is `/var/www/html` on port `80` by default.

## Python

A local host simple server with `cgi-bin` is run with a root of `/var/www` on port `8000` and only bound to `localhost` to limit access to files. Various libraries are installed `pip install autograd wolframwebengine jax[cpu] mypy` for AI and static type analysis.

## Mathematica

A server is started to the `WolframEngine` in the `/var/www/wl` directory. Port `18000`. A license key is copied from `secrets` if present.

## Node.js

A server is started in `/var/www/node` on port `3000`. A `npm install express jquery bootstrap underscore browserify` is performed to provide a basic system.
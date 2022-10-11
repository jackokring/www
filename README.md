# Generic Server

Place the directory structure at `/var/www` and run `config/initialize.sh` to perform all the default run requirements. This will add an application shortcut `server.desktop` for the current user. Also `config/editor.sh` runs vscode with an environment addition from `config/environment.sh` for settings and has its own shortcut `editor.desktop`.

## Apache/PHP

The default server is copied from `config` to the available sites and enabled. The necessary `apt install` is performed. The server root is `/var/www/html` on port `80` by default. The JavaScript and CSS are cloned into subdirectories when built from the `less`, `js/client` and `ts/client` directories.

## Python

A local host simple server with `cgi-bin` is run with a root of `/var/www` on port `8000` and only bound to `localhost` to limit access to files. Various libraries are installed `pip install autograd wolframwebengine jax[cpu] mypy` for AI and static type analysis for use on the server. Client python is in `py/client` for apache serving.

## Mathematica

A server is started to the `WolframEngine` in the `/var/www/wl` directory. Port `18000`. A license key is copied from `secrets` if present. A mathematical tool.

## Node.js / TypeScript

A server is started in `/var/www/node` on port `3000`. A `npm install express jquery bootstrap underscore browserify typescript marked @types/marked` is performed to provide a basic system. The directories `ts/server`, `js/server` and `py/server` are copied to `node/js` and `node/py` to bring the server code.

## Markdown

Compiles markdown from `md` to HTML and moves it to the main `/var/www/html` folder and appends `.html` to the filename.

## Less

All less files end up in `html/css` with `.css` appended to the filename after the less compiler has produced its output from the `less` directory.
# Generic Server

Place repository at `~/www` (`https://github.com/jackokring/www.git` while in the `~` directory) and then maybe use `certbot-once.sh` if you have **already** set a domain name to point to the IP and have not got a server running on port `80` yet. This is important as the bot uses its own bind to authenticate DNS correctness (and so ownership). A few cron jobs are set up to maintain the SSL certificate. **There is a task for this** setup to run `certbot-once.sh`. You'll likely have to `sudo apt install git` to be able to clone the repository on a basic Debian GCloud VM. The certbot sets a cron job to keep the SSL keys updated.

# Simplified Curl Install

```
cd ~
curl -L https://raw.githubusercontent.com/jackokring/www/master/config-env.sh > install.sh
bash install.sh
# | bash will not work as the directory of the install will not be set correctly.
# you can rm ~/install.sh
```

# Check Source

The script `check-src.sh` checks the sources for errors where possible. TypeScript to JavaScript is such a node hog so no not here. **There is a task for this**. This is where any checks before launch are performed. For example it makes all `.sh` scripts executable. All site specific JavaScript is in `static/js/main.js`.

# Cron Monthly

A monthly check on the SSL keys is performed in `cron-monthly.sh` and any other monthly maintainance can be added in this script.

# Flask Start Up

The script `flask-up.sh` starts the flask debug server. **There is a task for this**. A `https` server is started by `flask-ssl-up.sh`. The `certbot-once.sh` would have created the keys for the SSL port `443` server. Don't forget to change the `DOMAIN` variable in `config.py` as the domain will very likely not be the same for you. It is used to locate the domain keys.

# Bootstrap and Less

The basic browser version of `main.less` CSS is available. A minified version of bootstrap is also served from a CDN. This makes easy HTML decoration, and cuts down on server loading.

# Markdown

A markdown load template loads the HTML template and requests a `/static/md` prepended to the page path after the host name and a `.md` on the end for mimetyping, so fetching and rendering the markdown into the page.

# Python and Pyodide

Browser Python via WASM is provided in `py.html` using a web worker. In a similar way to markdown `/static/py` with an appended `.py` is used to load code.

# Phinka

The `bin/phinka` script launches as a module to avoid missing module references. Basically `python -m phinka "$@"` with arguments. Phinka is also available via `pip install phinka` if you don't need the web server code. [Available on PyPI](https://pypi.org/project/phinka/). `pip3 install --upgrade pip` is your friend. So is `sudo apt install python-is-python3` along with the module `venv`.

`phinka.blwz` - a data-compression format using some of the best and adding in (or technically removing) **self-partition mutual information** (a form of information fission). In principal sections of the BWT could be removed as reconstructable just based on a length count and enough mutual information about previous and following letters. I expect that is computationally intensive though. A faster modulable source for information fusion technolgy is still sought.

`phinka.dx` - calculus tools and other mathemeatical functions. Various integral asymptotics about singularities, which could exhibit Goldstone oscillation of x, while f(x) remains constant perhaps?

# Generic Server

Place repository at `~/www` (`https://github.com/jackokring/www.git` while in the `~` directory) and then maybe use `certbot-once.sh` if you have **already** set a domain name to point to the IP and have not got a server running on port `80` yet. This is important as the bot uses its own bind to authenticate DNS correctness (and so ownership). A few cron jobs are set up to maintain the SSL certificate. There is a task setup to run `certbot-once.sh`. You'll likely have to `sudo apt install git` to be able to clone the repository on a basic Debian GCloud VM.

# Check Source

The script `check-src.sh` checks the sources for errors where possible, and compiles any TypeScript to JavaScript. There is a task for this.

# Flask Start Up

The script `flask-up.sh` starts the flask server. There is a task for this. Depending on the `DEBUG` variable in `config-env.sh` either the debug `http` or deploy `https` server is started. The `certbot-once.sh` creates the keys for the SSL port `443` server. Don't forget to change the `DOMAIN` variable in `config.py` as the domain will not be the same for you. It is used to locate the domain keys.

# Bootstrap and Less

The basic browser version of `.less` is available. A minified version of bootstrap is also served from a CDN. This makes easy HTML decoration, and cuts down on server loading.
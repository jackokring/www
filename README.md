# Generic Server

Place repository at `~/www` and then maybe use `certbot-once.sh` if you have already set a domain name to point to the IP and have not got a server running on port `80`. This is important as the bot uses its own bind to authenticate DNS correctness. A few cron jobs are set up to maintain the SSL certificate.

# Check Source

The script `check-src.sh` checks the source for errors where possible. There is a task for this.

# Flask Start Up

The script `flask-up.sh` starts the flask server. There is a task for this. Depending on the `DEBUG` variable in `config-env.sh` either the debug `http` or deploy `https` server is started.


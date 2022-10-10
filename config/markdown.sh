#!/usr/bin/sh
# process markdown
cd /var/www/md
for f in ./*.md
do
    echo "Processing 'md/$f' to 'html/$f.html'"
    # always double quote "$f" filename
    npx marked --gfm --input "$f" --output "/var/www/html/$f.html"
done
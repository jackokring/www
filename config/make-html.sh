#!/usr/bin/bash
# make html files from bodies

for f in body/*.html
do
    cat config/header.html "$f" config/footer.html > "html/$f"
done
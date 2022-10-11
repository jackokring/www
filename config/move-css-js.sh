#!/usr/bin/bash
# move css and js

# apache css/js
mkdir html/css
mkdir html/js
mkdir node/js

cd node/node_modules
nodeFiles="underscore/underscore.js
bootstrap/dist/js/bootstrap.js
jquery/dist/jquery.js"

for f in nodeFiles
do
    cp "$f" ../../html/js
done

cd ../../js
for f in client/*.js
do
    cp "$f" ../html/js
done

npx browserify client/*.js > browserified-all.js 

for f in server/*.js
do
    cp "$f" ../node/js
done

nodeCSS="bootstrap/dist/css/bootstrap.css"

for f in nodeCSS
do
    cp "$f" ../../html/css
done

cd ../css
for f in *.css
do
    cp "$f" ../html/css
done

cd ../less
for f in *.less
do
    npx lessc "$f" "../html/css/$f.css"
done

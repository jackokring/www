function markdown(target, callback) {
    if(!callback) {
        callback = (error, html) => {
            // perform default
            console.log(error);
        }
    }
    fetch(window.location.host + '/static/md'
        + window.location.pathname + '.md')
    .then((response) => {
        if(response.ok) {
            return response.text();
        }
    })
    .then((result) => {
        document.getElementById(target).innerHTML
            = marked.parse(result, { gfm: true }, callback);
    });
}

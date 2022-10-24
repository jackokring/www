function markdown(target) {
    fetch(window.location.host + '/md'
        + window.location.pathname + '.md')
    .then((response) => {
        if(response.ok) {
            return response.text();
        }
    })
    .then((result) => {
        document.getElementById(target).innerHTML = marked.parse(result);
    });
}

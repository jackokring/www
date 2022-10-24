function markdown(target) {
    fetch(window.location.href + '.md')
    .then((response) => {
        if(response.ok) {
            return response.text();
        }
    })
    .then((result) => {
        document.getElementById(target).innerHTML = marked.parse(result);
    });
}

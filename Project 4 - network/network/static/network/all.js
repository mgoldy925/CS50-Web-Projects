document.addEventListener('DOMContentLoaded', function() {

    // Change page
    INFO.which = 'all';

    // Add eventListener for submitting new post
    try {
        document.querySelector('#create').addEventListener('submit', create_post);
    } catch(err) { }

    // var current_path = window.location.pathname;
    // current_path = current_path.substring(current_path.lastIndexOf("/") + 1, current_path.length);
    // if (current_path == '') current_path = "all";
    // load_posts(`${current_path}`);
    load_posts();
});

function create_post() {
    // Get content add submit it to API to create post
    var content = document.querySelector('#content').value;
    fetch('/create', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
    })
    .then(() => {
        // Reload page and return false to not refresh page
        load_posts('all');
        return false;
    });
}
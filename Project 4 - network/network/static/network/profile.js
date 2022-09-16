document.addEventListener('DOMContentLoaded', function() {

    // Change page
    INFO.which = document.querySelector('#profile-name').innerHTML;

    // Add eventListener for following a user
    try {
        document.querySelector('#follow').addEventListener('click', follow);
    } catch(err) {}

    load_posts();
});

function follow() {
    // Get user to follow, def buggy way to do it
    var name = document.querySelector('#profile-name').innerHTML;
    // Post to api
    fetch(`/follow`, {
        method: 'POST',
        body: JSON.stringify({
            name: name
        })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('#follow').innerHTML = data.followed ? "Unfollow" : "Follow";
        document.querySelector('#follower-count').innerHTML =  data.num_followers;
        load_posts(name);
        return false;
    });
}
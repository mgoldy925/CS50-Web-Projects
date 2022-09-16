const NUM_PAGINATOR_PAGES = 5;  // Number of pages to displayed for paginator nav

// Info for current pages
var INFO = {
    current: 0,
    first: 0,
    previous: 0,
    next: 0,
    last: 0,
    which: ''
}

document.addEventListener('DOMContentLoaded', function() {
    var builtin_pages = document.querySelectorAll('.pagination > li');
    let i = 0;
    for (let key in INFO) {
        if (key != 'current' && key != 'which') {
            builtin_pages[i++].addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    left: 0,
                    behavior: 'smooth'
                });
                load_posts(INFO[key]);
                return false;
            });
        }
    }
});

function load_posts(current = 0) {
    // Create correct URL and get posts
    var url_end = current ? `/${current}` : '';
    fetch(`/get/${INFO.which}${url_end}`)
    .then(response => response.json())
    .then(data => {
        // Get info and posts
        var info = data.info;
        var posts = data.posts;
        
        // Get total num of pages & other stuff & update global vars
        INFO.last = info.last;
        INFO.current = info.current;
        INFO.previous = Math.max(INFO.first, INFO.current-1);
        INFO.next = Math.min(INFO.last, INFO.current+1);
        INFO.which = info.which;

        // Set correct paginator numbers
        create_paginators();
        if (INFO.current == 0) {
            document.querySelector('#previous').style.display = 'none';
        } else {
            document.querySelector('#previous').style.display = '';
        }

        if (posts.length < 10) {
            document.querySelector('#next').style.display = 'none';
        } else {
            document.querySelector('#next').style.display = '';
        }

        // Get total num of pages
        all_posts = document.querySelector('#posts');
        if (posts.length === 0) {
            all_posts.innerHTML = 'No posts.';
        } else {
            var user = info.user;
            var authenticated = info.authenticated;

            all_posts.innerHTML = '';
            posts.forEach(post => {
                // Create html element for a given post
                var main_div = document.createElement('div');

                var post_div = document.createElement('div');
                post_div.classList.add('container', 'post');
                post_div.setAttribute('data-id', post.id);

                var name_wrapper = document.createElement('h5');
                var name = document.createElement('a');
                var datetime_posted = document.createElement('p');
                var content = document.createElement('p');
                var likes = document.createElement('p');
                
                name.innerHTML = post.poster;
                name.href = post.url;
                datetime_posted.innerHTML = "Posted at: " + post.posted;
                content.innerHTML = post.content;
                content.id = "content";
                likes.innerHTML = post.likes.length + " Likes";

                name_wrapper.appendChild(name);
                post_div.appendChild(name_wrapper);
                post_div.appendChild(datetime_posted);
                post_div.appendChild(content);
                post_div.append(likes);
                main_div.append(post_div);

                if (post.posted != post.edited) {
                    var datetime_edited = document.createElement('p');
                    datetime_edited.innerHTML = "Edited at: " + post.edited;
                    datetime_edited.id = "edit-time";
                    post_div.insertBefore(datetime_edited, content);
                }
                
                if (authenticated) {
                    var like_btn = document.createElement('button');
                    like_btn.innerHTML = contains(user, post.likes) ? "Unlike" : "Like";
                    like_btn.classList.add('btn', 'btn-primary');
                    like_btn.style.float = "left";
                    like_btn.addEventListener('click', () => like(like_btn));
                    post_div.insertBefore(like_btn, likes);
                    
                    if (user.username == post.poster) {
                        var edit_btn = document.createElement('button');
                        edit_btn.innerHTML = "Edit";
                        edit_btn.classList.add('btn', 'btn-primary');
                        edit_btn.style.float = 'right';
                        edit_btn.addEventListener('click', () => edit(edit_btn));                    
                        post_div.insertBefore(edit_btn, content);

                        var edit_div = post_div.cloneNode(false);
                        var new_name_wrapper = name_wrapper.cloneNode(true);
                        var cancel_btn = edit_btn.cloneNode(true);
                        var submit_btn = edit_btn.cloneNode(true);
                        var input_content = document.createElement('textarea');

                        cancel_btn.innerHTML = "Cancel";
                        submit_btn.innerHTML = "Submit";
                        cancel_btn.addEventListener('click', () => edit(cancel_btn)); 
                        submit_btn.addEventListener('click', () => edit(submit_btn)); 
                        input_content.value = content.innerHTML;
                        input_content.rows = 6;
                        input_content.cols = 140;
                        edit_div.style.display = "none";

                        edit_div.appendChild(new_name_wrapper);
                        edit_div.appendChild(cancel_btn);
                        edit_div.appendChild(submit_btn);
                        edit_div.appendChild(input_content);
                        main_div.appendChild(edit_div);
                    }
                }
                
                all_posts.appendChild(main_div);
            });
        }

    })
    .catch((error) => {
        console.log(error);
    });
}


function create_paginators(info) {

    // Get div to put page numbers into
    var pages = document.querySelector('#page-numbers');
    pages.innerHTML = '';

    // Get range of page numbers to display
    var extra_pages = Math.floor(NUM_PAGINATOR_PAGES / 2);
    var numbers = []
    for (let num = Math.max(INFO.first, INFO.current - extra_pages); num <= Math.min(INFO.last, INFO.current + extra_pages); num++) {
        numbers.push(num);
    }

    // Create elements for each page
    for (let num of numbers) {
        let a = document.createElement('a');
        a.innerHTML = num;
        a.classList.add('page-link');
        
        // Add event listener to change pages
        a.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                left: 0,
                behavior: 'smooth'
            });
            load_posts(num);
            return false;
        });

        let li = document.createElement('li');
        li.classList.add('page-item');
        li.appendChild(a);
        pages.appendChild(li);
    }
}


function like(btn) {
    // Post to api
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            id: btn.parentElement.dataset.id
        })
    })
    .then(response => response.json())
    .then(data => {
        btn.innerHTML = data.liked ? "Unlike" : "Like";
        btn.nextElementSibling.innerHTML = `${data.num_likes} Likes`;
        return false;
    });
}


function edit(btn) {
    var main_div_children = btn.parentElement.parentElement.childNodes;
    var post_div = main_div_children[0];
    var edit_div = main_div_children[1];

    // If we want to edit
    if (edit_div.style.display == "none") {
        // Change display of what we're looking at rn
        edit_div.style.display = "block";
        post_div.style.display = "none";
        edit_div.querySelector('textarea').value = post_div.querySelector('#content').innerHTML;
    }
    // Else if we want to submit or cancel (this whole function can easily be broken)
    else {
        // Check if submitting or cancelling
        if (btn.innerHTML == "Submit") {
            // Make sure post content is valid
            var new_content = edit_div.querySelector('textarea').value;
            if (new_content) {
                fetch('/edit', {
                    method: "POST",
                    body: JSON.stringify({
                        id: edit_div.dataset.id,
                        content: new_content
                    })
                })
                .then(response => response.json())
                .then(data => {
                    var datetime_edited = post_div.querySelector('#edit-time');
                    var content = post_div.querySelector('#content');
                    if (datetime_edited == null) {
                        datetime_edited = document.createElement('p');
                        datetime_edited.id = "edit-time";
                        post_div.insertBefore(datetime_edited, content);
                    }
                    datetime_edited.innerHTML = "Edited at: " + data.time;
                    content.innerHTML = new_content;
                    edit_div.style.display = "none";
                    post_div.style.display = "block";
                });
            } else {
                alert("You cannot make a blank post.");
            }
        } else if (btn.innerHTML == "Cancel") {
            // Switch display back
            edit_div.style.display = "none";
            post_div.style.display = "block";
        }
        
    }
}


function contains(obj, list) {
    for (var element of list) {
        if (element.username == obj.username) {
            return true;
        }
    }
    return false;
}
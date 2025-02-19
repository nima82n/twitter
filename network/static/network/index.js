
function follow() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const button = document.querySelector('#follow');
    const userId = button.dataset.userid;
    fetch('follow_unfollow', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            userId: userId
        })
    })
    .then(response => console.log(response))
    .catch(error => console.error(error))
    document.querySelector('#follow-button').innerHTML = `<button type="button" class="btn btn-primary" data-userId='${userId}' id='unfollow' onclick='unfollow()' >Unfollow</button>`
    let followerCount = parseInt(document.querySelector('#followers-count').innerHTML);
    followerCount++;
    document.querySelector('#followers-count').innerHTML = followerCount;
}


function unfollow() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const button = document.querySelector('#unfollow');
    const userId = button.dataset.userid;
    fetch('follow_unfollow', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            userId: userId
        })
    })
    .then(response => console.log(response))
    .catch(error => console.error(error))
    document.querySelector('#follow-button').innerHTML = `<button type="button" class="btn btn-primary" data-userId='${userId}' id='follow' onclick='follow()' >Follow</button>`
    let followerCount = parseInt(document.querySelector('#followers-count').innerHTML);
    followerCount--;
    document.querySelector('#followers-count').innerHTML = followerCount;
}


function editBox(boxNum) {
    document.querySelector(`#post-body-${boxNum}`).style.display = 'none';
    document.querySelector(`#edit-div-${boxNum}`).style.display = 'block';
    document.querySelector(`#edit-${boxNum}`).style.display = 'none';
}


function editPost(postNum) {
    const csrfToken = document.querySelector(`#csrf-${postNum}`).value;
    const content = document.querySelector(`#text-${postNum}`).value;
    const postId = document.querySelector(`#postId-${postNum}`).value;

    fetch('/edit', {
        method: 'PATCH', 
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content: content,
            postId: postId,
            action: 'edit'
        })
    })
    .then(response => console.log(response.messege))
    .catch(error => console.error(error))
    document.querySelector(`#post-body-${postNum}`).innerHTML = content;
    document.querySelector(`#post-body-${postNum}`).style.display = 'block';
    document.querySelector(`#edit-div-${postNum}`).style.display = 'none';
    document.querySelector(`#edit-${postNum}`).style.display = 'block';

}


function like(postId) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('/likeunlike', {
        method: 'PATCH', 
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            postId: postId,
            action: 'like'
        })
    })
    .then(response => console.log(response))
    .catch(error => console.error(error))

    .then(fetch(`/likeNum/${postId}`)
    .then(response => response.json())
    .then((data) => {
        let likes = parseInt(data.likes);
        document.querySelector(`#like-container-${postId}`).innerHTML = `<div id='unlike-${postId}' onclick='unlike(${postId})' >❤️ ${likes } </div>`
    })
    .catch(error => console.error(error)))
}


function unlike(postId) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('/likeunlike', {
        method: 'PATCH', 
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            postId: postId,
            action: 'unlike'
        })
    })
    .then(response => console.log(response))
    .catch(error => console.error(error))
    
    .then(fetch(`/likeNum/${postId}`)
    .then(response => response.json())
    .then(data => {
        let likes = parseInt(data.likes);
        console.log(likes)
        document.querySelector(`#like-container-${postId}`).innerHTML = `<div id='like-${postId}' onclick='like(${postId})' >🤍 ${likes} </div>`
    })
    .catch(error => console.error(error)))

}
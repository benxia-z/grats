// Maps post content to original body when editing
let postContent = new Map();

function editPost(postId) {
  postBody = document.querySelector('#post-' + postId).innerHTML;
  postContent.set('post-' + postId, postBody);
  editPostForm = // Setting inner post content to editor view
    `<div class="input-group"> 
      <textarea class="form-control" id="editPostText-${postId}" rows="3" cols="50">${postBody}</textarea> 
      <div class="input-group-append"> 
        <button type="button" class="btn btn-primary btn-sm update-button" post_id="${postId}">Submit</button> 
        <button type="button" class="btn btn-primary btn-sm cancel-button" post_id="${postId}">Cancel</button> 
      </div>
    </div>`;
  document.querySelector('#post-' + postId).innerHTML = editPostForm;

  // Adding event listeners for editor buttons
  let cancelBtns = document.querySelectorAll('.cancel-button');
  for (let i = 0; i < cancelBtns.length; i++) {
    cancelBtns[i].addEventListener('click', cancelPost);
  }

  let updateBtns = document.getElementsByClassName('update-button');
  for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', updatePost);
  }  
};

let updatePost = function(event) {
  let post_id = event.target.getAttribute('post_id');
  let body = document.querySelector('#editPostText-' + post_id).value;
  let data = {id: post_id, body: body};

  const promise = fetch('/update_post', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: new Headers({
      "content-type": "application/json"
    })
  });

  promise.then(function(response) {
    return response.json()
  })
  .then(function(data) {
    console.log('Success: ', data);
    document.querySelector('#post-' + post_id).innerHTML = body;
  })
  .catch(function(error) {
    console.error('Error', error);
    alert('Internal Server Error');
  });
}

function cancelPost(event) {
  let post_id = event.target.getAttribute('post_id');
  let body = postContent.get("post-" + post_id);
  document.querySelector('#post-' + post_id).innerHTML = body;
}

function deletePost(postId) {
  let data = {id: postId};
  const promise = fetch('/delete_post', {
    method: 'DELETE',
    body: JSON.stringify(data),
    headers: new Headers({
      "content-type": "application/json"
    })
  });

  promise.then(function(response) {
    return response.json()
  })
  .then(function(data) {
    console.log('Success: ', data);
    window.location.replace(data.redirect);
  })
  .catch(function(error) {
    console.error('Error', error);
    alert('Internal Server Error');
  });
};

/*const btn = document.querySelector('.btn-toggle');

btn.addEventListener('click', function() {
  document.body.classList.toggle('dark-theme')
}) */ 
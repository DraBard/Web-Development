document.addEventListener('DOMContentLoaded', function() {

    const editButtons = document.querySelectorAll('#editButton');
    const saveButtons = document.querySelectorAll('#saveButton');
    const editTextareas = document.querySelectorAll('#editTextarea');
    const editForms = document.querySelectorAll('#editForm');
    const text = document.querySelectorAll(".text")

    editButtons.forEach((editButton, index) => {
        const postId = editButton.getAttribute('data-post-id'); // Get the post ID
        editButton.addEventListener('click', function(){
        if (editTextareas[index].style.display === 'none') {
            editTextareas[index].style.display = 'block';
            saveButtons[index].style.display = 'block';
        } 
        else {
            editTextareas[index].style.display = 'none';
            saveButtons[index].style.display = 'none';
        }
        });

        editForms[index].addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission behavior
            
            const formData = new FormData();
            formData.append('content', editTextareas[index].value);
            formData.append('post_id', postId);
            console.log(formData)
            
            fetch('edit/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle the server's response if needed
  
                // You can update the UI here if necessary
                
                // Update the textarea and hide the save button
                text[index].textContent = data.content;
                editTextareas[index].style.display = 'none';
                saveButtons[index].style.display = 'none';
            })
            .catch(error => {
                console.error('There was a problem:', error);
            });        
        });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }
    });

    const likeButtons = document.querySelectorAll("#likeButton");
    const like = document.querySelectorAll(".like")

    likeButtons.forEach((likeButton, index) => {
        likeButton.addEventListener('click', function() {
        console.log("clicked")
        const postId = likeButton.getAttribute('post-id');
        console.log(postId)
        fetch(`like/${postId}/`)
        .then(response => {
            // Check if the response is okay (status code 200-299)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Parse the response body as JSON
            return response.json();
        })
        .then(data => {
            // Here, data is the parsed JSON from the response
            console.log(data);

            // Update the button text based on the action
            if (data.action === 'like') {
                likeButton.textContent = 'Like';

                const currentLikes = parseInt(like[index].textContent); // Parse current text content to integer
                const updatedLikes = currentLikes - 1; // Increment by 1
                like[index].textContent = updatedLikes.toString(); // Update text content with

            } else if (data.action === 'unlike') {
                likeButton.textContent = 'Unlike';

                const currentLikes = parseInt(like[index].textContent); // Parse current text content to integer
                const updatedLikes = currentLikes + 1; // Increment by 1
                like[index].textContent = updatedLikes.toString(); // Update text content with

            } else {
                console.error('Unexpected action:', data.action);
            }

            // // Refresh the page
            // window.location.reload();
        })
        .catch(error => {
            // Handle errors (failed network request, JSON parsing error, etc.)
            console.error('There was a problem:', error);
        })});
    });

    const followButton = document.getElementById('followButton');

    if (followButton) {
        followButton.addEventListener('click', function() {
            const targetUserId = this.dataset.userId;

            fetch(`/toggle_follow/${targetUserId}/`)
            .then(response => {
                // Check if the response is okay (status code 200-299)
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                // Parse the response body as JSON
                return response.json();
            })
            .then(data => {
                // Here, data is the parsed JSON from the response
                console.log(data);

                // Update the button text based on the action
                if (data.action === 'follow') {
                    followButton.textContent = 'Unfollow';
                } else if (data.action === 'unfollow') {
                    followButton.textContent = 'Follow';
                } else {
                    console.error('Unexpected action:', data.action);
                }

                // Refresh the page
                window.location.reload();
            })
            .catch(error => {
                // Handle errors (failed network request, JSON parsing error, etc.)
                console.error('There was a problem:', error);
            })});
    };
});


document.addEventListener('DOMContentLoaded', function() {
    const followButton = document.getElementById('followButton');

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
        })
        .catch(error => {
            // Handle errors (failed network request, JSON parsing error, etc.)
            console.error('There was a problem:', error);
        });
    });
});


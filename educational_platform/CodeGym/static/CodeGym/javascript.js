document.addEventListener('DOMContentLoaded', function() {


    const codingForm = document.getElementById('coding');
    
    if (codingForm) {

        codingForm.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log("klikniete");
    
             // Function to get CSRF token from cookies
            function getCookie(name) {
                const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
                return cookieValue ? cookieValue.pop() : '';
            }
    
            const code = document.getElementById('console').value;
            console.log(code);
            fetch('run_code/', {
            method: 'POST',
            body: JSON.stringify({
                'code': code
            }),
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
            });

    }


})
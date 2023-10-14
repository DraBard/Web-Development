document.addEventListener('DOMContentLoaded', function() {


    const codingForm = document.getElementById('coding');
    
    if (codingForm) {

        codingForm.addEventListener('submit', function(event) {
            event.preventDefault();
    
             // Function to get CSRF token from cookies
            function getCookie(name) {
                const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
                return cookieValue ? cookieValue.pop() : '';
            }
    
            const code_in = document.getElementById('console_in').value;
            const code_out = document.getElementById('console_out');

            console.log(code_in);
            fetch('run_code/', {
            method: 'POST',
            body: JSON.stringify({
                'code_in': code_in
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

            .then(data => {
                console.log(data)
                code_out.value = data.output;
            })

            .catch(error => {
                console.error('Fetch error:', error);  // This logs any network or parsing errors
            });
            });
    }
})
// Handle order increment/decrement buttons
const incrementCreateOrderBtn = document.getElementById('incrementCreateOrderBtn');
const decrementCreateOrderBtn = document.getElementById('decrementCreateOrderBtn');
const createOrderDisplay = document.getElementById('createOrderDisplay');

if (incrementCreateOrderBtn && decrementCreateOrderBtn && createOrderDisplay) {
    incrementCreateOrderBtn.addEventListener('click', function (event) {
        event.preventDefault();
        let currentOrder = parseInt(createOrderDisplay.value);
        createOrderDisplay.value = currentOrder + 1;
    });

    decrementCreateOrderBtn.addEventListener('click', function (event) {
        event.preventDefault();
        let currentOrder = parseInt(createOrderDisplay.value);
        if (currentOrder > 1) {
            createOrderDisplay.value = currentOrder - 1;
        }
    });
}

const addQuestionForm = document.getElementById('addQuestionForm');
if (addQuestionForm) {
    addQuestionForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        var url = window.location.pathname;
        const surveyId = url.substring(url.lastIndexOf('/') + 1);

        const payload = {
            question_text: data.question_text,
            order: parseInt(data.order),
            is_mandatory: data.is_mandatory
        };

        try {
            const response = await fetch(`/question/create/${surveyId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });
            if (response.ok) {
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}
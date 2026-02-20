function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};


function logout() {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }

    window.location.href = '/auth/login-page';
};


document.querySelectorAll('.editQuestionButton').forEach(button => {

    button.addEventListener('click', function (event) {

        event.preventDefault();

        const questionId = event.currentTarget.dataset.questionId;

        const url = `/admin/edit-question/${questionId}`;

        window.location.href = url;
    });

});


const deleteQuestionButtons = document.querySelectorAll('.deleteQuestionButton')
if (deleteQuestionButtons){
    
    deleteQuestionButtons.forEach(button => {

        button.addEventListener('click', async function (event) {

            event.preventDefault();

            const questionId = event.currentTarget.dataset.questionId;

            try {
                const response = await fetch(`/question/delete/${questionId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getCookie('access_token')}`
                    }
                });
                if (response.ok) {
                    window.location.reload(true);
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    });
}


const deleteQuestionOptionButtons = document.querySelectorAll('.deleteQuestionOptionButton')
if (deleteQuestionOptionButtons){
    
    deleteQuestionOptionButtons.forEach(button => {
        button. addEventListener('click', async function (event) {

            event.preventDefault();

            const questionOptionId = event.currentTarget.dataset.questionOptionId;
            console.log(questionOptionId)
            
            try {
                const response = await fetch(`/question/question_option/delete/${questionOptionId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getCookie('access_token')}`
                    }
                });
                if (response.ok) {
                    window.location.reload(true);
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    });
}


const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);

        const payload = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            payload.append(key, value);
        }

        try {
            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: payload.toString()
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `access_token=${data.access_token}; path=/`;
                window.location.href = '/admin/survey';
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


// Handle order increment/decrement buttons
const incrementOrderBtn = document.getElementById('incrementOrderBtn');
const decrementOrderBtn = document.getElementById('decrementOrderBtn');
const orderDisplay = document.getElementById('orderDisplay');

if (incrementOrderBtn && decrementOrderBtn && orderDisplay) {
    incrementOrderBtn.addEventListener('click', function (event) {
        event.preventDefault();
        let currentOrder = parseInt(orderDisplay.value);
        orderDisplay.value = currentOrder + 1;
    });

    decrementOrderBtn.addEventListener('click', function (event) {
        event.preventDefault();
        let currentOrder = parseInt(orderDisplay.value);
        if (currentOrder > 1) {
            orderDisplay.value = currentOrder - 1;
        }
    });
}

const editQuestionForm = document.getElementById('editQuestionForm');
if (editQuestionForm) {
    editQuestionForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        var url = window.location.pathname;
        const questionId = url.substring(url.lastIndexOf('/') + 1);

        const payload = {
            question_text: data.question_text,
            order: parseInt(data.order),
            is_mandatory: data.is_mandatory
        };

        try {
            const response = await fetch(`/question/update/${questionId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });
            if (response.ok) {
                const result = await response.json();
                if (!result || !result.survey_id) {
                    alert('Survey ID not returned from server.');
                    return;
                }
                window.location.href = `/admin/question/${result.survey_id}`;
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


const addQuestionOptionForm = document.getElementById('addQuestionOptionForm');
if (addQuestionOptionForm) {
    addQuestionOptionForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        var url = window.location.pathname;
        const questionId = url.substring(url.lastIndexOf('/') + 1);

        const payload = {
            value: data.value,
            order: parseInt(data.order)
        };

        try {
            const response = await fetch(`/question/question_option/create/${questionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });
            if (response.ok) {
                window.location.reload(true);
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


const surveyResponseForm = document.getElementById("surveyResponseForm");
if (surveyResponseForm) {
    surveyResponseForm.addEventListener('submit', async function (event) {

        event.preventDefault();

        const params = new URLSearchParams(window.location.search);
        
        const pathParts = window.location.pathname.split('/');
        const surveyId = pathParts[3].split('?')[0];
        const restaurantCode = params.get("restaurant_code");

        if (!restaurantCode) {
            alert('Restaurant code is missing. Please go back and enter it.');
            return;
        }

        const response_payload = {
            restaurant_code: restaurantCode,
            begin_date: new Date().toISOString(),
            end_date: new Date().toISOString()
        }

        let responseId;
        try{
            const response = await fetch(`/response/create/${surveyId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(response_payload)
            });
            if (response.ok) {
                const data = await response.json();
                responseId = parseInt(data.response_id);
            } else{
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch(error){
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        };

        const cards = document.querySelectorAll(".card");

        for(const card of cards){
            const questionId = parseInt(card.dataset.questionId);
            const checked = card.querySelector("input[type=radio]:checked");

            if (!checked) return;
            const optDiv = checked.closest(".form-check");
            const questionOptionId = parseInt(optDiv.dataset.questionOptionId);

            let answerId;
            const answer_payload = {}
            try{
                const response = await fetch(`/answer/create/${responseId}/${questionId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(answer_payload)
                });
                if (response.ok) {
                    const data = await response.json();
                    answerId = data.answer_id;
                } else{
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch(error){
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            };

            const answer_option_payload = {};
            try{
                const response = await fetch(`/answer/answer_option/create/${answerId}/${questionOptionId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(answer_option_payload)
                });
                if (response.ok) {
                } else{
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch(error){
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            };
        };
        
    });
}
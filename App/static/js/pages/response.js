const pathParts = window.location.pathname.split('/');
const surveyId = pathParts[3];
const city = getCookie("city");
var responseId=-1;

document.addEventListener("DOMContentLoaded", async () => {
    
    if (!city) {
        alert('City not found. Please select a city first.');
        window.location.href = `/survey/city/${surveyId}`;
        return;
    }

    const payload = {
        city: city,
        begin_date: new Date().toISOString(),
        end_date: null
    };

    try{
            const response = await fetch(`/response/create/${surveyId}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });

            if (response.ok){
                const data = await response.json();
                responseId = data.response_id;
            }else{
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        }catch(error){
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        };
    
    const newResponseForm = document.getElementById("newResponseForm");
    if (newResponseForm) {
        newResponseForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const answers = [];

            document.querySelectorAll(".form-check-input:checked").forEach(input => {

                const questionId = input.closest(".card").dataset.questionId;
                const questionOptionId = input.closest(".form-check").dataset.questionOptionId;

                console.log(questionId)
                console.log(questionOptionId)

                const answer_various = {
                    answer: null,
                    question_id: questionId
                }

                console.log(answer_various)

                const answer_and_option = {
                    answer: answer_various,
                    question_option_id: questionOptionId
                }

                console.log(answer_and_option)

                answers.push(answer_and_option)

            });

            const payload = {answers: answers};
            
            try{
                const response = await fetch(`/answer/create/${responseId}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                if (response.ok){
                    window.location.href = `/survey/city/${surveyId}`;
                }else{
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            }catch(error){
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            };
        });
    }

});


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
const pathParts = window.location.pathname.split('/');
const surveyId = pathParts[3];

document.addEventListener("DOMContentLoaded", async () => {

    const form = document.getElementById("newResponseForm");

    form.addEventListener("change", async function (event) {

        if (!event.target.matches('input[type="radio"]')) return;
        
        const input = event.target;

        const questionId = input.closest(".card").dataset.questionId;
        const questionOptionId = input.closest(".form-check-label").dataset.questionOptionId;


        try{
            const response = await fetch(`/question/dependency/${questionId}/${questionOptionId}/${surveyId}`, {
                method: "GET",
                headers: {'Content-Type': 'application/json'}
            });
            if (response.ok){
                const data = await response.json();
                
                // Hide only dependent questions from this specific source question
                document.querySelectorAll(`[data-depends-on-question="${questionId}"]`).forEach(card => {
                    card.style.display = 'none';
                });
                
                if (data.has_dependency && data.question) {
                    // Check if dependent question already exists
                    let questionCard = document.querySelector(`[data-question-id="${data.question.question_id}"]`);
                    
                    if (!questionCard) {
                        // Create new question card
                        questionCard = createQuestionCard(data.question, data.options, questionId);
                        
                        // Insert in the correct order position
                        const allCards = Array.from(form.querySelectorAll('.card[data-question-id]'));
                        const submitButton = form.querySelector('button[type="submit"]').parentElement;
                        let inserted = false;
                        
                        for (const card of allCards) {
                            const cardOrder = parseInt(card.dataset.questionOrder || 999);
                            if (data.question.order < cardOrder) {
                                form.insertBefore(questionCard, card);
                                inserted = true;
                                break;
                            }
                        }
                        
                        // If not inserted, append before submit button
                        if (!inserted) {
                            form.insertBefore(questionCard, submitButton);
                        }
                    } else {
                        // Show existing question card
                        questionCard.style.display = 'block';
                    }
                    
                    // Scroll to the dependent question
                    questionCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            }else{
                console.error('Error loading dependent questions');
            }
        }catch(error){
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        };
        

    });
    
    const newResponseForm = document.getElementById("newResponseForm");
    if (newResponseForm) {
        newResponseForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const answers = [];

            document.querySelectorAll(".form-check-input:checked").forEach(input => {

            const questionId = Number(input.closest(".card").dataset.questionId);
            const questionOptionId = Number(input.closest(".form-check-label").dataset.questionOptionId);

                const answer_various = {
                    answer: null,
                    question_id: questionId
                }

                const answer_and_option = {
                    answer: answer_various,
                    question_option_id: questionOptionId
                }

                answers.push(answer_and_option)

            });

            const payload = {answers: answers};
            
            try{
                const response = await fetch(`/answer/create`, {
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


function createQuestionCard(question, options, sourceQuestionId) {
    const card = document.createElement('div');
    card.className = 'card border-0 shadow-sm mb-4';
    card.setAttribute('data-question-id', question.question_id);
    card.setAttribute('data-question-order', question.order);
    card.setAttribute('data-is-dependent', 'true');
    card.setAttribute('data-depends-on-question', sourceQuestionId);
    
    let optionsHtml = '';
    options.forEach(opt => {
        optionsHtml += `
            <div class="form-check p-0">
                <label data-question-option-id="${opt.question_option_id}"
                    class="form-check-label option-item d-flex align-items-center w-100
                            border rounded-3 px-3 py-3">
                    <input class="form-check-input me-3" 
                           type="radio" 
                           name="question_${question.question_id}">
                    <span class="small">${opt.value}</span>
                </label>
            </div>
        `;
    });
    
    card.innerHTML = `
        <div class="px-4 py-3 border-bottom">
            <h6 class="mb-0 fw-semibold">${question.question_text}</h6>
        </div>
        <div class="card-body px-4 py-3">
            <div class="d-flex flex-column gap-2">
                ${optionsHtml}
            </div>
        </div>
    `;
    
    return card;
}


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
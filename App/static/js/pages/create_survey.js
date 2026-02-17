const createSurveyForm = document.getElementById("createSurveyForm");
if (createSurveyForm) {
    createSurveyForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        const answers = [];
    
        const surveyStatusId = document.getElementById("selectStatus").value;

        const payload = {
            name: data.name,
            description: data.description,
            start_date: data.start_date + "T00:00:00",
            end_date: data.end_date
                ? data.end_date + "T00:00:00"
                : null,
            min_responses: 0,
            max_responses: 1
        };


        console.log(payload)

        try{
            const response = await fetch(`/survey/create/${surveyStatusId}`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });
            if (response.ok){
                window.location.href="/admin/survey";
            }else{
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        }catch(error){
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    }); 
}

const cityForm = document.getElementById("cityForm");
if (cityForm) {
    cityForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const city_id = document.getElementById("city").value;

        const pathParts = window.location.pathname.split('/');
        const surveyId = parseInt(pathParts[3]);

        const payload = {
            city_id: parseInt(city_id),
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
            }else{
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        }catch(error){
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        };

        window.location.href = `/survey/fill/${surveyId}`;
        return
    });
};
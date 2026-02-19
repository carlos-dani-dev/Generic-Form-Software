const createDependencyForm = document.getElementById("createDependencyForm");
if (createDependencyForm){
    createDependencyForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        var url = window.location.pathname;
        const chosenQuestionId = url.substring(url.lastIndexOf('/') + 1);

        const targetQuestionId = document.getElementById("dependency-question").value;
        const sourceQuestionOptionId = document.querySelector(".form-check-input:checked").value;

        const payload={
            source_question_option_id: sourceQuestionOptionId,
            target_question_id: targetQuestionId,
            action: "SHOW"
        }

        var newOrder = 0;

        try {
            const response = await fetch(`/question/dependency/create/${chosenQuestionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });
            if (response.ok) {
                const order = await response.json();
                newOrder = parseInt(order) + 1;
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }

        const payload_={
            order: newOrder,
            is_mandatory: true,
            is_independent: false
        }

        try {
            const response = await fetch(`/question/update/${targetQuestionId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload_)
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
        window.location.href=`/admin/edit-question/${chosenQuestionId}`;
    });
}

const deleteDependencyButton = document.getElementById("deleteDependencyButton");
if (deleteDependencyButton){
    deleteDependencyButton.addEventListener("click", async function (event){
        event.preventDefault();

        var url = window.location.pathname;
        const chosenQuestionId = url.substring(url.lastIndexOf('/') + 1);

        try {
            const response = await fetch(`/question/dependency/delete/${chosenQuestionId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                }
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

        const payload_={
            order: 1,
            is_mandatory: true,
            is_independent: true
        }

        try {
            const response = await fetch(`/question/update/${chosenQuestionId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload_)
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

        try {
            const response = await fetch(`/question/update/${targetQuestionId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload_)
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

        const url = `/admin/edit-question/${chosenQuestionId}`;
        window.location.href = url;
    });
}
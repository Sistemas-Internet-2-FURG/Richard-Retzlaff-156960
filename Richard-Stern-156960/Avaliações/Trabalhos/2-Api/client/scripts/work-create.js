document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem('access_token');
    
    const form = document.getElementById('workForm');
    const courseSelect = document.getElementById('course');

    try {
        const response = await fetch('http://localhost:5000/courses', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            }
        });
    
        if (response.ok) {
            const courses = await response.json();
    
            courses.forEach(course => {
                const option = document.createElement('option');
                option.value = course.id;
                option.textContent = course.title;
                courseSelect.appendChild(option);
            });
        } else {
            console.error('Erro ao buscar cursos: ', response.status);
            alert('Não foi possível carregar as disciplinas.');
        }
    } catch (error) {
        console.error('Erro na requisição de cursos: ', error);
        alert('Erro ao carregar disciplinas.');
    }
    

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const createWorkResponse = await fetch('http://localhost:5000/works', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(data)
            });

            if (createWorkResponse.ok) {
                window.location.href = './dashboard.html';
            } else {
                alert('Erro ao publicar o trabalho. Tente novamente.');
            }
        } catch (error) {
            console.error('Erro na criação do trabalho: ', error);
            alert('Erro ao tentar publicar o trabalho.');
        }
    });
});

document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem('access_token');

    const urlParams = new URLSearchParams(window.location.search);
    const workId = urlParams.get('id');
    
    const form = document.getElementById('workForm');
    const titleInput = document.getElementById('title');
    const courseSelect = document.getElementById('course');
    const priceInput = document.getElementById('price');
    const descriptionInput = document.getElementById('description');

    let workCourseName = '';

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

            const selectedOption = Array.from(courseSelect.options).find(option => option.textContent === workCourseName);
            if (selectedOption) {
                selectedOption.selected = true;
            }
        } else {
            console.error('Erro ao buscar cursos: ', response.status);
            alert('Não foi possível carregar as disciplinas.');
        }
    } catch (error) {
        console.error('Erro na requisição de cursos: ', error);
        alert('Erro ao carregar disciplinas.');
    }
    
    try {
        const response = await fetch(`http://localhost:5000/works/${workId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            }
        });
    
        if (response.ok) {
            const work = await response.json();

            titleInput.value = work.title
            workCourseName = work.course;
            priceInput.value = work.price
            descriptionInput.value = work.description

            const selectedOption = Array.from(courseSelect.options).find(option => option.textContent === workCourseName);
            if (selectedOption) {
                selectedOption.selected = true;
            }

        } else {
            console.error('Erro ao buscar informações do trabalho: ', response.status);
            alert('Não foi possível carregar o trabalho.');
        }
    } catch (error) {
        console.error('Erro na requisição do trabalho: ', error);
        alert('Erro ao carregar o trabalho.');
    }

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const createWorkResponse = await fetch(`http://localhost:5000/works/${workId}`, {
                method: 'PUT',
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

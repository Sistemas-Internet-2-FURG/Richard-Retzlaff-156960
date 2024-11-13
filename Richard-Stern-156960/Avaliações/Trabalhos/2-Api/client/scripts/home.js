document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem('access_token');
    
    const worksContainer = document.getElementById('works-container');

    try {
        const response = await fetch('http://localhost:5000/works', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const works = await response.json();

            works.forEach(work => {
                const workCard = document.createElement('div');
                workCard.classList.add('card', 'work-item');
                workCard.setAttribute('data-course', work.course_id);

                workCard.innerHTML = `
                    <h2>${work.title}</h2>
                    <p class="description">${work.description}</p>
                    <p><strong>Disciplina:</strong> ${work.course}</p>
                    <p><strong>Autor:</strong> ${work.author}</p>
                    <p class="price">R$${work.price}</p>
                    <button>Comprar</button>
                `;

                worksContainer.appendChild(workCard);
            });

        } else {
            console.error('Erro ao buscar os works: ', response.status);
            worksContainer.innerHTML = '<p>Não foi possível carregar os trabalhos.</p>';
        }
    } catch (error) {
        console.error('Erro na requisição: ', error);
        worksContainer.innerHTML = '<p>Erro ao carregar os trabalhos.</p>';
    }
});

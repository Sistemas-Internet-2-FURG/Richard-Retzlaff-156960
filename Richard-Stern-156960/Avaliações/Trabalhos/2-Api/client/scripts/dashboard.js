document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem('access_token');

    const worksContainer = document.getElementById('works');

    try {
        const response = await fetch('http://localhost:5000/dashboard', {
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
                workCard.classList.add('card', 'my-card', 'work-item');

                workCard.innerHTML = `
                    <h2>${work.title}</h2>
                    <p><strong>Disciplina:</strong> ${work.course}</p>
                    <p class="price">R$${work.price}</p>
                    <div class="actions">
                        <a href="./work-edit.html?id=${work.id}"><button class="edit-button">Editar</button></a>
                        <button class="delete-button" data-id="${work.id}">Deletar</button>
                    </div>
                `;

                worksContainer.appendChild(workCard);
            });

            // Adicionar o listener para os botões de deletar
            const deleteButtons = document.querySelectorAll('.delete-button');
            deleteButtons.forEach(button => {
                button.addEventListener('click', async function () {
                    const workId = this.getAttribute('data-id');
                    
                    // Confirmar a exclusão
                    const confirmDelete = confirm('Tem certeza que deseja deletar este trabalho?');
                    if (!confirmDelete) {
                        return;
                    }

                    try {
                        const deleteResponse = await fetch(`http://localhost:5000/works/${workId}`, {
                            method: 'DELETE',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${token}`
                            }
                        });

                        if (deleteResponse.ok) {
                            alert('Trabalho deletado com sucesso!');
                            // Remover o card do trabalho deletado
                            this.closest('.work-item').remove();
                        } else if (deleteResponse.status === 403) {
                            alert('Você não tem permissão para deletar este trabalho.');
                        } else {
                            console.error('Erro ao deletar o trabalho:', deleteResponse.status);
                            alert('Erro ao deletar o trabalho. Tente novamente.');
                        }
                    } catch (error) {
                        console.error('Erro na requisição de delete:', error);
                        alert('Erro ao tentar deletar o trabalho. Tente novamente.');
                    }
                });
            });

        } else {
            console.error('Erro ao buscar os trabalhos:', response.status);
            worksContainer.innerHTML = '<p>Não foi possível carregar seus trabalhos.</p>';
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        worksContainer.innerHTML = '<p>Erro ao carregar seus trabalhos.</p>';
    }
});

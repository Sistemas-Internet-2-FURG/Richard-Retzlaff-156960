function loadHeader() {
    const headerContent = `
        <a href="./home.html" class="logo">ComprAI kkkj</a>
        <nav>
            <ul>
                <li><a href="./dashboard.html">Dashboard</a></li>
                <li><a href="./work-create.html"><button>Publicar trabalho</button></a></li>
                <li><button id="logout-button" class="logout-button">Logout</button></li>
            </ul>
        </nav>
    `;

    const header = document.getElementById('main-header');
    header.innerHTML = headerContent;

    const logoutButton = document.getElementById('logout-button');
    logoutButton.addEventListener('click', function () {
        localStorage.removeItem('access_token');
        window.location.href = '../index.html';
    });
}

loadHeader();

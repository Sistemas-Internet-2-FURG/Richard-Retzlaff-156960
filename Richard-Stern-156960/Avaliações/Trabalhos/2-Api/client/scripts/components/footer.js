function loadFooter() {
    const headerContent = `
        <p>Feito com <span style="color: red">❤</span> por Gabriel Endres, Nairo Elsner e Richard Stern</p>
    `;

    const header = document.getElementById('main-footer');
    header.innerHTML = headerContent;
}

loadFooter();

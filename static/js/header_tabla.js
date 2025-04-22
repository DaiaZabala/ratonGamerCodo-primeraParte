document.addEventListener('DOMContentLoaded', function() {
    // Crear el contenido del header dinámicamente
    const headerContent = `
        <header id="header">
            <div>
                <a href="{{url_for('index')}}" id="logo-link" >
                    <img id="logo-header" src="../static/img/logo.jpg" alt="logo">
                </a>
            </div>

            <p id="nombre-web">Ratón Gamer</p>
            <p id="app-admin">App Admin</p>

            <nav class="menu">
                <a id="ingresarUsuarioLink" href="#">Ingresar Usuario</a>
                <a class="hipervinc-header" href="{{ url_for('index') }}">Cerrar sesión</a>
            </nav>
        </header>
    `;

    // Agregar el contenido del encabezado al principio del body
    document.body.insertAdjacentHTML('afterbegin', headerContent);

    // Obtener la URL del logo y asignarla a su href
    const logoLink = document.getElementById('logo-link');
    const logoUrl = logoLink.getAttribute('data-url'); // Obtener la URL generada por Flask
    logoLink.href = logoUrl; // Establecer el enlace del logo

    // Establecer el enlace de 'Ingresar Usuario' con la URL correspondiente
    const ingresarUsuarioLink = document.getElementById('ingresarUsuarioLink');
    ingresarUsuarioLink.href = urls.ingresar_usuario; // Asegúrate de definir 'urls.ingresar_usuario' en tu JS

    // Si tienes otros enlaces o elementos que necesitas manipular, los puedes agregar aquí
});
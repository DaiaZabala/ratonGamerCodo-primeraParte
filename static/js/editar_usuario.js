
    function modificar(event) {
        event.preventDefault(); // Previene recarga

        let id = document.getElementById("id").value;

        let datos = {
            nombre: document.getElementById("nombre").value,
            apellido: document.getElementById("apellido").value,
            nombre_usuario: document.getElementById("nombre_usuario").value,
            correo: document.getElementById("correo").value,
            contrasena: document.getElementById("contrasena").value,
            sexo: document.getElementById("sexo").value,
            pais: document.getElementById("pais").value,
            rol: document.getElementById("rol").value,
            imagen: document.getElementById("imagen").value,
        };

        fetch(`http://localhost:5000/update/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datos)
        })
        .then(res => {
            if (res.ok) {
                alert("Usuario actualizado correctamente");
                window.location.href = "/tabla_usuarios";
            } else {
                throw new Error("Error en la modificación");
            }
        })
        .catch(err => {
            console.error(err);
            alert("No se pudo modificar el usuario");
        });
    }
    
    function modificarRol(event) {
        event.preventDefault();
    
        const id = document.getElementById("id").value;
        const rol = document.getElementById("rol").value;
    
        fetch(`/update/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ rol: rol }),
        })
        .then(response => response.json())
        .then(data => {
            alert("Rol actualizado correctamente");
            console.log(data);
        })
        .catch(error => {
            console.error("Error al actualizar rol:", error);
            alert("Hubo un error al actualizar el rol");
        });
    }

    document.addEventListener("DOMContentLoaded", function() {
        const form = document.querySelector('form.campos-form');
    
        form.addEventListener("submit", function(event) {
            // Validaciones del formulario antes de enviarlo
            let valid = true;
    
            // Verificamos que todos los campos necesarios estén completos
            const nombre = document.getElementById("nombre").value;
            const apellido = document.getElementById("apellido").value;
            const nombre_usuario = document.getElementById("nombre_usuario").value;
            const correo = document.getElementById("correo").value;
    
            if (!nombre || !apellido || !nombre_usuario || !correo) {
                valid = false;
                alert("Todos los campos son necesarios.");
            }
    
            // Si no es válido, evitamos que el formulario se envíe
            if (!valid) {
                event.preventDefault();
            }
        });
    });
    
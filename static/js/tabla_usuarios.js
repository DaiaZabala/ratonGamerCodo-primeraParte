const { createApp } = Vue

  createApp({
    data() {
      return {
        url:"http://127.0.0.1:5000/usuarios", // Retorna todos los registro de la tabla usuarios
        usuarios:[],
        error:false,
        cargando:true
      }
    },
    // Se llama después de que la instancia haya 
    // terminado de procesar todas las opciones relacionadas con el estado.
    created() {
        this.fetchData(this.url)  // Invocando al método
    },
    methods: {
        fetchData(url) {
            // Acá se consume la Api  /usuarios
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.usuarios = data;
                    this.cargando=false
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                });
        },
        // el id se necesita para buscar en la DB y eliminarlo
        eliminar(id) {

            const url = 'https://localhost:5000/borrar/${id}';
            const options = {
              method: 'DELETE'
            };
            fetch(url, options)
              .then(res => res.json()) // Si devolvés JSON en Flask
              .then(res => {
                alert("Usuario eliminado correctamente");
                this.usuarios = this.usuarios.filter(u => u.id !== id); // Actualiza sin recargar
              })
              .catch(err => {
                console.error(err);
                alert("Error al eliminar el usuario");
              });
          }
        }
    
      }).mount('#app')
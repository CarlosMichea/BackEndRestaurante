// ============================================================================
// JavaScript propio y mínimo para "Sabores del Chef" (sin librerías externas)
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Cerrar automáticamente las alertas flash (messages) después de 4 segundos
    const alertasAutoCerrar = document.querySelectorAll('.alerta-autocierre');
    alertasAutoCerrar.forEach((alerta) => {
        setTimeout(() => {
            if (window.bootstrap && window.bootstrap.Alert) {
                const instancia = window.bootstrap.Alert.getOrCreateInstance(alerta);
                instancia.close();
            } else {
                alerta.remove();
            }
        }, 4000);
    });

    // 2. Formatear precios en pesos chilenos: "$ 8.900"
    const formateadorCLP = new Intl.NumberFormat('es-CL');
    document.querySelectorAll('[data-precio-clp]').forEach((elemento) => {
        const valorNumerico = Number(elemento.dataset.precioClp);
        if (!Number.isNaN(valorNumerico)) {
            elemento.textContent = `$ ${formateadorCLP.format(valorNumerico)}`;
        }
    });

    // 3. Modal de confirmación para eliminar plato enviando POST con csrf_token
    const modalElemento = document.getElementById('modalEliminarPlato');
    if (modalElemento && window.bootstrap && window.bootstrap.Modal) {
        const modalBootstrap = new window.bootstrap.Modal(modalElemento);
        const spanNombre = document.getElementById('modalNombrePlato');
        const formularioEliminar = document.getElementById('formEliminarPlato');

        document.querySelectorAll('.btn-abrir-modal-eliminar').forEach((boton) => {
            boton.addEventListener('click', (evento) => {
                // Evitamos ir a eliminar_confirmar.html cuando JS está activo
                evento.preventDefault();
                const urlEliminar = boton.dataset.eliminarUrl;
                const nombrePlato = boton.dataset.platoNombre;

                if (spanNombre) {
                    spanNombre.textContent = nombrePlato || 'este plato';
                }
                if (formularioEliminar && urlEliminar) {
                    formularioEliminar.setAttribute('action', urlEliminar);
                }
                modalBootstrap.show();
            });
        });
    }
});

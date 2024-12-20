let get_price_from_articulo_option = node => {
    let option_selected = node.selectedOptions[0].textContent;
    let precio_minorista = option_selected.split("|")[3].trim().slice(5);
    let precio_mayorista = option_selected.split("|")[4].trim().slice(5);

    return precio_mayorista, precio_minorista
}

let select_to_articulo_venta = (node, text=null) => {
    let option_selected = '';
    if(text) {
        option_selected = text;
    } else {
        option_selected = node.selectedOptions[0].textContent;
    }
    let row = option_selected.split("|")
    if(row.length >= 5 ){
        return {
            codigo: row[0].trim(),
            codigo_interno: row[1].trim(),
            nombre: row[2].trim(),
            precio_minorista: row[3].trim().slice(5),
            precio_mayorista: row[4].trim().slice(5),
            umbral: row[5].trim().slice(7)
        };
    } else {
        return null
    }
};

const update_precio_total = () => {
    const precio_total_element = document.querySelector("div.readonly");
    const precio_total = calcular_precio_total();
    precio_total_element.innerHTML = `<br><p class="text-blue text-bold">${precio_total.toFixed(2)}</p>`;

}
const calcular_precio_total = ()=> {
   return Array.from(document.querySelectorAll('.field-precio_total p')).slice(1).reduce(
    (acumulador, elemento)=>{
        if(elemento.class == ['text-blue', 'text-bold']){
            return acumulador
        }
        const valor = parseFloat(elemento.textContent);
        return acumulador + (isNaN(valor)? 0 : valor)
    }, 0
   );
    
};

const get_indice = (select_id, select_name='-articulo') => {
    if (!select_id) {
        console.error('select_id es undefined o null');
        return null;
    }

    // Si el select_id viene de select2, intentar obtener el ID real
    if (select_id.startsWith('select2-')) {
        const element = document.querySelector(`[data-select2-id="${select_id}"]`);
        if (element) {
            select_id = element.id;
        }
    }

    // Intentar diferentes patrones de extracción
    const patterns = [
        /id_ventas-(\d+)-articulo/,
        /ventas-(\d+)/,
        /\d+/
    ];

    for (let pattern of patterns) {
        const match = select_id.match(pattern);
        if (match) {
            return match[1];
        }
    }

    console.error('No se pudo extraer el índice de:', select_id);
    return null;
};


let get_price_node = indice => {
    return document.querySelector('#id_ventas-'+indice+'-precio');
}

let get_cantidad_node = indice => {
    return document.querySelector('#id_ventas-'+indice+'-cantidad');    
}
// }


document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("select[id^='id_ventas']").forEach(item => {
        item.onchange = function() {
            let select_id = this.dataset['select2Id'] || '0';
            console.log("select_id:", select_id);

            let indice = get_indice(select_id);
            if (!indice) {
                console.error("Element not found for indice:", indice);
                return;
            }

            let cantidadNode = document.querySelector(`#id_ventas-${indice}-cantidad`);
            let price_node = get_price_node(indice);

            if (!cantidadNode || !price_node) {
                console.error("Element not found for indice:", indice);
                return;
            }

            // Simula un evento de cambio en el campo de cantidad
            cantidadNode.dispatchEvent(new Event('change'));

            let cantidad = cantidadNode.value;
            let articulo_venta = select_to_articulo_venta(item);
            let total = document.querySelector(`tr#ventas-${indice} td.field-precio_total`);

            if (articulo_venta) {
                console.log("Artículo seleccionado:", articulo_venta.nombre);
                if (cantidad > articulo_venta.umbral) {
                    price_node.setAttribute("value", articulo_venta.precio_mayorista);
                    total.innerHTML = "<p style='color:blue'>" + String(parseFloat(cantidad) * parseFloat(price_node.value)) + "</p>";
                } else {
                    price_node.setAttribute("value", articulo_venta.precio_minorista);
                    total.innerHTML = "<p style='color:blue'>" + String(parseFloat(cantidad) * parseFloat(articulo_venta.precio_minorista)) + "</p>";
                }
            }
            update_precio_total();
        }
    });
    
    function manejarPrecio(fila){
        let cantidad = parseFloat(fila.querySelector('input[id$="-cantidad"]').value) || 0;
        let precio_node = fila.querySelector('input[id$="-precio"]');
        let precio = parseFloat(precio_node.value) || 0;
        let total = cantidad*precio;
        fila.querySelector('.field-precio_total p').textContent = total.toFixed(2);
    }

    function manejarCantidad(fila){
        actualizarTotalFila(fila)
        update_precio_total();
    }

    function actualizarTotalFila(fila) {
        try {
            const cantidadInput = fila.querySelector('input[id$="-cantidad"]');
            const precioInput = fila.querySelector('input[id$="-precio"]');
            const selectArticulo = fila.querySelector("select[id^='id_ventas-'][id$='-articulo']");
            const totalElement = fila.querySelector('.field-precio_total p');

            if (!cantidadInput || !precioInput || !selectArticulo || !totalElement) {
                console.error('Elementos faltantes en la fila:', fila.id);
                return;
            }

            const cantidad = parseFloat(cantidadInput.value) || 0;
            const articuloVenta = select_to_articulo_venta(selectArticulo);

            if (!articuloVenta) {
                console.warn('No hay artículo seleccionado en la fila:', fila.id);
                totalElement.textContent = '0.00';
                return;
            }

            const precio = cantidad > articuloVenta.umbral 
                ? parseFloat(articuloVenta.precio_mayorista) 
                : parseFloat(articuloVenta.precio_minorista);

            precioInput.value = precio.toFixed(2);
            const total = cantidad * precio;
            totalElement.textContent = total.toFixed(2);

        } catch (error) {
            console.error('Error al actualizar total de fila:', error);
            console.error('Fila:', fila);
        }
    }

    function agregarEventosANuevoInline(nuevoInline) {
        let selectArticulo = nuevoInline.querySelector("select[id^='id_ventas-'][id$='-articulo']");
        let inputCantidad = nuevoInline.querySelector("input[id$='-cantidad']");
        let inputPrecio = nuevoInline.querySelector("input[id$='-precio']");

        selectArticulo.addEventListener('change', manejarCambioArticulo);
        inputCantidad.addEventListener('change', manejarCambioCantidad);
        inputPrecio.addEventListener('change', manejarCambioPrecio);
    }

    
    function actualizarTotalGlobal() {
        let sumTotal = Array.from(document.querySelectorAll('.field-precio_total p'))
            .reduce((acc, el) => acc + parseFloat(el.textContent || 0), 0);
        let total_p = document.querySelector('div.readonly');
        if (total_p) {
            total_p.innerHTML= `<br><strong> ${sumTotal.toFixed(2)}</strong>` ;
        }
    }

    function manejarCambioArticulo(event) {
        let select = event.params.data.element; 
        let fila = select.closest('tr');
        let articuloVenta = select_to_articulo_venta(select);
        let cantidad = parseFloat(fila.querySelector('input[id$="-cantidad"]').value) || 0;
        let precioNode = fila.querySelector('input[id$="-precio"]');
        let precio = cantidad > articuloVenta.umbral ? articuloVenta.precio_mayorista : articuloVenta.precio_minorista;
        precioNode.value = precio;
        precioNode.innerHTML = "<p style='color:blue'>" + precio + "</p>";
        actualizarTotalFila(fila);
        update_precio_total();

    }

    function manejarCambioPrecio(event) {
        let input = event.target;
        let fila = input.closest('tr');
        manejarPrecio(fila);
        update_precio_total();

    }

    function manejarCambioCantidad(event){
        let input = event.target;
        let fila = input.closest('tr');
        manejarCantidad(fila);
        update_precio_total();

    }

    function manejarEliminacionArticulo(event) {
        let fila = event.target.closest('tr');
        if (fila) {
            
            
            // Marcar el formulario para eliminación
            let deleteInput = fila.querySelector('input[name$="-DELETE"]');
            fila.querySelectorAll('input, select').forEach(element => {
                element.removeAttribute('required');
                    element.classList.remove('is-invalid');
                });
            if (deleteInput) {
                deleteInput.checked = true;
            }
            fila.style.display = 'none'; // Ocultar la fila en lugar de eliminarla
            // fila.remove();
            update_precio_total();
        }
    }

    // Add event listeners for delete buttons
    document.querySelectorAll('.delete-button-class').forEach(button => {
        button.addEventListener('click', manejarEliminacionArticulo);
    });
    document.querySelectorAll('.delete-inline-row').forEach(icon => {
        icon.addEventListener('click', manejarEliminacionArticulo);
    });

    // Agregar eventos a todos los elementos existentes y actualizar totales
    document.querySelectorAll('tr[id^="ventas-"]').forEach(fila => {
        agregarEventosANuevoInline(fila);
        manejarPrecio(fila);
        // actualizarTotalFila(fila);
    });
    actualizarTotalGlobal();

    // Observa cambios en el grupo de inlines para agregar eventos a nuevos inlines
    const observer = new MutationObserver(function
        (mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.classList && node.classList.contains('dynamic-ventas')) {
                        agregarEventosANuevoInline(node);
                        actualizarTotalFila(node);
                        let deleteButton = node.querySelector('.delete-button-class');
                        if (deleteButton) {
                            deleteButton.addEventListener('click', manejarEliminacionArticulo);
                        }
                        document.querySelectorAll("select[id^='id_ventas']").forEach(
                            item => {
                                item.onchange = function(){
                                    let select_id = this.dataset['select2Id'];
                                    let indice = get_indice(select_id);
                                    let cantidad = document.querySelector(`#id_ventas-${indice}-cantidad`).value;
                                    let price_node = get_price_node(indice);
                    
                                    let articulo_venta = select_to_articulo_venta(item);
                                    let total = document.querySelector(`tr#ventas-${indice} td.field-precio_total`)
                    
                                    if(cantidad > articulo_venta.umbral) {
                                        price_node.setAttribute("value", articulo_venta.precio_mayorista)
                                        ;
                                        total.innerHTML =  "<p style='color:blue'>" + String(parseFloat(cantidad)*parseFloat(articulo_venta.precio_mayorista)) + "</p>";
                                    } else {
                                        price_node.setAttribute("value", articulo_venta.precio_minorista);
                                        total.innerHTML = "<p style='color:blue'>" + String(parseFloat(cantidad)*parseFloat(articulo_venta.precio_minorista)) + "</p>";
                                    }
                                    update_precio_total();
                                
                                }
                            }
                        );
                    }   
                });
            }
        });
    });

    const inlineGroup = document.querySelector('.inline-group');
    if (inlineGroup) {
        observer.observe(inlineGroup, {
            childList: true,
            subtree: true
        });
    }

    function validarFormulario() {
        console.log('Iniciando validación...');
        
        // 1. Identificar filas que realmente necesitan validación
        const filasRelevantes = Array.from(document.querySelectorAll('tr[id^="ventas-"]'))
            .filter(fila => {
                // Ignorar fila template y filas marcadas para eliminar
                if (fila.id === 'ventas-empty' || fila.id.includes('__prefix__')) return false;
                const deleteInput = fila.querySelector('input[name$="-DELETE"]');
                if (deleteInput?.checked) return false;

                // Solo validar filas que tengan un artículo seleccionado
                const articulo = fila.querySelector('select[id$="-articulo"]')?.value;
                return Boolean(articulo);
            });

        console.log(`Filas a validar: ${filasRelevantes.length}`);

        let errores = [];
        let filasConError = new Set();

        // 2. Validar cada fila relevante
        filasRelevantes.forEach(fila => {
            const filaId = fila.id;
            const indice = filaId.match(/\d+/)[0];
            
            // Obtener elementos
            const selectArticulo = fila.querySelector('select[id$="-articulo"]');
            const precioInput = fila.querySelector('input[id$="-precio"]');

            // Limpiar clases de error previas
            [selectArticulo, precioInput].forEach(elem => {
                if (elem) elem.classList.remove('is-invalid');
            });

            // Validar artículo (principal validación)
            if (!selectArticulo?.value) {
                selectArticulo.classList.add('is-invalid');
                errores.push(`Fila ${indice}: Debe seleccionar un artículo`);
                filasConError.add(filaId);
            }

            // Validar precio solo si hay artículo seleccionado
            if (selectArticulo?.value && precioInput) {
                const precio = parseFloat(precioInput.value);
                if (isNaN(precio) || precio <= 0) {
                    precioInput.classList.add('is-invalid');
                    errores.push(`Fila ${indice}: Precio debe ser mayor a 0`);
                    filasConError.add(filaId);
                }
            }
        });

        // 3. Mostrar resultados
        if (errores.length > 0) {
            console.log('Errores encontrados:', errores);
            mostrarErrores(errores);
            return false;
        }

        // 4. Validar que haya al menos una fila válida
        if (filasRelevantes.length === 0) {
            mostrarErrores(['Debe seleccionar al menos un artículo']);
            return false;
        }

        console.log('Validación exitosa');
        return true;
    }

    function mostrarErrores(errores) {
        // Crear mensaje de error
        const mensajeError = document.createElement('div');
        mensajeError.className = 'alert alert-danger alert-dismissible fade show';
        mensajeError.innerHTML = `
            <h4>Por favor corrija los siguientes errores:</h4>
            <ul>
                ${errores.map(error => `<li>${error}</li>`).join('')}
            </ul>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insertar mensaje en el DOM
        const form = document.querySelector('form');
        const existingAlert = form.querySelector('.alert');
        if (existingAlert) {
            existingAlert.remove();
        }
        form.insertBefore(mensajeError, form.firstChild);

        // Scroll al primer error
        const primerElementoConError = document.querySelector('.is-invalid');
        if (primerElementoConError) {
            primerElementoConError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    function limpiarFilasVacias() {
        document.querySelectorAll('tr[id^="ventas-"]').forEach(fila => {
            if (fila.id === 'ventas-empty' || fila.id.includes('__prefix__')) return;

            const articulo = fila.querySelector('select[id$="-articulo"]')?.value;
            
            // Si no hay artículo seleccionado, marcar para eliminar
            if (!articulo) {
                const deleteInput = fila.querySelector('input[name$="-DELETE"]');
                if (deleteInput) {
                    deleteInput.checked = true;
                    fila.style.opacity = '0.5';
                }
            }
        });
    }

    // Validación en tiempo real solo para artículos y precios
    document.addEventListener('DOMContentLoaded', () => {
        document.addEventListener('change', (e) => {
            const target = e.target;
            
            // Solo validar cambios en selects de artículos y campos de precio
            if (target.matches('select[id$="-articulo"], input[id$="-precio"]')) {
                const fila = target.closest('tr');
                if (fila) {
                    validarFila(fila);
                }
            }
        });
    });

    function validarFila(fila) {
        const selectArticulo = fila.querySelector('select[id$="-articulo"]');
        const precioInput = fila.querySelector('input[id$="-precio"]');

        // Limpiar errores previos
        [selectArticulo, precioInput].forEach(elem => {
            if (elem) elem.classList.remove('is-invalid');
        });

        // Solo validar si hay artículo seleccionado
        if (selectArticulo?.value) {
            if (precioInput) {
                const precio = parseFloat(precioInput.value);
                if (isNaN(precio) || precio <= 0) {
                    precioInput.classList.add('is-invalid');
                }
            }
        }
    }

    // Modificar el evento de guardar
    document.querySelector('#guardar-venta').addEventListener('click', function(e) {
        e.preventDefault();
        limpiarFilasVacias();
        if (validarFormulario()) {
            this.closest('form').submit();
        }
    });

    function handleSelectionChange(event) {
        // Obtener el ID correcto independientemente del origen del evento
        const select_id = this.id || this.dataset.select2Id || event?.target?.id;
        console.log('Manejando cambio de selección:', { select_id, eventType: event?.type });

        const indice = get_indice(select_id);
        if (!indice) {
            console.error('No se pudo obtener el índice para:', select_id);
            return;
        }

        const fila = document.querySelector(`tr#ventas-${indice}`);
        if (!fila) {
            console.error('No se encontró la fila para el índice:', indice);
            return;
        }

        actualizarTotalFila(fila);
        update_precio_total();
    }

    document.querySelectorAll("select[id^='id_ventas']").forEach(item => {
        item.onchange = handleSelectionChange;
        item.onclick = handleSelectionChange; // Si necesitas que el click también lo maneje
    });

    function intentarCorregirDatos(filasInvalidas) {
        let correcciones = [];
        let correccionesRealizadas = false;

        filasInvalidas.forEach(filaInfo => {
            const fila = document.querySelector(`#${filaInfo.id}`);
            if (!fila) return;

            const cantidadInput = fila.querySelector('input[id$="-cantidad"]');
            const selectArticulo = fila.querySelector('select[id$="-articulo"]');
            const precioInput = fila.querySelector('input[id$="-precio"]');
            const deleteInput = fila.querySelector('input[name$="-DELETE"]');

            // Caso 1: Fila completamente vacía
            if (!selectArticulo?.value && (!cantidadInput?.value || cantidadInput.value === '1')) {
                if (deleteInput) {
                    deleteInput.checked = true;
                    correcciones.push(`Fila ${filaInfo.id}: Marcada para eliminación por estar vacía`);
                    correccionesRealizadas = true;
                }
                return;
            }

            // Caso 2: Cantidad inválida
            if (cantidadInput && (isNaN(cantidadInput.value) || parseFloat(cantidadInput.value) <= 0)) {
                cantidadInput.value = '1';
                correcciones.push(`Fila ${filaInfo.id}: Cantidad corregida a 1`);
                correccionesRealizadas = true;
            }

            // Caso 3: Precio faltante pero artículo seleccionado
            if (selectArticulo?.value && (!precioInput?.value || parseFloat(precioInput.value) <= 0)) {
                const articuloVenta = select_to_articulo_venta(selectArticulo);
                if (articuloVenta) {
                    const cantidad = parseFloat(cantidadInput?.value) || 1;
                    const precio = cantidad > articuloVenta.umbral 
                        ? articuloVenta.precio_mayorista 
                        : articuloVenta.precio_minorista;
                    
                    precioInput.value = precio.toFixed(2);
                    correcciones.push(`Fila ${filaInfo.id}: Precio actualizado a ${precio.toFixed(2)}`);
                    correccionesRealizadas = true;
                }
            }
        });

        if (correccionesRealizadas) {
            mostrarModalCorrecciones(correcciones);
            return true;
        }

        return false;
    }

    function mostrarModalCorrecciones(correcciones) {
        // Crear modal si no existe
        let modal = document.getElementById('correccionesModal');
        if (!modal) {
            modal = document.createElement('div');
            modal.innerHTML = `
                <div class="modal fade" id="correccionesModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Correcciones Automáticas</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div id="listaCorrecciones"></div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                <button type="button" class="btn btn-primary" id="aceptarCorrecciones">Aceptar y Continuar</button>
                            </div>
                        </div>
                    </div>
                </div>`;
            document.body.appendChild(modal);
        }

        // Actualizar contenido
        const listaCorrecciones = document.getElementById('listaCorrecciones');
        listaCorrecciones.innerHTML = `
            <p>Se realizaron las siguientes correcciones:</p>
            <ul>
                ${correcciones.map(correccion => `<li>${correccion}</li>`).join('')}
            </ul>
            <p>¿Desea continuar con estas correcciones?</p>
        `;

        // Configurar botón de aceptar
        const btnAceptar = document.getElementById('aceptarCorrecciones');
        btnAceptar.onclick = function() {
            const modal = bootstrap.Modal.getInstance(document.getElementById('correccionesModal'));
            modal.hide();
            document.querySelector('form').submit();
        };

        // Mostrar modal
        const modalInstance = new bootstrap.Modal(document.getElementById('correccionesModal'));
        modalInstance.show();
    }

    // Asegurarse de que Bootstrap está disponible
    document.addEventListener('DOMContentLoaded', () => {
        if (typeof bootstrap === 'undefined') {
            console.warn('Bootstrap no está cargado. El modal no funcionará correctamente.');
        }
    });
});
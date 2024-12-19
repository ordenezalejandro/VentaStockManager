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
    // Verificar si select_id está definido
    if (select_id) {
        // Intentar extraer el índice usando el formato esperado
        if (select_id.length > 'id_ventas-'.length + select_name.length) {
            return select_id.slice('id_ventas-'.length, -`${select_name}`.length);
        }
        
        // Intentar extraer el índice usando una expresión regular como alternativa
        const regex = /id_ventas-(\d+)-articulo/;
        const match = select_id.match(regex);
        if (match) {
            return match[1]; // Retornar el índice encontrado
        }
    }
    
    console.error("Invalid select_id:", select_id);
    return null; // Retornar null si el select_id es inválido
}


let get_price_node = indice => {
    return document.querySelector('#id_ventas-' + indice + '-precio');
}

let get_cantidad_node = indice => {
    return document.querySelector('#id_ventas-' + indice + '-cantidad');
}
// }


document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("select[id^='id_ventas']").forEach(
        item => {
            item.onchange = function() {
                let select_id = this.dataset['select2Id'];
                let indice = get_indice(select_id);
                let cantidadNode = document.querySelector(`#id_ventas-${indice}-cantidad`);
                let price_node = get_price_node(indice);
                let total = document.querySelector(`tr#ventas-${indice} td.field-precio_total`);

                try {
                    // Verificar si cantidadNode existe
                    if (!cantidadNode) {
                        throw new Error(`Cantidad input not found for indice: ${indice}`);
                    }

                    let cantidad = cantidadNode.value;
                    let articulo_venta = select_to_articulo_venta(item);

                    // Lógica para establecer precios y actualizar totales
                    if (articulo_venta) {
                        if (cantidad > articulo_venta.umbral) {
                            price_node.setAttribute("value", articulo_venta.precio_mayorista);
                            total.innerHTML = "<p style='color:blue'>" + String(parseFloat(cantidad) * parseFloat(articulo_venta.precio_mayorista)) + "</p>";
                        } else {
                            price_node.setAttribute("value", articulo_venta.precio_minorista);
                            total.innerHTML = "<p style='color:blue'>" + String(parseFloat(cantidad) * parseFloat(articulo_venta.precio_minorista)) + "</p>";
                        }
                    } else {
                        console.error("Invalid articulo_venta:", articulo_venta);
                    }

                    update_precio_total();
                } catch (error) {
                    console.error(error.message);
                }
            }
        }
    );
    
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
        let cantidad = parseFloat(fila.querySelector('input[id$="-cantidad"]').value) || 0;
        let precio_node = fila.querySelector('input[id$="-precio"]');
        let precio = parseFloat(precio_node.value) || 0;
        let selectArticulo = fila.querySelector("select[id^='id_ventas-'][id$='-articulo']");
        let articuloVenta = select_to_articulo_venta(selectArticulo);
        if (articuloVenta === null){
            return;
        }
        let umbral = articuloVenta.umbral;
        let precio_value = cantidad > umbral ? articuloVenta.precio_mayorista : articuloVenta.precio_minorista;
        precio_node.value = precio_value;
        let total = cantidad*precio_value;
        fila.querySelector('.field-precio_total p').textContent =  total.toFixed(2) ;
        // let total = cantidad * precio;
        // fila.querySelector('.field-precio_total p').textContent = total.toFixed(2);
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
        
        // Verificar si articuloVenta es válido
        if (!articuloVenta) {
            console.error("Invalid articuloVenta:", articuloVenta);
            return; // Salir si el artículo no es válido
        }

        let cantidad = parseFloat(fila.querySelector('input[id$="-cantidad"]').value) || 0;
        let precioNode = fila.querySelector('input[id$="-precio"]');
        
        // Asignar el precio correcto basado en la cantidad y el umbral
        let precio;
        if (cantidad > articuloVenta.umbral) {
            precio = parseFloat(articuloVenta.precio_mayorista);
        } else {
            precio = parseFloat(articuloVenta.precio_minorista);
        }

        // Verificar que el precio se haya establecido correctamente
        if (isNaN(precio)) {
            console.error("Invalid price calculated:", precio);
            return; // Salir si el precio es inválido
        }

        // Establecer el precio en el nodo correspondiente
        precioNode.value = precio; // Asegúrate de que esto esté configurando el valor correctamente
        precioNode.innerHTML = "<p style='color:blue'>" + precio.toFixed(2) + "</p>"; // Mostrar el precio en el formato correcto

        // Actualizar el total de la fila
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
                                item.onchange = function() {
                                    let select_id = this.dataset['select2Id'];
                                    let indice = get_indice(select_id);
                                    
                                    // Check if the cantidad input exists before accessing its value
                                    let cantidadNode = document.querySelector(`#id_ventas-${indice}-cantidad`);
                                    if (!cantidadNode) {
                                        console.error(`Cantidad input not found for indice: ${indice}`);
                                        return; // Exit the function if the input does not exist
                                    }
                                    
                                    let cantidad = cantidadNode.value;
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
});
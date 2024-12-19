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
    // Manejar el evento onchange para cada select de artículo
    document.querySelectorAll("select[id^='id_ventas-'][id$='-articulo']").forEach(item => {
        item.onchange = function() {
            let select_id = this.id; // Obtener el ID del select
            let indice = select_id.split('-')[1]; // Extraer el índice
            let cantidadNode = document.querySelector(`#id_ventas-${indice}-cantidad`);
            let price_node = document.querySelector(`#id_ventas-${indice}-precio`);
            let totalNode = document.querySelector(`#ventas-${indice} .field-precio_total p`);

            // Verificar si cantidadNode existe
            if (!cantidadNode) {
                console.error(`Cantidad input not found for indice: ${indice}`);
                return; // Salir si el input no existe
            }

            let cantidad = parseFloat(cantidadNode.value) || 0; // Asegurarse de que sea un número
            let articulo_venta = select_to_articulo_venta(this); // Obtener el artículo seleccionado

            // Verificar si articulo_venta es válido
            if (!articulo_venta) {
                console.error("Invalid articulo_venta:", articulo_venta);
                return; // Salir si el artículo no es válido
            }

            // Lógica para establecer precios y actualizar totales
            let precio;
            if (cantidad > articulo_venta.umbral) {
                precio = parseFloat(articulo_venta.precio_mayorista);
            } else {
                precio = parseFloat(articulo_venta.precio_minorista);
            }

            // Verificar que el precio se haya establecido correctamente
            if (isNaN(precio)) {
                console.error("Invalid price calculated:", precio);
                return; // Salir si el precio es inválido
            }

            // Establecer el precio en el nodo correspondiente
            price_node.value = precio.toFixed(2); // Asegúrate de que esto esté configurando el valor correctamente
            totalNode.textContent = (cantidad * precio).toFixed(2); // Actualizar el total

            // Actualizar el precio total global
            update_precio_total();
        }
    });

    // Manejar el evento input para la cantidad
    document.querySelectorAll("input[id^='id_ventas-'][id$='-cantidad']").forEach(item => {
        item.oninput = function() {
            let cantidadNode = this; // Obtener el input de cantidad
            let select_id = this.id.replace('-cantidad', '-articulo'); // Obtener el ID del select correspondiente
            let articuloSelect = document.querySelector(`#${select_id}`);
            let indice = select_id.split('-')[1]; // Extraer el índice
            let price_node = document.querySelector(`#id_ventas-${indice}-precio`);
            let totalNode = document.querySelector(`#ventas-${indice} .field-precio_total p`);

            // Verificar si el select de artículo existe
            if (!articuloSelect) {
                console.error(`Articulo select not found for indice: ${indice}`);
                return; // Salir si el select no existe
            }

            let cantidad = parseFloat(cantidadNode.value) || 0; // Asegurarse de que sea un número
            let articulo_venta = select_to_articulo_venta(articuloSelect); // Obtener el artículo seleccionado

            // Verificar si articulo_venta es válido
            if (!articulo_venta) {
                console.error("Invalid articulo_venta:", articulo_venta);
                return; // Salir si el artículo no es válido
            }

            // Lógica para establecer precios y actualizar totales
            let precio;
            if (cantidad > articulo_venta.umbral) {
                precio = parseFloat(articulo_venta.precio_mayorista);
            } else {
                precio = parseFloat(articulo_venta.precio_minorista);
            }

            // Verificar que el precio se haya establecido correctamente
            if (isNaN(precio)) {
                console.error("Invalid price calculated:", precio);
                return; // Salir si el precio es inválido
            }

            // Establecer el precio en el nodo correspondiente
            price_node.value = precio.toFixed(2); // Asegúrate de que esto esté configurando el valor correctamente
            totalNode.textContent = (cantidad * precio).toFixed(2); // Actualizar el total

            // Actualizar el precio total global
            update_precio_total();
        }
    });

    // Función para actualizar el precio total global
    const update_precio_total = () => {
        const precio_total_element = document.querySelector("div.readonly");
        const precio_total = calcular_precio_total();
        precio_total_element.innerHTML = `<br><p class="text-blue text-bold">${precio_total.toFixed(2)}</p>`;
    };

    // Función para calcular el precio total
    const calcular_precio_total = () => {
        return Array.from(document.querySelectorAll('.field-precio_total p')).reduce(
            (acumulador, elemento) => {
                const valor = parseFloat(elemento.textContent) || 0; // Asegurarse de que sea un número
                return acumulador + valor;
            }, 0
        );
    };

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

            // Lógica para establecer precios y actualizar totales
            let precio;
            if (cantidad > articulo_venta.umbral) {
                precio = parseFloat(articulo_venta.precio_mayorista);
            } else {
                precio = parseFloat(articulo_venta.precio_minorista);
            }

            // Verificar que el precio se haya establecido correctamente
            if (isNaN(precio)) {
                console.error("Invalid price calculated:", precio);
                return; // Salir si el precio es inválido
            }

            // Establecer el precio en el nodo correspondiente
            price_node.value = precio.toFixed(2); // Asegúrate de que esto esté configurando el valor correctamente
            totalNode.textContent = (cantidad * precio).toFixed(2); // Actualizar el total

            // Actualizar el precio total global
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

    const inlineGroup = document.querySelector('.inline-group');
    if (inlineGroup) {
        observer.observe(inlineGroup, {
            childList: true,
            subtree: true
        });
    }
});
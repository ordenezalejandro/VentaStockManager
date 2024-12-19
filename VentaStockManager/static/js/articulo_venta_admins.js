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

    const inlineGroup = document.querySelector('.inline-group');
    if (inlineGroup) {
        observer.observe(inlineGroup, {
            childList: true,
            subtree: true
        });
    }
});
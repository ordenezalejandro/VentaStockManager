
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
    const result = {
        codigo: row[0].trim(),
        codigo_interno: row[1].trim(),
        nombre: row[2].trim(),
        precio_minorista: row[3].trim(),
        precio_mayorista: row[4].trim(),
        umbral:4
    };
    return result;
};

const get_indice = (select_id, select_name='-articulo') => {
    return select_id.slice('id_venta--'.length, -'-articulo'.length)
};

let get_price_node = indice => {
    
    return document.querySelector('#id_ventas-'+indice+'-precio');
    
}

document.addEventListener("DOMContentLoaded",
    function(event) {
        document.querySelectorAll("input[name^='ventas-']").forEach(
            item =>{
                item.addEventListener("change", event =>{
                let quantity = event.target.parentElement.parentElement.querySelector('input[id$=cantidad]').value;
                let price = event.target.parentElement.parentElement.querySelector('input[id$=precio_minorista]').value;
                let total = parseFloat(price*quantity);
                event.target.parentElement.parentElement.querySelector('[class$=total]').querySelector('p').textContent = total;

                let sum_total = [...document.querySelectorAll('[class="field-total"] p')].reduce((a, b) => a + parseFloat(b.textContent), 0.0);
                let total_p = document.querySelector('div [class="readonly"]');
                total_p.textContent = sum_total;
                }
             );
            }
        );

        document.querySelectorAll("select[id^='id_ventas']").forEach(
            item => {
                item.onchange = function(){
                    console.log(item);
                    let select_id = this.dataset['select2Id'];
                    let indice = get_indice(select_id);
                    let cantidad = document.querySelector(`#id_ventas-${indice}-cantidad`).value;
                    let price_node = get_price_node(indice);

                    let articulo_venta = select_to_articulo_venta(item);
                    let total = document.querySelector(`tr#venta-${indice} td.field-precio_toal`)

                    if(cantidad > articulo_venta.umbral) {
                        price_node.setAttribute("value", articulo_venta.precio_mayorista);
                        total.setAttribute('innerText', "<p style='color:blue'>" + String(parseFloat(cantidad)*parserFloat(articulo_venta.precio_mayorista)) + "</p>");
                    } else {
                        price_node.setAttribute("value", articulo_venta.precio_minorista);
                        total.setAttribute('innerText', "<p style='color:blue'>" + String(parseFloat(cantidad)*parserFloat(articulo_venta.precio_minorista)) + "</p>");
                    }

                
                }
            }
        );
        document.querySelectorAll("input[id$='cantidad']").forEach(
            item => {
                item.onchange = function(){
                    console.log(item);
                    let indice = get_indice(item.id, "-cantidad");
                    let cantidad = item.value;
                    let price_node = get_price_node(indice);
                    let select_articulo_venta = document.querySelector(`#id_ventas-${indice}-articulo`);
                    let articulo_venta = null;
                    if (! select_articulo_venta || select_articulo_venta.textContent === '\n'){
                        return null;
                    } else {
                        articulo_venta = select_to_articulo_venta(null, text=select_articulo_venta.textContent);
                    }
                    let total = document.querySelector(`tr#venta-${indice} td.field-precio_toal`)
                
                    if(cantidad > articulo_venta.umbral) {
                        price_node.setAttribute("value", articulo_venta.precio_mayorista);
                        total.setAttribute('innerText', "<p style='color:blue'>" + String(parseFloat(cantidad)*parserFloat(articulo_venta.precio_mayorista)) + "</p>");
                    } else {
                        price_node.setAttribute("value", articulo_venta.precio_minorista);
                        total.setAttribute('innerText', "<p style='color:blue'>" + String(parseFloat(cantidad)*parserFloat(articulo_venta.precio_minorista)) + "</p>");
                    }
                
                }
            }
        );
    }
);

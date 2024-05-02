
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
        precio_minorista: row[3].trim().slice(5),
        precio_mayorista: row[4].trim().slice(5),
        umbral:4
    };
    return result;
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
    return select_id.slice('id_ventas-'.length, -`${select_name}`.length)
};

let get_price_node = indice => {
    return document.querySelector('#id_ventas-'+indice+'-precio');
}

let get_cantidad_node = indice => {
    return document.querySelector('#id_ventas-'+indice+'-cantidad');    
}

document.addEventListener("DOMContentLoaded",

    function(event) {
        const init = (event) => {
            // event.preventDefault();        
            document.querySelectorAll('tr[id^=ventas-]').forEach(item=>{
                let precio_total = 0;
                let precio_total_node = item.querySelector('.field-precio_total');
                try {
                    let cantidad = parseFloat(item.querySelector('[id$=cantidad]').value);
                    let precio = parseFloat(item.querySelector('[id$=precio]').value);
                    let result = (cantidad*precio).toFixed(2)
                    precio_total = isNaN(result) ? 0.00: result;
                } catch (error) {
                    precio_total = 0.00;   
                }
                precio_total_node.innerHTML =  "<p class='color:blue'>" + precio_total + "</p>";
            });
            update_precio_total();
        };

        document.querySelectorAll("input[name^='ventas-']").forEach(
            item =>{
                item.addEventListener("change", event =>{
                let quantity = event.target.parentElement.parentElement.querySelector('input[id$=cantidad]').value;
                let price = event.target.parentElement.parentElement.querySelector('input[id$=precio]').value;
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
                    let select_id = this.dataset['select2Id'];
                    let indice = get_indice(select_id);
                    let cantidad = document.querySelector(`#id_ventas-${indice}-cantidad`).value;
                    let price_node = get_price_node(indice);

                    let articulo_venta = select_to_articulo_venta(item);
                    let total = document.querySelector(`tr#ventas-${indice} td.field-precio_total`)

                    if(cantidad > articulo_venta.umbral) {
                        price_node.setAttribute("value", articulo_venta.precio_mayorista);
                        total.innerHTML =  "<p style='color:blue'>" + String(parseFloat(cantidad)*parseFloat(articulo_venta.precio_mayorista)) + "</p>";
                    } else {
                        price_node.setAttribute("value", articulo_venta.precio_minorista);
                        total.innerHTML = "<p style='color:blue'>" + String(parseFloat(cantidad)*parseFloat(articulo_venta.precio_minorista)) + "</p>";
                    }
                    update_precio_total();
                
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
                    let total = document.querySelector(`tr#ventas-${indice} td.field-precio_total`)
                
                    if(cantidad > articulo_venta.umbral) {
                        price_node.setAttribute("value", articulo_venta.precio_mayorista);
                        total.innerHTML =  "<p style='color:blue'>" + String(parseFloat(cantidad)*parseFloat(articulo_venta.precio_mayorista)) + "</p>";
                    } else {
                        price_node.setAttribute("value", articulo_venta.precio_minorista);
                        total.innerHTML = "<p style='color:blue'>" + String(parseFloat(cantidad)*parseFloat(articulo_venta.precio_minorista)) + "</p>";
                    }
                    update_precio_total();
                }
            }
        );
        document.querySelectorAll("input[id$='precio']").forEach(
            item => {
                item.onchange = function(){
                    let indice = get_indice(item.id, "-precio");
                    let cantidad = get_cantidad_node(indice).value;
                    let precio = item.value;
                    let select_articulo_venta = document.querySelector(`#id_ventas-${indice}-articulo`);
                    let articulo_venta = null;
                    if (! select_articulo_venta || select_articulo_venta.textContent === '\n'){
                        return null;
                    } else {
                        articulo_venta = select_to_articulo_venta(null, text=select_articulo_venta.textContent);
                    }
                    let total = document.querySelector(`tr#ventas-${indice} td.field-precio_total`)
                
                    total.innerHTML =  "<p style='color:blue'>" + (parseFloat(cantidad)*parseFloat(precio)).toFixed(2) + "</p>";
                
                    update_precio_total();
                }
            }
        );
        document.querySelectorAll("select[id^='id_ventas-'][id$='-articulo']").forEach(
            select => {
                select.onchange = function() {
                    let indice = get_indice(select.id, "-articulo");
                    let articulo_venta = select_to_articulo_venta(null, text=select.options[select.selectedIndex].text);
                    let cantidad_node = document.querySelector(`#id_ventas-${indice}-cantidad`);
                    let precio_node = document.querySelector(`#id_ventas-${indice}-precio`);
                    let total_node = document.querySelector(`tr#ventas-${indice} td.field-precio_total`);

                    if (cantidad_node.value > articulo_venta.umbral) {
                        precio_node.value = articulo_venta.precio_mayorista;
                        total_node.innerHTML = "<p style='color:blue'>" + (parseFloat(cantidad_node.value) * parseFloat(articulo_venta.precio_mayorista)).toFixed(2) + "</p>";
                    } else {
                        precio_node.value = articulo_venta.precio_minorista;
                        total_node.innerHTML = "<p style='color:blue'>" + (parseFloat(cantidad_node.value) * parseFloat(articulo_venta.precio_minorista)).toFixed(2) + "</p>";
                    }
                    update_precio_total();
                }
            }
        );
        init();
        
    }
);

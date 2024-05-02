
let get_price_from_articulo_option = node => {
    let option_selected = node.selectedOptions[0].textContent;
    let price = option_selected.match(/\d+.?\d+/)[0];

    return price
}

let get_price_node = select_id => {
    let id = select_id.slice('id_venta-'.length, -'-articulo'.length);
    return document.querySelector('#id_ventas-'+id+'-precio');
    
}

document.addEventListener("DOMContentLoaded",
    function(event) {
        document.querySelectorAll("input[name^='items-']").forEach(
            item =>{
                item.addEventListener("change", event =>{
                let quantity = event.target.parentElement.parentElement.querySelector('input[id$=quantity]').value;
                let price = event.target.parentElement.parentElement.querySelector('input[id$=price]').value;
                let total = parseFloat(price*quantity);
                event.target.parentElement.parent Element.querySelector('[class$=total]').querySelector('p').textContent = total;

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
                    let price_node = get_price_node(select_id);
                    price_node.value =  get_price_from_articulo_option(item);
                    }
            }
        );
    }
);

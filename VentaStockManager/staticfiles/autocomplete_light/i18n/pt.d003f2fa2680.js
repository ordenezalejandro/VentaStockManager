/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(e){var n;(n=e&&e.fn&&e.fn.select2&&e.fn.select2.amd?e.fn.select2.amd:n).define("select2/i18n/pt",[],function(){return{errorLoading:function(){return"Os resultados não puderam ser carregados."},inputTooLong:function(e){e=e.input.length-e.maximum;return"Por favor apague "+e+" "+(1!=e?"caracteres":"caractere")},inputTooShort:function(e){return"Introduza "+(e.minimum-e.input.length)+" ou mais caracteres"},loadingMore:function(){return"A carregar mais resultados…"},maximumSelected:function(e){return"Apenas pode seleccionar "+e.maximum+" "+(1!=e.maximum?"itens":"item")},noResults:function(){return"Sem resultados"},searching:function(){return"A procurar…"},removeAllItems:function(){return"Remover todos os itens"}}}),n.define,n.require},event=new CustomEvent("dal-language-loaded",{lang:"pt"});document.dispatchEvent(event);
/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(n){var e;(e=n&&n.fn&&n.fn.select2&&n.fn.select2.amd?n.fn.select2.amd:e).define("select2/i18n/ru",[],function(){function t(n,e,t,u){return n%10<5&&0<n%10&&n%100<5||20<n%100?1<n%10?t:e:u}return{errorLoading:function(){return"Невозможно загрузить результаты"},inputTooLong:function(n){var e=n.input.length-n.maximum,n="Пожалуйста, введите на "+e+" символ";return(n+=t(e,"","a","ов"))+" меньше"},inputTooShort:function(n){n=n.minimum-n.input.length;return"Пожалуйста, введите ещё хотя бы "+n+" символ"+t(n,"","a","ов")},loadingMore:function(){return"Загрузка данных…"},maximumSelected:function(n){return"Вы можете выбрать не более "+n.maximum+" элемент"+t(n.maximum,"","a","ов")},noResults:function(){return"Совпадений не найдено"},searching:function(){return"Поиск…"},removeAllItems:function(){return"Удалить все элементы"}}}),e.define,e.require},event=new CustomEvent("dal-language-loaded",{lang:"ru"});document.dispatchEvent(event);
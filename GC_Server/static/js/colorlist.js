function sendData(colorName){
    var select = document.getElementById('selectColor');
    select.value=colorName;
    console.log(colorName);
    var form = document.getElementById('colorradio');
    form.submit();
}
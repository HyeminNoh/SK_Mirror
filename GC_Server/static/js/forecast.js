window.onload(makeForecast());

function makeForecast(){
    // get JSON with using pure javascript
    var request= new XMLHttpRequest();

    var url= "http://127.0.0.1:8080/forecast";
    request.open("GET", url);
    request.responseType='json';
    request.send();
    request.onload = function() {
        var forecast_data = request.response;
        console.log(forecast_data);
        var forecast_body = document.getElementById('forecast');
        for (var i = 0; i < Object.keys(forecast_data).length; i++) {
            row = forecast_body.insertRow(forecast_body.rows.length);
            row.style.fontSize="20px"
            keyword = row.insertCell(0);
            text = row.insertCell(1);
            text.style.padding="5px"
            var keys = Object.keys(forecast_data);
            var content = forecast_data[keys[i]];
            keyword.innerHTML = keys[i];
            text.innerHTML = content;
        }
    }
}
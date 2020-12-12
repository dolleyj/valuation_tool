$( function () {
    
    console.log("index.js loaded!");

    $("#submit_add_stock").on("click", function(e){
        e.preventDefault();
        var stock_sym = $("#search_symbol").val();
        console.log("Searching stock: ", stock_sym);

        var response = get_stock_data(stock_sym);
        response.then(function(data){
            console.log("Inside then!");
            // console.log(data);
            console.log(stock_sym, ': ', data['fair_values'])
        });
    });

});




function get_stock_data(stock_sym) {
console.log("Inside get_stock_data");
return $.get("./api/get_stock_info", {"symbol": stock_sym}, function(data) {
    // console.log(data);
    return data;
});
}

function buildTable(){
    //TODO Build the table on page onload. Uses STORED data (sqlite3)?
}

function addRowToTable(data) {
    // var rowHtml = "<tr>"   
}
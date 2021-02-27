$( function () {
    
    console.log("index.js loaded!");
    load_stocks();

    $("#submit_add_stock").on("click", function(e){
        e.preventDefault();
        var stock_sym = $("#search_symbol").val();
        console.log("Searching stock: ", stock_sym);

        var response = get_stock_data(stock_sym);
        response.then(function(data){
            console.log(stock_sym, ': ', data);

            // Add stock to table as last row
            var rowHTML = buildTableRow(data['table_headers'], data['stock']);
            $(".table-last-row").removeClass("table-last-row").after(rowHTML);


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

function get_stored_stocks() {
    console.log("Inside get_stored_stocks");
    return $.get("./api/get_stored_stocks", function(data) {
        // console.log(data);
        return data;
    });
}

function load_stocks() {
    console.log("loading saved stocks...");
    var response = get_stored_stocks();
    response.then(function(data){

        // Build the table from stored stocks
        var tableHTML = buildTable(data['table_headers'], data['stocks']);
        $("#stock_table_container").html(tableHTML);
    });
}

function buildTable(table_headers, data){
    //TODO Build the table on page onload. Uses STORED data (sqlite3)?
    var tableHTML = "<table class='table table-striped'><thead><tr>";

    // Build table headers
    table_headers.forEach(item => {
        tableHTML += "<th>" + item['human_readable'] + "</th>";
    });
    tableHTML += "</tr></thead><tbody>";
    
    // Build data rows
    data.forEach((stock, idx, _stocks) => {
        if (idx === _stocks.length - 1) {
            tableHTML += "<tr class='table-last-row'>";
        } else {
            tableHTML += "<tr>";
        }
        table_headers.forEach((header) => {
            tableHTML += "<td>" + stock[ header['name'] ] + "</td>";
        });
        tableHTML += "</tr>";
    });
    tableHTML += "</tbody></table>";
    
    return tableHTML;    
}

function buildTableRow(table_headers, stock_data) {
    var rowHTML = "<tr class='table-last-row'>"; 

    table_headers.forEach((header) => {
        rowHTML += "<td>" + stock_data[ header['name'] ] + "</td>";
    });
    rowHTML += "</tr>";

    return rowHTML;
}

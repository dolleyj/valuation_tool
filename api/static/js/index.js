// Global stocks-table jQuery object
var $stocksTable = $("#stocks-table");

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

            // // Add stock to table as last row
            // var rowHTML = buildTableRow(data['table_headers'], data['stock']);
            // $(".table-last-row").removeClass("table-last-row").after(rowHTML);

            addStockToTable(data['stock']);
        });
    });

});

window.operateEvents = {
    'click .refresh': function (e, value, row, index) {
        // Refresh a stock's data
        // alert('You click like action, row: ' + JSON.stringify(row))
        console.log("Refreshing row: ", row);
        // TODO - https://examples.bootstrap-table.com/index.html#methods/update-row.html

    },
    'click .remove': function (e, value, row, index) {
        // Remove a stock from the database and table
        var response = deleteStockFromTable(row.symbol);
        response.then(function(data){
            if (data.success) {
                $stocksTable.bootstrapTable('remove', {
                    field: 'symbol',
                    values: [row.symbol]
                });
            } else {
                //TODO - handle this with better style
                alert("Unable to delete stock from database.");
            }
        });
        
    }
}

// BootstrapTable function
function operateFormatter(value, row, index) {
    /* Returns the buttons/icons for row events
    */
    return [
      '<a class="refresh" href="javascript:void(0)" title="Refresh">',
      '<i class="fa fa-refresh">R</i>',
      '</a>  ',
      '<a class="remove" href="javascript:void(0)" title="Remove">',
      '<i class="fa fa-trash">T</i>',
      '</a>'
    ].join('')
}


function addStockToTable(data) {
    /* Adds new row to stocks-table and auto-scrolls to bottom
    */
    $stocksTable.bootstrapTable('append', data);
    $stocksTable.bootstrapTable('scrollTo', 'bottom');
}

function deleteStockFromTable(stock_sym) {
    /* Deletes a stock from the database. Returns true if successful, otherwise false
    */
    console.log("Inside deleteStockFromTable");
    return $.get("./api/delete_stock", {"symbol": stock_sym}, function(data) {
        return data;
    });
}

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
        console.log("sqlite data: ", data);

        // Build the table from stored stocks
        buildTableBody($stocksTable, data['stocks']);
    });
}

function buildTableHeaders($element, headers) {
    // TODO?
}

function buildTableBody($element, data) {
    console.log("Inside buildTableBody");
    // Initialize Bootstrap Table
    $element.bootstrapTable({data:data});
}

// function buildTable(table_headers, data){
//     //TODO Build the table on page onload. Uses STORED data (sqlite3)?
//     var tableHTML = "<table class='table table-striped'><thead><tr>";

//     // Build table headers
//     table_headers.forEach(item => {
//         tableHTML += "<th>" + item['human_readable'] + "</th>";
//     });
//     tableHTML += "</tr></thead><tbody>";
    
//     // Build data rows
//     data.forEach((stock, idx, _stocks) => {
//         if (idx === _stocks.length - 1) {
//             tableHTML += "<tr class='table-last-row'>";
//         } else {
//             tableHTML += "<tr>";
//         }
//         table_headers.forEach((header) => {
//             tableHTML += "<td>" + stock[ header['name'] ] + "</td>";
//         });
//         tableHTML += "</tr>";
//     });
//     tableHTML += "</tbody></table>";
    
//     return tableHTML;    
// }

// function buildTableRow(table_headers, stock_data) {
//     var rowHTML = "<tr class='table-last-row'>"; 

//     table_headers.forEach((header) => {
//         rowHTML += "<td>" + stock_data[ header['name'] ] + "</td>";
//     });
//     rowHTML += "</tr>";

//     return rowHTML;
// }

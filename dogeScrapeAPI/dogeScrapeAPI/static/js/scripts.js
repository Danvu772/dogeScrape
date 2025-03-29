$(document).ready(function() {
    // Ensure csvFiles is available
    if (typeof csvFiles !== 'undefined' && csvFiles.length > 0) {
        csvFiles.forEach(function(csvFile) {
            var tableId = 'dataTable-' + csvFile;  // Unique ID for each table
            var apiUrl = '/api/data/' + csvFile;  // Endpoint for fetching data

            // Create a new table container dynamically
            var tableContainer = $('<div></div>').appendTo('#tables-container');
            tableContainer.append('<h3>' + csvFile + '</h3>');  // Table Title
            tableContainer.append('<table id="' + tableId + '" class="table table-striped table-bordered"><thead><tr></tr></thead><tbody></tbody></table>');

            // Initialize DataTable for the current CSV file
            $('#' + tableId).DataTable({
                ajax: {
                    url: apiUrl,  // API endpoint
                    dataSrc: '', // Data is directly returned in the JSON response
                },
                columns: []  // Empty columns initially; these will be dynamically populated
                , paging: true,      // Enable pagination
                searching: true,   // Enable search
                ordering: true,    // Enable sorting
                info: true,        // Enable info display
            });

            // Dynamically set columns after DataTable has been initialized
            $.ajax({
                url: apiUrl,  // Fetch data again to get the columns
                success: function(data) {
                    if (data.length > 0) {
                        // Extract column names from the first row of the data
                        var columns = Object.keys(data[0]);

                        // Define columns dynamically
                        var columnDefs = columns.map(function (col) {
                            return { data: col, title: col }; // Use column names for the headers
                        });

                        // Redefine the DataTable columns dynamically
                        var table = $('#' + tableId).DataTable();
                        table.clear().destroy(); // Clear the table and destroy old DataTable instance
                        table = $('#' + tableId).DataTable({
                            ajax: {
                                url: apiUrl,
                                dataSrc: ''
                            },
                            columns: columnDefs, // Dynamically set columns
                            paging: true,
                            searching: true,
                            ordering: true,
                            info: true
                        });
                    }
                }
            });
        });
    } else {
        console.error("csvFiles array is not defined or empty.");
    }
});

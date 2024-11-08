const dataTableOptions = {
    columnDefs: [
        {className: 'center', targets: [0,1,2,3,4,5,6,7]},
        {orderable: false, targets: [4,6,7]},
        {searchable: false, targets: [0,3,4,5,6,7]},
        {responsivePriority: 1, targets: -1}
    ],
    pageLength: 8,
    destroy: true,
}

$(document).ready(function () {
    $('#dataTableGym').DataTable(dataTableOptions);
    $('#dataTableGymDay').DataTable(dataTableOptionsDay);
    
});

//esta parte es la de los usuarios que solo van un día
const dataTableOptionsDay = {
    columnDefs: [
        {className: 'center', targets: [0,1,2,3,4,5,6]},
        {orderable: false, targets: [3,5,6]},
        {searchable: false, targets: [0,3,4,5,6]}
    ],
    pageLength: 8,
    destroy: true
}
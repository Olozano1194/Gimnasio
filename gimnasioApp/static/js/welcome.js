const dataTableOptions = {
    columnDefs: [
        {className: 'center', targets: [0,1,2,3,4,5,6,7]},
        {orderable: false, targets: [4,6,7]}, //Columnas ordenables
        {searchable: false, targets: [0,3,4,5,6,7]} //Columnas no buscables
        
    ],
    pageLength: 8, //Número de registros por pagina
    destroy: true, //Destruir instancias previas de la tabla al iniciar de nuevo
    order: [[0, 'desc']], //Ordenar por la primera columna de manera descendente
    //"aaSorting": []
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
    destroy: true, 
    order: [[0, 'desc']]
}
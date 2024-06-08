
const dataTableOptions = { 
    columnDefs: [
        {className: 'center', targets: [0,1,2,3,4,5,6,7]},
        {orderable: false, targets: [4,6,7]},
        {searchable: false, targets: [0,3,4,5,6,7]}
    ],
    pageLength: 8,
    destroy: true
}

// const initDataTable = async() => {
//     if (dataTableIsInitialized) {
//         dataTable.destroy();
//     }
// await listGym();

// dataTable = $('#dataTableGym').DataTable(dataTableOptions);

// dataTableIsInitialized = true;

// };

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

// $(document).ready(function () {
//     $('#dataTableGymDay').DataTable(dataTableOptionsDay);
// });
// const listGym = async () => {
//     try {
//         const response = await fetch('http://127.0.0.1:8000/listGym');
//         const data = await response.json();
//         // console.log(data.gym);
//         let content = ``;
//         data.gym.forEach((userGym, index) => {
//             content += `
//                 <tr>
//                     <td>${index+1}</td>
//                     <td>${userGym.name}</td>
//                     <td>${userGym.lastname}</td>
//                     <td>${userGym.phone}</td>
//                     <td>${userGym.address}</td>
//                     <td>${userGym.dateInitial}</td>
//                     <td>${userGym.dateFinal}</td>
//                     <td>${userGym.price}</td>
//                     <td>
//                        <a href="{%  url 'update_user' u.id %}" class='btn btn-sm btn-block btn-info'><i class="fa-solid fa-pencil"></i> Update</a>
//                        <a href="{%  url 'delete' u.id %}" class='btn btn-sm btn-block btn-danger btnDelete'><i class="fa-regular fa-trash-can"></i> Delete</a>
//                     </td>

//                 </tr>
//             `            
//         });
//         tableBodyGym.innerHTML = content;
//     } catch (error) {
//         alert(error);
//     }

// };

// window.addEventListener('load', async() => {
//     await initDataTable();
// });
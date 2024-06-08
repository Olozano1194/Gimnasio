const btnsDelete = document.querySelectorAll('.btnDelete');

//esto es del archivo html delete

(function () {
    
    btnsDelete.forEach(btn => {
        btn.addEventListener('click', function (e) {
            let confirmación= confirm('¿Está seguro de eliminar el usuario?');
            if (!confirmación) {
                e.preventDefault();
            }
        });
        
    });
})();
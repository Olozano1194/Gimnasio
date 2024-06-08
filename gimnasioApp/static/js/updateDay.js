const formUser = document.getElementById('formUser');
const inputName = document.getElementById('name');
const inputLastname = document.getElementById('lastname');
const inputPhone = document.getElementById('phone');
const inputDate = document.getElementById('dateInitial');
const inputPrice = document.getElementById('price');
const btnEnviar = document.querySelector('.btnUpdate');


btnEnviar.disabled = true;

window.onload = function validaciones() {
    
     //esto es para el nombre y apellido
    const validateEmptyField = (e) => {
        const field = e.target;
        const fieldValue = e.target.value;

        if (fieldValue.trim().length === 0) {
            
            field.classList.add('falla');
            field.nextElementSibling.classList.add('error');
            field.nextElementSibling.innerText = `${field.name} requerido`;
            btnEnviar.disabled = true;
        }else if (/^\d+$/.test(fieldValue) || /\d/.test(fieldValue)) {
            field.classList.add('falla');
            field.nextElementSibling.classList.add('error');
            field.nextElementSibling.innerText = `El ${field.name} no debe contener números`;
            btnEnviar.disabled = true;
        }else {
            field.classList.remove('falla')
            field.nextElementSibling.classList.remove('error');
            field.nextElementSibling.innerText = '';
            btnEnviar.disabled = false;
        }
    }

    //esto es para el usuario
    const validateEmptyField2 = (e) => {
        const field = e.target;
        const fieldValue = e.target.value;

        if (fieldValue.trim().length === 0) {
            
            field.classList.add('falla');
            field.nextElementSibling.classList.add('error');
            field.nextElementSibling.innerText = `${field.name} requerido`;
            btnEnviar.disabled = true;
        }else {
            field.classList.remove('falla')
            field.nextElementSibling.classList.remove('error');
            field.nextElementSibling.innerText = '';
            btnEnviar.disabled = false;
        }
    }

    //validar numeros
    const validateEmptyFieldNum = (e) => {
        const field = e.target;
        const fieldValue = e.target.value;

        if (fieldValue.trim().length === 0) {
            
            field.classList.add('falla');
            field.nextElementSibling.classList.add('error');
            field.nextElementSibling.innerText = `${field.name} requerido`;
            btnEnviar.disabled = true;
            
        }else if (!/^\d+$/.test(fieldValue) || !/\d/.test(fieldValue)) {
            field.classList.add('falla');
            field.nextElementSibling.classList.add('error');
            field.nextElementSibling.innerText = `El ${field.name} debe ser numero`;
            btnEnviar.disabled = true;
        }else {
            field.classList.remove('falla')
            field.nextElementSibling.classList.remove('error');
            field.nextElementSibling.innerText = '';
            btnEnviar.disabled = false;
        }
    }
    
    
    inputName.addEventListener('blur', validateEmptyField);
    inputLastname.addEventListener('blur', validateEmptyField);
    inputPhone.addEventListener('blur', validateEmptyFieldNum);
    inputPrice.addEventListener('blur', validateEmptyFieldNum);

}
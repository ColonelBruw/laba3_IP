import { API_HOST, API_PORT } from 'astro:env/client';
import { authorizationStatusSet, authorizationStatusSwitch, authorization_status } from './auth_check';

const modal_reg = document.getElementById('ModalReg');
const modal_login = document.getElementById('ModalLogin');
const modal_logout = document.getElementById('ModalLogout');

const reg_btn = document.getElementById('RegistrationButton');
const login_btn = document.getElementById('LoginButton');
const logout_btn = document.getElementById('LogoutButton');

const submit_reg_btn = document.getElementById('SubmitRegistration');
const submit_login_btn = document.getElementById('SubmitLogin');
const submit_logout_btn = document.getElementById('SubmitLogin');

const close_reg_span = document.querySelector('.CloseRegModal');
const close_login_span = document.querySelector('.CloseLoginModal');
const close_logout_span = document.querySelector('.CloseLogoutModal');


// Открытие формы
reg_btn.addEventListener('click', function() {
    modal_reg.style.display = 'block'
});
login_btn.addEventListener('click', function() {
    modal_login.style.display = 'block'
});
logout_btn.addEventListener('click', function() {
    modal_logout.style.display = 'block'
});

// Закрытие формы по крестику
close_reg_span.addEventListener('click', function() {
    modal_reg.style.display = 'none'
});
close_login_span.addEventListener('click', function() {
    modal_login.style.display = 'none'
});
close_logout_span.addEventListener('click', function() {
    modal_logout.style.display = 'none'
});

// Закрытие по клику вне окна
window.addEventListener('click', function(event) {
    if (event.target === modal_logout) {
        modal_logout.style.display = 'none'
    } else if (event.target === modal_reg) {
        modal_reg.style.display = 'none'
    } else if (event.target === modal_login) {
        modal_login.style.display = 'none'
    }
});

// Отправка данных формы регистрации
modal_reg.onsubmit = async (event) => {
    event.preventDefault();

    submit_reg_btn.disabled = true;

    const formData = new FormData(modal_reg);
    // formData.delete('confirmpassword')

    const plainFormData = Object.fromEntries(formData.entries())

    console.log(formData)
    console.log(plainFormData)

    try {
        // Отправка данных на FastAPI сервер
        const response = await fetch(`http://${API_HOST}:${API_PORT}/api/v1/endpoints/registration`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(plainFormData)
        });

        const result = await response.json();

        if (response.ok) {
            if (result.status === "200") {
                alert(result.message)
                modal_reg.reset()
                modal_reg.style.display = 'none'
                submit_reg_btn.disabled = false;
            } else {
                alert(result.message)
                submit_reg_btn.disabled = false;
            };
        } else {
            alert("Ошибка на бекенде: код " + response.status)
        }
    } catch (error) {
        alert("Что-то пошло не так: " + error.message)
    }
}

// Отправка данных формы входа
modal_login.onsubmit = async (event) => {
    event.preventDefault();

    submit_login_btn.disabled = true;

    const formData = new FormData(modal_login);
    const plainFormData = Object.fromEntries(formData.entries())

    console.log(formData)

    try {
        // Отправка данных на FastAPI сервер
        // console.log('вход в трай')
        const response = await fetch(`http://${API_HOST}:${API_PORT}/api/v1/endpoints/login`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(plainFormData)
        });

        const result = await response.json();
        console.log(result)

        if (response.ok) {
            if (result.status === "200") {
                modal_login.reset()
                modal_login.style.display = 'none';
                submit_login_btn.disabled = false;
                authorizationStatusSwitch(1);
                // console.log('статус свитч ок')
            } else {
                submit_login_btn.disabled = false;
                alert(result.message)
            }
            await authorizationStatusSet();
        } else {
            alert("Ошибка на бекенде: код " + response.status)
        }
    } catch (error) {
        alert("Что-то пошло не так: " + error.status)
    }
}

// Выход из акканунта
modal_logout.onsubmit = async (event) => {
    event.preventDefault();

    submit_logout_btn.disabled = true;

    try {
        // Отправка данных на FastAPI сервер
        const response = await fetch(`http://${API_HOST}:${API_PORT}/api/v1/endpoints/logout`, {
            method: 'GET',
            credentials: 'include',
        });

        const result = await response.json();

        if (response.ok) {
            if (result.status === "200") {
                modal_logout.reset()
                modal_logout.style.display = 'none';
                submit_logout_btn.disabled = false;
                authorizationStatusSwitch(0);
            } else {
                alert(1)
                submit_logout_btn.disabled = false;
            };
            await authorizationStatusSet();
        } else {
            alert("Ошибка на бекенде: код " + response.status)
        }
    } catch (error) {
        alert("Что-то пошло не так: " + error.status)
    }
}

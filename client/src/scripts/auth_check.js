// Импортируем переменные окружения
import { API_HOST, API_PORT } from 'astro:env/client';

const reg_btn = document.getElementById('RegistrationButton');
const login_btn = document.getElementById('LoginButton');
const logout_btn = document.getElementById('LogoutButton');
const name_holder = document.querySelector('#NameHolder')

// Равен 1 если пользователь авторизован, иначе 0
export let authorization_status = 0;
export function authorizationStatusSwitch(newValue) {
    authorization_status = newValue;
}

// Функция проверки авторизации - имеет ли пользователь активную сессию или нет
async function authorizationCheck() {
    try {
        // Отправка данных на FastAPI сервер
        // console.log(1)
        const response = await fetch(`http://${API_HOST}:${API_PORT}/api/v1/endpoints/auth-check`, {
            method: 'POST',
            credentials: 'include',
        });
        // console.log(2)

        const result = await response.json();
        console.log(result)

        if (response.ok) {
            if (result.status === '200') {
                authorization_status = 1;
                console.log(211)
                return result;
            } else {
                authorization_status = 0;
                console.log(result.message)
            }
        } else {
            alert('Не удалось установить статус аутентификации: ' + response.message)
        }
    } catch (error) {
        alert("Что-то пошло не так: " + error.message)
    }
};

// Функция устанавливающая отображение страницы в зависимости от статуса авторизации
export async function authorizationStatusSet() {
    const result = await authorizationCheck();
    if (authorization_status) {
        name_holder.textContent = `Здравствуйте, ${result.payload['first_name']}!`;
        name_holder.style.display = 'inline'
        reg_btn.style.display = 'none'
        login_btn.style.display = 'none'
        logout_btn.style.display = 'block'
    } else {
        name_holder.style.display = 'none'
        reg_btn.style.display = 'block'
        login_btn.style.display = 'block'
        logout_btn.style.display = 'none'
    }
}

authorizationStatusSet();

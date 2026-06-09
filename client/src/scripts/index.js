// Импортируем переменные окружения
import { API_HOST, API_PORT } from 'astro:env/client';

const modal_job = document.getElementById('ModalJob');
const employment_btn = document.getElementById('EmploymentButton');
const submit_job_btn = document.getElementById('SubmitJob');
const close_employment_span = document.querySelector('.CloseJobModal');

const theme_btn = document.getElementById('Theme');

// Открытие формы
employment_btn.addEventListener('click', function() {
    modal_job.style.display = 'block'
});

// Закрытие формы по крестику
close_employment_span.addEventListener('click', function() {
    modal_job.style.display = 'none'
});

// Отправка данных формы
modal_job.onsubmit = async (event) => {
    event.preventDefault();

    submit_job_btn.disabled = true;

    const formData = new FormData(modal_job);
    const plainFormData = Object.fromEntries(formData.entries())

    console.log(formData.get('pos'))

    try {
        // Отправка данных на FastAPI сервер
        const response = await fetch(`http://${API_HOST}:${API_PORT}/api/v1/endpoints/job-application`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(plainFormData)
        });

        const result = await response.json();
        console.log(result)

        if (response.ok) {
            if (result.status === "200") {
                alert(result.message)
                modal_job.reset()
                modal_job.style.display = 'none'
                submit_job_btn.disabled = false;
            } else {
                alert(result.message)
                submit_job_btn.disabled = false;
            }
        } else {
            alert("Ошибка на бекенде: код " + response.status)
        }
    } catch (error) {
        alert("Что-то пошло не так: " + error)
    }
}

// Закрытие по клику вне окна
window.addEventListener('click', function(event) {
    if (event.target === modal_job) {
        modal_job.style.display = 'none'
    }
});

//Функция переключения темы
function switchTheme() {
        const theme_btn_img = theme_btn.firstElementChild.src
        if (theme_btn_img.split("/").at(-1) === "moon.png") {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.querySelector('#ThemeIcon').src = '/sun.jpg'
            document.querySelector('#HeaderImg').src = '/carfast_negate.png'
            document.querySelector('#UpperDiv1Img').src = '/carfast_negate.png'
        } else {
            document.documentElement.setAttribute('data-theme', 'light')
            document.querySelector('#ThemeIcon').src = '/moon.png'
            document.querySelector('#HeaderImg').src = '/carfast.png'
            document.querySelector('#UpperDiv1Img').src = '/carfast.png'
        }
    }
    
//Смена темы
theme_btn.addEventListener('click', switchTheme);

//Установка картинок на задний план в блоке выбора услуг
for (let i = 1; i < 7; i++) {
    let service_button = document.getElementById('ServiceBlock' + i)
    service_button.style.setProperty('background-image', 'url("services' + i + '.jpg")');
}
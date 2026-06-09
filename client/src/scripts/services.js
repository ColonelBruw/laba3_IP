// Импортируем переменные окружения
import { API_HOST, API_PORT } from 'astro:env/client';

const modal_service = document.getElementById('ModalService');
const service_btns = document.querySelectorAll('.TheService')
const submit_service_btn = document.getElementById('SubmitService');
const close_service_span = document.querySelector('.CloseServiceModal');

const theme_btn = document.getElementById('Theme');

// Задание динамических пределов установления даты в форме
// Записаться можно начиная с завтрашнего дня в интервале 3 месяцев
const min_input_date = new Date();
min_input_date.setDate(min_input_date.getDate() + 1);

const max_input_date = new Date();
max_input_date.setMonth(max_input_date.getMonth() + 3);

document.querySelector('#InputDate').min = min_input_date.toISOString().split('T')[0];
document.querySelector('#InputDate').max = max_input_date.toISOString().split('T')[0];

// Закрытие по крестику
close_service_span.addEventListener('click', function() {
    modal_service.style.display = 'none';
});

// Функция открытия модальных окон услуг
service_btns.forEach(btn => {
    btn.addEventListener('click', function() {
        let service_name = btn.querySelector('p').textContent
        console.log(service_name)

        let modal_title = document.getElementById('ModalTitle')

        modal_title.textContent = service_name
        console.log(modal_title.textContent)
        
        modal_service.style.display = 'block';
    });
  });


// Отправка формы записи на услугу
modal_service.onsubmit = async (event) => {
    event.preventDefault();

    submit_service_btn.disabled = true;

    const formData = new FormData(modal_service);
    const service_name = document.querySelector('#ModalTitle').textContent
    formData.append('service_name', service_name)
    
    const plainFormData = Object.fromEntries(formData.entries())

    console.log(formData)
    console.log(plainFormData)

    try {
        // Отправка данных на FastAPI сервер
        const response = await fetch(`http://${API_HOST}:${API_PORT}/api/v1/endpoints/service-appointment`, {
            method: 'POST', 
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(plainFormData)
        });

        const result = await response.json();
        console.log(result.pos)

        if (response.ok) {
            if (result.status === "200") {
                alert(result.message)
                modal_service.reset()
                modal_service.style.display = 'none'
                submit_service_btn.disabled = false;
            } else {
                alert(result.message)
                submit_service_btn.disabled = false;
            }
        } else {
            alert('Ошибка на бекенде: код ' + response.status)
        }
    } catch (error) {
        alert("Что-то пошло не так: " + error.message)
    }
}

// Закрытие по клику вне окна
window.addEventListener('click', function(event) {
    if (event.target === modal_service) {
        modal_service.style.display = "none"
    }
});

// Функция открытия модальных окон услуг
service_btns.forEach(btn => {
    btn.addEventListener('click', function() {
        let service_name = btn.querySelector('p').textContent
        console.log(service_name)

        let modal_title = document.getElementById('ModalTitle')

        modal_title.textContent = service_name
        console.log(modal_title.textContent)
        
        modal_service.style.display = 'block';
    });
  });

//Функция переключения темы
function switchTheme() {
        const theme_btn_img = theme_btn.firstElementChild.src
        if (theme_btn_img.split("/").at(-1) === "moon.png") {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.querySelector('#ThemeIcon').src = '/sun.jpg'
            document.querySelector('#HeaderImg').src = '/carfast_negate.png'

            for (let i = 1; i < 7; i++) {
                document.querySelector('#Service' + i + 'Img').src = '/services1' + i + '_negate.png'
            }
    
        } else {
            document.documentElement.setAttribute('data-theme', 'light')
            document.querySelector('#ThemeIcon').src = '/moon.png'
            document.querySelector('#HeaderImg').src = '/carfast.png'

            for (let i = 1; i < 7; i++) {
                document.querySelector('#Service' + i + 'Img').src = '/services1' + i + '.png'
            }
        }
    }
    
//Смена темы
theme_btn.addEventListener('click', switchTheme);
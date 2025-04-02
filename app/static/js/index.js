const registr_btn = document.querySelector('#registr_btn')
const login_btn = document.querySelector('#login_btn')
const userdata_forms = document.querySelectorAll('.user_data_form')
const hide_userdata_form = document.querySelectorAll('.hide_userdata_form')

registr_btn.addEventListener('click', () => {
    userdata_forms[1].style.display = 'none'
    userdata_forms[0].style.animation = 'show_input_form ease forwards 0.3s'
    userdata_forms[0].style.display = 'flex'
})

login_btn.addEventListener('click', () => {
    userdata_forms[0].style.display = 'none'
    userdata_forms[1].style.animation = 'show_input_form ease forwards 0.3s'
    userdata_forms[1].style.display = 'flex'
})

hide_userdata_form[0].addEventListener('click', () => {
    userdata_forms[0].style.animation = 'hide_input_form ease 0.2s forwards'
    setTimeout(() => {
        userdata_forms[0].style.animation = 'none'
        userdata_forms[0].style.display = 'none'
    }, 200)
})
hide_userdata_form[1].addEventListener('click', () => {
    userdata_forms[1].style.animation = 'hide_input_form ease 0.2s forwards'
    setTimeout(() => {
        userdata_forms[1].style.animation = 'none'
        userdata_forms[1].style.display = 'none'
    }, 200)
})
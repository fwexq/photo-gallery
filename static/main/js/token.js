let submitInput = document.getElementById('submit-form')
let form = document.getElementById('form')
let input1 = document.getElementsByName('email')[0]
let input2 = document.getElementsByName('password')[0]
console.log(form, '00000000')

let info = {}
$(form).submit(function (e){
    e.preventDefault()
    info['email'] = input1.value
    info['password'] = input2.value
    a = $.ajax({
        url: 'http://localhost:8000/api/login/',
        method: 'POST',
        data: JSON.stringify({'email': info.email, 'password': info.password}),
        dataType: 'json',
        contentType:'application/json',
        success: function (response, status){
            localStorage.setItem(`token${info.email}`, response.token)
            console.log(localStorage.getItem(`token${info.email}`))
        },
        error: (error) => {
            console.log(error)
        }
    })
     e.target.submit()
})
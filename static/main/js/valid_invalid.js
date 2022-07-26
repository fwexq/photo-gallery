let baseUrl = `http://localhost:8000/api/`
let validBtns= document.getElementsByName('valid-btn')
let invalidBtns = document.getElementsByName('invalid-btn')


async function makeRequest(url, method = 'GET', headers) {
    return $.ajax({
        url,
        method: method,
        headers: headers,
        success: (res) => {
            return res
        },
        error: function (res, status) {
            console.log(res)
        }
    })
}
for (let btn of validBtns) {
    $(btn).click(async function (event) {
        let user = this.dataset.user
        console.log(this.dataset.user)
        let id = this.dataset.posts_id
        let data = await makeRequest(`${baseUrl}valid/${id}/`, 'POST', {'Authorization': `Token ${localStorage.getItem(`token${user}`)}`})
        console.log(data.answer)
    }
    )
}
for (let btn of invalidBtns) {
    $(btn).click(async function (event) {
        let user = this.dataset.user
        let id = this.dataset.posts_id
        let data = await makeRequest(`${baseUrl}invalid/${id}/`, 'POST', {'Authorization': `Token ${localStorage.getItem(`token${user}`)}`})
        console.log(data.answer)
    }
    )
}
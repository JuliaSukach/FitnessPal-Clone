const GOOGLE_CLIENT_ID = '121483820619-lr68ifev2038buns1ite5va1fmibt87i.apps.googleusercontent.com'

document.addEventListener("DOMContentLoaded", () => {
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth?' +
      'response_type=code' +
      '&client_id=' + GOOGLE_CLIENT_ID  +
      '&redirect_uri=http://localhost:8000/auth/google/callback' +
      '&scope=https://www.googleapis.com/auth/userinfo.email'

    let button = document.getElementById('go')
    if (button) {
        button.addEventListener('click', () => {
          window.location.href = googleAuthUrl
        })
    }
    const form = document.getElementById('create-comment')
    const textarea = document.querySelector("textarea[name='create_comment']")

    if (textarea) {
        textarea.addEventListener('keydown', (event) => {
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault() // prevent newline from being added
            form.submit()// trigger form submission
        }
    })
    }
})
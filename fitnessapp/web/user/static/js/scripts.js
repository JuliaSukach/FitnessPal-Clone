const GOOGLE_CLIENT_ID = '121483820619-lr68ifev2038buns1ite5va1fmibt87i.apps.googleusercontent.com'

document.addEventListener("DOMContentLoaded", () => {
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth?' +
      'response_type=code' +
      '&client_id=' + GOOGLE_CLIENT_ID  +
      '&redirect_uri=http://localhost:8000/auth/google/callback' +
      '&scope=https://www.googleapis.com/auth/userinfo.email'

    document.getElementById('go').addEventListener('click', () => {
      window.location.href = googleAuthUrl
    })
})
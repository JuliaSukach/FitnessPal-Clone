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
    const socket = new WebSocket('ws://localhost:8000/ws')
    const input = document.querySelector('input.messenger[type="text"]')
    const sendButton = document.querySelector('.send-message-btn')
    const messageForm = document.querySelector('#message-form')
    const messagesBox = document.querySelector('.messages-box')
    let recipient_id
    if (input) {
        socket.onopen = function(event) {
            console.log('WebSocket connection established.')
        }
        socket.onerror = function(event) {
            console.log('WebSocket connection error:', event)
        }
        socket.onmessage = function(event) {
            let data = JSON.parse(event.data)
            console.log('Received message:', data)
            let message = document.createElement('div')
            message.classList.add(`chat-message-${data.sender == recipient_id ? 'left' : 'right'}`, 'pb-4')
            message.innerHTML += `<div>
                <img src="https://bootdey.com/img/Content/avatar/avatar1.png" class="rounded-circle mr-1" alt="Chris Wood" width="40" height="40">
                <div class="text-muted small text-nowrap mt-2">2:33 am</div>
            </div>
            <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                <div class="font-weight-bold mb-1">You</div>
                ${data.message}
            </div>`
            messagesBox.appendChild(message)
        }

        // let sendMessage = () => {
        //     let message = 'Hello, server!'
        //     socket.send(message)
        //     console.log('Message sent:', message)
        // }
        // sendButton.addEventListener('click', sendMessage)
        input.addEventListener('keypress', function(event) {
            if (event.keyCode === 13) { // 13 is the Enter key
                const message = input.value
                socket.send(message)
                console.log('Message sent:', message)
                input.value = ''
            }
        })

        messageForm.addEventListener('submit', event => {
            event.preventDefault()

            const formData = new FormData(messageForm)
            const recipientId = formData.get('recipient_id')
            const message = formData.get('message')
            recipient_id = recipientId

            const body = new URLSearchParams({
              recipient_id: recipientId,
              message: message
            })

            fetch(`/messages/${recipientId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: body
            })
            .then(response => {
                console.log('Message sent to server')
                input.value = ''
            })
            .catch(error => {
                console.error('Error sending message to server:', error)
            })
        })
    }
})
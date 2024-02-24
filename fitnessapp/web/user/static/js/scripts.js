const GOOGLE_CLIENT_ID = '121483820619-lr68ifev2038buns1ite5va1fmibt87i.apps.googleusercontent.com'

document.addEventListener("DOMContentLoaded", () => {
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth?' +
      'response_type=code' +
      '&client_id=' + GOOGLE_CLIENT_ID  +
      '&redirect_uri=http://localhost:8000/auth/google/callback' +
      '&scope=https://www.googleapis.com/auth/userinfo.email'

    let button = document.getElementById('go')
    if (button) {
        button.addEventListener('click', (event) => {
            event.preventDefault()
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
            let rec_id = document.getElementsByName("recipient_id")[0].value
            let message = document.createElement('div')
            message.classList.add(`chat-message-${data.sender == rec_id ? 'left' : 'right'}`, 'pb-4')
            message.innerHTML += `<div>
                <img src="https://bootdey.com/img/Content/avatar/avatar3.png" class="rounded-circle mr-1" alt="Chris Wood" width="40" height="40">
                <div class="text-muted small text-nowrap mt-2">${Date.now()}</div>
            </div>
            <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                <div class="font-weight-bold mb-1">${data.sender == rec_id ? data.sender_name : 'You'}</div>
                ${data.message}
            </div>`
            messagesBox.appendChild(message)
        }

        let sendMessage = () => {
            debugger
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
        }

        messageForm.addEventListener('submit', event => {
            event.preventDefault()
            sendMessage()
        })
    }

    const matchedFood = document.querySelectorAll(' li.matched-food')
    for (let i = 0; i < matchedFood.length; i++) {
        matchedFood[i].addEventListener('click', function(event) {
            let oldFoodDesc = document.querySelector('input.food-description')
            if (oldFoodDesc) {
                oldFoodDesc.remove()
                document.querySelector('h3.second').remove()
                document.querySelector('input#food_entry_quantity').remove()
                document.querySelector('select#food_entry_weight_id').remove()
                document.querySelector('p.serving').remove()
                document.querySelector('h3.third').remove()
                document.querySelector('select#food_entry_meal_id').remove()
                document.querySelector('input#update_servings').remove()
            }

            let foodName = document.createElement('input')
            foodName.classList.add('food-description')
            foodName.setAttribute('name', 'food-description')
            foodName.setAttribute('type', 'text')
            foodName.setAttribute('value',event.currentTarget.querySelector('a.search').textContent)


            let secondTitle = document.createElement('h3')
            secondTitle.classList.add('secondary-title', 'second')
            secondTitle.innerText='How much?'

            let foodQ = document.createElement('input')
            foodQ.setAttribute('id','food_entry_quantity')
            foodQ.setAttribute('name','food_entry')
            foodQ.classList.add('text', 'short')
            foodQ.setAttribute('value','1')

            let foodEntry = document.createElement('select')
            foodEntry.setAttribute('id','food_entry_weight_id')
            foodEntry.setAttribute('name','food_entry')
            foodEntry.classList.add('select')

            let option = document.createElement("option")
            option.setAttribute("value", event.currentTarget.querySelector('p.search-nutritional-info').textContent.trim())
            let text = document.createTextNode(event.currentTarget.querySelector('p.search-nutritional-info').textContent)
            option.appendChild(text)
            foodEntry.appendChild(option)

            let serving = document.createElement('p')
            serving.classList.add('serving')
            serving.innerText='serivng of'

            let thirdTitle = document.createElement('h3')
            thirdTitle.classList.add('secondary-title', 'third')
            thirdTitle.innerText='To which meal?'

            let foodMealId = document.createElement('select')
            foodMealId.setAttribute('id','food_entry_meal_id')
            foodMealId.setAttribute('name','food_entry_meal_id')
            foodMealId.classList.add('select')

            let option1 = document.createElement("option")
            option1.setAttribute("value", "0")
            let text1 = document.createTextNode("Breakfast")
            option1.appendChild(text1)
            foodMealId.append(option1)

            let option2 = document.createElement("option")
            option2.setAttribute("value", "1")
            let text2 = document.createTextNode("Lunch")
            option2.appendChild(text2)
            foodMealId.append(option2)

            let option3 = document.createElement("option")
            option3.setAttribute("value", "2")
            let text3 = document.createTextNode("Dinner")
            option3.appendChild(text3)
            foodMealId.append(option3)

            let option4 = document.createElement("option")
            option4.setAttribute("value", "3")
            let text4 = document.createTextNode("Snacks")
            option4.appendChild(text4)
            foodMealId.append(option4)

            let buttonLog = document.createElement('input')
            buttonLog.setAttribute('id','update_servings')
            buttonLog.setAttribute('type','submit')
            buttonLog.classList.add('button', 'log')
            buttonLog.innerHTML='Add Food To Diary'


            let loadedBox = document.querySelector('div#loaded_item')
            loadedBox.append(foodName, secondTitle, foodQ, foodEntry, serving, thirdTitle, foodMealId, buttonLog)
        })
    }

    function deleteMeal(event) {
          event.preventDefault()
          const mealId = event.target.dataset.mealId
          fetch('/food/diary', {
            method: 'delete',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ meal_id: mealId })
          })
          .then(response => {
            if (response.ok) {
              window.location.reload();
            } else {
              alert('Error deleting meal');
            }
          })
          .catch(error => {
            console.error(error);
            alert('Error deleting meal');
          })
    }

    document.querySelectorAll('.delete-meal').forEach(function(element) {
        element.addEventListener('click', deleteMeal)
    })

    const deleteLinks = document.querySelectorAll('.delete-user')
    deleteLinks.forEach(link => {
        link.addEventListener('click', async (event) => {
            event.preventDefault();
            const userId = event.target.dataset.userId
            const response = await fetch(`/profile/${userId}`, { method: 'delete' })
            if (response.ok) {
                console.log('deleted')
                location.reload()
            } else {
                const errorMessage = await response.text();
                alert(`Error deleting user: ${errorMessage}`);
            }
        })
    })

})
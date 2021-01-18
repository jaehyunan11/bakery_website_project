let updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let foodId = this.dataset.food
        let action = this.dataset.action
        console.log('foodId:', foodId, 'Action:', action)

        console.log('User:', user)
        if (user === 'AnonymousUser') {
            console.log('User is not log in')
            // addCookieItem(foodId, action)
        } else {
            updateUserOrder(foodId, action)
            // updateUserOrder(foodId, action)

        }
    })

}

function updateUserOrder(foodId, action) {
    console.log('user is logged in, sending data')

    // Where we want to send item to
    let url = '/update_item/'

    // Where we want to send to (URL), define what kinds of data send to (method=....)
    fetch(url, {
        method: 'POST',
        // data
        headers: {
            'Content-Type': 'application/json',
            // javascript csrf_token
            'X-CSRFToken': csrftoken,
        },
        // send data to view as string 
        body: JSON.stringify({ 'foodId': foodId, 'action': action })
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data:', data)
            // reload page
            location.reload()
        })
}
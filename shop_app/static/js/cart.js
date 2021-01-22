let updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let foodId = this.dataset.food
        let action = this.dataset.action
        console.log('foodId:', foodId, 'Action:', action)

        console.log('User:', user)
        if (user == 'AnonymousUser') {
            addCookieItem(foodId, action)
        } else {
            updateUserOrder(foodId, action)

        }
    })

}

// Update Cookieitem when user add or delete item in cart
function addCookieItem(foodId, action) {
    console.log('User is not log in')

    let selector = document.getElementById('selector');
    let optionValue = selector.value

    if (action == 'add') {
        if (cart[foodId] == undefined) {
            cart[foodId] = { 'quantity': 1 }
        } else {
            cart[foodId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[foodId]['quantity'] -= 1

        if (cart[foodId]['quantity'] <= 0) {
            console.log('Remove Item')
            delete cart[foodId]
        }
    }

    if (action == 'multi-add') {
        if (optionValue == 1) {
            cart[foodId]['quantity'] += 1
        } else if (optionValue == 2) {
            cart[foodId]['quantity'] += 2
        } else if (optionValue == 3) {
            cart[foodId]['quantity'] += 3
        } else if (optionValue == 4) {
            cart[foodId]['quantity'] += 4
        } else {
            cart[foodId]['quantity'] += 5

        }

    }

    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
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
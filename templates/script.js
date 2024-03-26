document.addEventListener('DOMContentLoaded', function() {
    var plusButtons = document.getElementsByClassName('plus-button');
    var minusButtons = document.getElementsByClassName('minus-button');
    var countElements = document.getElementsByClassName('count');
    var cartItems = document.getElementById('cart-items');
    var placeOrderButton = document.getElementById('place-order-button');

    for (var i = 0; i < plusButtons.length; i++) {
        plusButtons[i].addEventListener('click', incrementCounter);
    }

    for (var i = 0; i < minusButtons.length; i++) {
        minusButtons[i].addEventListener('click', decrementCounter);
    }

    function incrementCounter() {
        var countElement = this.parentNode.getElementsByClassName('count')[0];
        var count = parseInt(countElement.innerText);
        var itemName = this.parentNode.parentNode.getElementsByClassName('item-name')[0].innerText;

        count++;
        countElement.innerText = count;

        if (count === 1) {
            // Add item to cart
            var newRow = document.createElement('tr');
            newRow.innerHTML = '<td>' + itemName + '</td><td>' + count + '</td><td>$10</td>';
            cartItems.appendChild(newRow);
        } else {
            // Update quantity in cart
            var cartItem = cartItems.getElementsByTagName('tr');
            for (var i = 0; i < cartItem.length; i++) {
                if (cartItem[i].getElementsByTagName('td')[0].innerText === itemName) {
                    cartItem[i].getElementsByTagName('td')[1].innerText = count;
                    break;
                }
            }
        }
    }

    function decrementCounter() {
        var countElement = this.parentNode.getElementsByClassName('count')[0];
        var count = parseInt(countElement.innerText);
        var itemName = this.parentNode.parentNode.getElementsByClassName('item-name')[0].innerText;

        if (count > 0) {
            count--;
            countElement.innerText = count;

            if (count === 0) {
                // Remove item from cart
                var cartItem = cartItems.getElementsByTagName('tr');
                for (var i = 0; i < cartItem.length; i++) {
                    if (cartItem[i].getElementsByTagName('td')[0].innerText === itemName) {
                        cartItems.removeChild(cartItem[i]);
                        break;
                    }
                }
            } else {
                // Update quantity in cart
                var cartItem = cartItems.getElementsByTagName('tr');
                for (var i = 0; i < cartItem.length; i++) {
                    if (cartItem[i].getElementsByTagName('td')[0].innerText === itemName) {
                        cartItem[i].getElementsByTagName('td')[1].innerText = count;
                        break;
                    }
                }
            }
        }
    }

    placeOrderButton.addEventListener('click', function() {
        alert('Order placed!');
    });
});

document.getElementById("place-order-button").addEventListener("click", function() {
    // Extract cart data from the table and create a JSON object
    var cartItems = [];
    var table = document.getElementById("cart-items");
    var rows = table.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) {
        var item = rows[i].cells[0].innerText;
        var quantity = parseInt(rows[i].cells[1].innerText);
        var price = parseFloat(rows[i].cells[2].innerText.replace("$", ""));
        cartItems.push({
            "item": item,
            "quantity": quantity,
            "price": price
        });
    }

    // Send the cart data to the Flask app using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/order", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(cartItems));
});
const BASE_URL = "http://127.0.0.1:5000";

async function createUser(){

```
const response = await fetch(BASE_URL + "/users",{
    method:"POST",
    headers:{
        "Content-Type":"application/json"
    },
    body:JSON.stringify({
        name:document.getElementById("name").value,
        email:document.getElementById("email").value,
        password:document.getElementById("password").value
    })
});

alert(JSON.stringify(await response.json()));
```

}

async function login(){

```
const response = await fetch(BASE_URL + "/login",{
    method:"POST",
    headers:{
        "Content-Type":"application/json"
    },
    body:JSON.stringify({
        email:document.getElementById("loginEmail").value,
        password:document.getElementById("loginPassword").value
    })
});

const data = await response.json();

document.getElementById("loginResult").innerText =
    JSON.stringify(data,null,2);
```

}

async function loadFoods(){

```
const response = await fetch(BASE_URL + "/foods");
const foods = await response.json();

let html = "";

foods.forEach(food => {

    html += `
    <div class="card">
        <h3>${food.name}</h3>
        <p>Price: ₹${food.price}</p>
        <p>${food.category}</p>
    </div>
    `;
});

document.getElementById("foods").innerHTML = html;
```

}

async function loadRestaurants(){

```
const response = await fetch(BASE_URL + "/restaurants");
const restaurants = await response.json();

let html = "";

restaurants.forEach(r => {

    html += `
    <div class="card">
        <h3>${r.name}</h3>
        <p>${r.cuisine}</p>
        <p>⭐ ${r.rating}</p>
    </div>
    `;
});

document.getElementById("restaurants").innerHTML = html;
```

}

async function addToCart(){

```
const response = await fetch(BASE_URL + "/cart/add",{
    method:"POST",
    headers:{
        "Content-Type":"application/json"
    },
    body:JSON.stringify({
        user_id:Number(document.getElementById("userId").value),
        menu_id:Number(document.getElementById("menuId").value),
        quantity:Number(document.getElementById("quantity").value)
    })
});

alert(JSON.stringify(await response.json()));
```

}

async function checkout(){

```
const userId =
    document.getElementById("checkoutUserId").value;

const response =
    await fetch(BASE_URL + "/checkout/" + userId,{
        method:"POST"
    });

const data = await response.json();

document.getElementById("checkoutResult").innerText =
    JSON.stringify(data,null,2);
```

}

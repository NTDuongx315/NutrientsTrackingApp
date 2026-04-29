function displayNextElement(button) {
    button.nextElementSibling.style.display = 'block';
}

function addFood2NewMeal(button, foodList) {
    // console.log(foodList);
    const form = button.parentElement;
    const lastChild = form.lastElementChild;

    let foodLabel = document.createElement('label');
    foodLabel.innerText = "Food: ";
    let select = document.createElement('select');
    select.name = "food_id";
    select.required = true;
    foodList.forEach(food => {
        let option = document.createElement('option');
        option.value = food.id;
        option.innerText = food.name;
        select.appendChild(option);
    });
    foodLabel.appendChild(select);
    form.insertBefore(foodLabel, lastChild);

    let amountLabel = document.createElement('label');
    amountLabel.innerText = "Amount: ";
    let input = document.createElement('input');
    input.type = "number";
    input.name = "amount";
    input.placeholder = "Amount (g)";
    input.required = true;
    amountLabel.appendChild(input);
    form.insertBefore(amountLabel, lastChild);
}
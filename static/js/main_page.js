window.addEventListener("load", () => {
  const orderTicket = localStorage.getItem("order-summary" || "");
  const orderSummary = document.getElementById("readonly-textarea");
  orderSummary.value = orderTicket;
});

function clearOrderSummary() {
  localStorage.setItem("order-summary", "");
}

function increaseQuantity(productId) {
  const quantity = document.getElementById(`input-${productId}`);
  quantity.value = parseInt(quantity.value) + 1;
}

function decreaseQuantity(productId) {
  const quantity = document.getElementById(`input-${productId}`);
  if (parseInt(quantity.value) > 1) {
    quantity.value = quantity.value - 1;
  }
}

// adds the product to the ordersummary, then submits the order summary
// to save it in the session
function addToOrder(productName, productPrice, productId) {
  const orderSummary = document.getElementById("readonly-textarea");
  const quantity = document.getElementById(`input-${productId}`);

  const quantityInt = parseInt(quantity.value);
  const str = `${quantityInt}\t${productName}\t${(
    quantityInt * parseFloat(productPrice)
  ).toFixed(2)}`;
  quantity.value = 1;
  orderSummary.value += `\n${str}`;
  localStorage.setItem("order-summary", orderSummary.value);
}

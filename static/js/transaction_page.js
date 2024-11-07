document.addEventListener("DOMContentLoaded", () => {
  calculateTotal();
  var timeout = 10000;
  window.setTimeout(sendBackToMainScreen, timeout);
});

function calculateTotal() {
  const prices = document.getElementsByClassName("order-price-li");
  let total = 0;
  for (let price of prices) {
    total += parseFloat(price.textContent);
    console.log(price.textContent);
  }
  const totalSpanElement = document.getElementById("total-cost-span");
  totalSpanElement.textContent = `${total.toFixed(2)}`;
}

function sendBackToMainScreen() {
  window.location = "http://127.0.0.1:5000";
}

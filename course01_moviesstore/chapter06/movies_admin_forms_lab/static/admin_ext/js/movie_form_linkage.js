
(function () {
  // Admin 的表单字段 id 一般是 id_<field>
  const priceEl = document.getElementById("id_price");
  const discountEl = document.getElementById("id_discount");

  // readonly 字段在 Admin 中通常渲染成 <div class="readonly">...</div>
  // 它的容器通常在 #id_final_price 或者包含在 field-final_price 中
  const finalPriceContainer = document.querySelector(".field-final_price .readonly");

  function toNumber(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : 0;
  }

  function calcFinalPrice() {
    const price = toNumber(priceEl ? priceEl.value : 0);
    const discount = toNumber(discountEl ? discountEl.value : 0);

    const safeDiscount = Math.min(Math.max(discount, 0), 90);
    const finalPrice = price * (100 - safeDiscount) / 100;

    if (finalPriceContainer) {
      // 保留两位小数显示
      finalPriceContainer.textContent = finalPrice.toFixed(2);
    }
  }

  function bind() {
    if (priceEl) priceEl.addEventListener("input", calcFinalPrice);
    if (discountEl) discountEl.addEventListener("input", calcFinalPrice);
    calcFinalPrice();
  }

  document.addEventListener("DOMContentLoaded", bind);
})();
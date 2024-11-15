function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
async function dalert(n) {
    await sleep(1000);
    alert(n);
}
var notify = new URLSearchParams(window.location.search).get("notify");
if (notify.length > 5) dalert(notify);
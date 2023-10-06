function onReady(callback) {
  var intervalId = window.setInterval(function() {
    if (document.getElementsByTagName('body')[0] !== undefined) {
      window.clearInterval(intervalId);
      callback.call(this);
    }
  }, 1000);
}

function setVisible(selector, visible) {
  document.querySelector(selector).style.display = visible ? 'block' : 'none';
  document.body.classList.add("stop-scrolling");
}

onReady(function() {
  setVisible('.layout-wrapper', true);
  setVisible('#loading', false);
});
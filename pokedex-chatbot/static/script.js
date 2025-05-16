function sendMessage() {
  const input = document.getElementById("userInput");
  const chatlog = document.getElementById("chatlog");
  const message = input.value.trim();

  if (!message) return;

  chatlog.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
  input.value = "";

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: message })
  })
  .then(res => res.json())
  .then(data => {
    let botMsg = `<div><strong>Bot:</strong><br>${data.text}</div>`;
    if (data.image) {
      botMsg += `<img src="${data.image}" alt="Pokemon Image" class="poke-img">`;
    }
    chatlog.innerHTML += botMsg;
    chatlog.scrollTop = chatlog.scrollHeight;
  });
}
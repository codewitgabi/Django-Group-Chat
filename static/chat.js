const form = document.querySelector("#chat-form");
const messageBox = document.querySelector("#chat-messages");
const protocol = window.location.protocol === "https:" ? "wss": "ws";
const ws_url = `${protocol}://${window.location.host}/chat/${group_id}/`;

// Websocket instance
const chat_socket = new WebSocket(ws_url);


chat_socket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  let output = "";

  if (data.type === "group_messages") {
    const messages = data.messages;
    for (let message of messages) {
      output += (message.sender === user) ?
      `<div class="sender">
      <p>${message.message}</p>
      <small class="date-sent">${ new Date(message.time_created).toDateString() }</small>
      </div>`:
      `<div class="receiver">
      <h4 class="username">@${ message.sender }</h4>
      <p>${ message.message }</p>
      <small class="date-sent">${ new Date(message.time_created).toDateString() }</small>
      </div>`
    }
    messageBox.innerHTML = output;
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const message = e.target.message.value;

  chat_socket.send(JSON.stringify({
    "message": message
  }))

  form.reset();
})
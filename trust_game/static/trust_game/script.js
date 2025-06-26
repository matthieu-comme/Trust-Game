// Fonction pour mettre à jour le timer du chat
function updateChatTimer() {
  updateTimeRemaining();
  document.getElementById("time_remaining").textContent = timeRemaining;

  if (timeRemaining <= 0) {
    clearInterval(chatTimer);
    disableChat(true);
  }
}

function updateTimeRemaining() {
  const now = Date.now() / 1000;
  timeRemaining = Math.max(parseInt(expireTime - now), 0);
}

// Fonction pour désactiver le chat
function disableChat(is_expired) {
  // is_expired : boolean = true si temps écoulé, faux si c'est le joueur A qui a envoyé
  const placeholder = is_expired
    ? "Temps écoulé"
    : "Joueur A a pris sa décision";
  if (has_cheap_talk) setDisabled(inputCheapTalk, buttonCheapTalk, placeholder);

  if (has_chat_gpt) setDisabled(inputGPT, buttonGPT, placeholder);
}
// désactive les composants du chat
function setDisabled(input, button, placeholder) {
  input.disabled = true;
  button.disabled = true;
  input.placeholder = placeholder;
}

// Fonctions pour envoyer un message
function sendChatMessageCheapTalk(message) {
  playerPrefix = roleIsPlayerA ? "Joueur A" : "Joueur B";
  if (isTyping) doneTyping();

  return { message: message, player_type: playerPrefix };
}

function sendChatMessageGPT(message, playerPrefix) {
  const chatBoxGPT = document.getElementById("chatbox-gpt");
  const messageHTML = `${playerPrefix}${message}<br>`;
  chatBoxGPT.innerHTML += messageHTML;
  chatBoxGPT.scrollTop = chatBoxGPT.scrollHeight;

  return { message: message, is_chat_gpt: true };
}

// playerPrefix nécessaire en cas d'appel pour chatgpt
function sendChatMessage(input, playerPrefix = null) {
  const message = input.value.trim();
  let dataToSend;

  if (!message) return;

  if (playerPrefix == null) dataToSend = sendChatMessageCheapTalk(message);
  else dataToSend = sendChatMessageGPT(message, playerPrefix);

  input.value = "";
  input.focus();

  liveSend(dataToSend);
}

// Fonctions pour gérer l'indicateur de frappe
function doneTyping() {
  isTyping = false;
  liveSend({ typing_status: false });
  clearTimeout(typingTimer);
}

// reconstruis les data et les envoie en cas de refresh
function refreshFromSavedData() {
  const amount_sent = js_vars.amount_sent;
  const amount_sent_back = js_vars.amount_sent_back;

  if (amount_sent != null) {
    disableChat(false);
    const data_sent = { status: "sent", amount_sent: amount_sent };
    const data_received = {
      status: "received",
      amount_sent: amount_sent,
      tripled_amount: amount_sent * js_vars.multiplier,
    };
    liveRecv(data_sent);
    liveRecv(data_received);
  }

  if (amount_sent_back != null) {
    const data_complete = {
      status: "complete",
      can_proceed: true,
      amount_sent: amount_sent,
      amount_sent_back: amount_sent_back,
      tripled_amount: amount_sent * js_vars.multiplier,
    };
    liveRecv(data_complete);
  }
}

// fonctions d'envoi de jetons
function sendTokens() {
  const amountInput = document.getElementById("amount_input");
  const amount = parseInt(amountInput.value);

  if (isNaN(amount) || amount < 0 || amount > js_vars.endowment) {
    amountInput.classList.add("is-invalid");
    return;
  }

  amountInput.classList.remove("is-invalid");
  liveSend({ amount_sent: amount });

  document.getElementById("send_button").disabled = true;
  document.getElementById("sent_amount").textContent = amount;
  document.getElementById("waiting_message").classList.remove("d-none");
}

function sendTokensBack() {
  const amountBackInput = document.getElementById("amount_back_input");
  const maxAmount = parseInt(
    document.getElementById("tripled_amount_1").textContent
  );
  const amountBack = parseInt(amountBackInput.value);

  if (isNaN(amountBack) || amountBack < 0 || amountBack > maxAmount) {
    amountBackInput.classList.add("is-invalid");
    return;
  }

  amountBackInput.classList.remove("is-invalid");
  liveSend({ amount_sent_back: amountBack });
  document.getElementById("send_back_button").disabled = true;
}

// Fonction pour mettre à jour les résultats finaux

function resultsPlayerA(data) {
  const resultsDiv = document.getElementById("final_results_content");
  const amountSent = data.amount_sent;
  const amountReceived = data.amount_sent_back;
  const finalBalance = js_vars.endowment - amountSent + amountReceived;

  resultsDiv.innerHTML = `
        <p>Vous avez envoyé ${amountSent} jetons au Joueur B.</p>
        <p>Le Joueur B vous a renvoyé ${amountReceived} jetons.</p>
        <p><strong>Votre solde final: ${finalBalance} jetons</strong></p>
      `;
}

function resultsPlayerB(data) {
  const resultsDiv = document.getElementById("final_results_content");
  const amountReceived = data.amount_sent;
  const tripledAmount = data.tripled_amount;
  const amountSentBack = data.amount_sent_back;
  const finalBalance = tripledAmount - amountSentBack;

  resultsDiv.innerHTML = `
        <p>Vous avez reçu ${tripledAmount} jetons (${amountReceived} × ${js_vars.multiplier}).</p>
        <p>Vous avez renvoyé ${amountSentBack} jetons au Joueur A.</p>
        <p><strong>Votre solde final: ${finalBalance} jetons</strong></p>
      `;
}

function updateFinalResults(data) {
  if (roleIsPlayerA) resultsPlayerA(data);
  else resultsPlayerB(data);
}

// Gestion des messages live

function handleChatGPTReply(data) {
  const chatBoxGPT = document.getElementById("chatbox-gpt");
  const reply = data.reply;
  chatBoxGPT.innerHTML += `${data.bot_prefix}${reply}<br>`;
  chatBoxGPT.scrollTop = chatBoxGPT.scrollHeight;
}

function handleNewMessage(data) {
  const chatHistory = document.getElementById("chat_history");
  const newMessage = data.new_message;

  chatHistory.innerHTML += newMessage;
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

function handleTypingIndicator(data) {
  const typingIndicator = document.getElementById("typing_indicator");
  if (data.other_player_typing) {
    typingIndicator.classList.remove("d-none");
  } else {
    typingIndicator.classList.add("d-none");
  }
}

function handleSentStatus(data) {
  disableChat(false);
  document.getElementById("send_button").disabled = true;
  document.getElementById("sent_amount").textContent = data.amount_sent;
  document.getElementById("waiting_message").classList.remove("d-none");
}

function handleReceivedStatus(data) {
  disableChat(false);
  document.getElementById("waiting_for_A").classList.add("d-none");
  document.getElementById("received_amount_display").classList.remove("d-none");
  document.getElementById("received_amount").textContent = data.amount_sent;
  document.getElementById("tripled_amount_1").textContent = data.tripled_amount;
  document.getElementById("tripled_amount_2").textContent = data.tripled_amount;
  document.getElementById("amount_back_input").max = data.tripled_amount;
}

function handleCompleteStatus(data) {
  canProceed = data.can_proceed;
  document.getElementById("game_results").classList.remove("d-none");
  updateFinalResults(data);
  if (canProceed) document.getElementById("proceed_button").disabled = false;
}

function liveRecv(data) {
  if (data.is_chat_gpt) handleChatGPTReply(data);
  if (data.new_message) handleNewMessage(data);
  if (data.hasOwnProperty("other_player_typing")) handleTypingIndicator(data);
  if (data.status === "sent" && roleIsPlayerA) handleSentStatus(data);
  if (data.status === "received" && !roleIsPlayerA) handleReceivedStatus(data);
  if (data.status === "sent" || data.status === "received")
    document.getElementById("time").classList.add("d-none");
  if (data.status === "complete") handleCompleteStatus(data);
}

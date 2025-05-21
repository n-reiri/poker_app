(() => {
  const roomId = JSON.parse(document.getElementById("room-id").textContent);
  const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
  const chatSocket = new WebSocket(
    `${wsScheme}://${window.location.host}/ws/rooms/${roomId}/`
  );

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    // data: { player_id, action, amount, chips }
    console.log("Received:", data);

    // チップ数を更新
    const el = document.querySelector(`#player-${data.player_id} .chips`);
    if (el) {
      el.textContent = data.chips;
    }

    // (任意) アクション履歴に追記する例
    // const historyDiv = document.getElementById('history');
    // historyDiv.innerHTML += `<p>${data.action} ${data.amount || ''}</p>`;
  };

  chatSocket.onclose = function (e) {
    console.error("WebSocket closed unexpectedly");
  };

  // アクションボタンにイベントをバインド
  document.querySelectorAll(".action-button").forEach((btn) => {
    btn.onclick = () => {
      const action = btn.dataset.action;
      const amount = document.getElementById("bet-amount")?.value || 0;
      chatSocket.send(JSON.stringify({ action, amount }));
    };
  });
})();

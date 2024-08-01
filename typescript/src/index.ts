// src/index.ts

// 関数1: テキストを変更する
function changeText() {
  const appDiv: HTMLElement | null = document.getElementById('app');
  if (appDiv) {
    appDiv.innerText = "Text has been changed!";
  }
}

// 関数2: コンソールにメッセージを表示する
function logMessage() {
  console.log("Button was clicked!");
}

// 関数3: 背景色を変更する
function changeBackgroundColor() {
  document.body.style.backgroundColor = "lightblue";
}

// 関数4APIサーバーにメッセージを送信する
async function postRequest(url: string, data: any): Promise<any> {
  try {
      const response = await fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      });
      console.log(JSON.stringify(data));
      if (!response.ok) {
          throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      return result;
  } catch (error) {
      console.error('Error:', error);
      throw error;
  }
}


document.addEventListener('DOMContentLoaded', () => {
  const changeTextButton: HTMLButtonElement | null = document.querySelector('#changeTextButton');
  const logMessageButton: HTMLButtonElement | null = document.querySelector('#logMessageButton');
  const changeBgColorButton: HTMLButtonElement | null = document.querySelector('#changeBgColorButton');
  const postRequestToAPI: HTMLButtonElement | null = document.querySelector('#postRequestToAPI');

  if (changeTextButton) {
    changeTextButton.addEventListener('click', changeText);
  }

  if (logMessageButton) {
    logMessageButton.addEventListener('click', logMessage);
  }

  if (changeBgColorButton) {
    changeBgColorButton.addEventListener('click', changeBackgroundColor);
  }

  if (postRequestToAPI) {
    postRequestToAPI.addEventListener('click', () => {
      const url = 'http://127.0.0.1:8000/publish'
      const data = {
        spam: 'World!!',
        message: 'Hello!',
        data: '安西雄一郎'
    };
      console.log(data)
      const startTime = Date.now();
      postRequest(url,data);
      const endTime = Date.now();
      console.log(`Message ${data} published.`);
      console.log(`Message publishing took ${endTime - startTime}ms.`);
    });
  }
});

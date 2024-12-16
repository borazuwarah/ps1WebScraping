console.log("background.js está funcionando");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'getCurrentUrl') {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            const currentUrl = tabs[0].url;
            console.log("La URL actual es: " + currentUrl);  // Verifica que la URL está siendo obtenida
            sendResponse({ url: currentUrl });
        });
        return true; // Esto asegura que la respuesta sea asincrónica
    }
});
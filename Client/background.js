// // Function to send a message to the content script
// function sendMessageToContentScript() {
//     chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
//         if (tabs.length > 0) {
//             var tab = tabs[0];
//             console.log("hello",tab.url);
//             chrome.tabs.sendMessage(tab.id, { message: "Hello from background.js!", url: tab.url });
//         }
//     });
// }

// // Add listener for onInstalled event
// chrome.runtime.onInstalled.addListener(function () {
//     sendMessageToContentScript();
// });

// // Add listener for onUpdated event
// chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
//     if (changeInfo.status === "complete" && tab.active) {
//         sendMessageToContentScript();
//     }
// });
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    if (changeInfo.status == 'complete') {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            var url = tabs[0].url;
            if (isGitHubRepository(url)) {
                chrome.tabs.sendMessage(tabId, { message: 'github_repo_url', url: url });
            }
            
        });
    }
});

function isGitHubRepository(url) {
    // Implement a logic to check if the given URL is a GitHub repository URL
    // For example:
    return /^https:\/\/github\.com\/[\w\-]+\/[\w\-]+\/issues(\/\d+)?\/?$/.test(url);
}

// threshold_score = 0.75


// parcelRequire = (function (modules, cache, entry, globalName) {
//   // Save the require from previous bundle to this closure if any
//   var previousRequire = typeof parcelRequire === "function" && parcelRequire;
//   var nodeRequire = typeof require === "function" && require;


//   // background.js

//   // // Create a listener for when the active tab changes
//   // chrome.tabs.onActivated.addListener(function(activeInfo) {
//   //   // Get details of the current tab
//   //   chrome.tabs.get(activeInfo.tabId, function(tab) {
//   //       // Log the URL of the current tab
//   //       console.log("Current URL:", tab.url);
//   //       // You can use tab.url in any way you want here
//   //   });
//   // });




//   function newRequire(name, jumped) {
//     if (!cache[name]) {
//       if (!modules[name]) {
//         var currentRequire =
//           typeof parcelRequire === "function" && parcelRequire;
//         if (!jumped && currentRequire) {
//           return currentRequire(name, true);
//         }

//         if (previousRequire) {
//           return previousRequire(name, true);
//         }

//         if (nodeRequire && typeof name === "string") {
//           return nodeRequire(name);
//         }

//         var err = new Error("Cannot find module '" + name + "'");
//         err.code = "MODULE_NOT_FOUND";
//         throw err;
//       }

//       localRequire.resolve = resolve;
//       localRequire.cache = {};

//       var module = (cache[name] = new newRequire.Module(name));

//       modules[name][0].call(
//         module.exports,
//         localRequire,
//         module,
//         module.exports,
//         this
//       );
//     }

//     return cache[name].exports;

//     function localRequire(x) {
//       return newRequire(localRequire.resolve(x));
//     }

//     function resolve(x) {
//       return modules[name][1][x] || x;
//     }
//   }

//   function Module(moduleName) {
//     this.id = moduleName;
//     this.bundle = newRequire;
//     this.exports = {};
//   }

//   newRequire.isParcelRequire = true;
//   newRequire.Module = Module;
//   newRequire.modules = modules;
//   newRequire.cache = cache;
//   newRequire.parent = previousRequire;
//   newRequire.register = function (id, exports) {
//     modules[id] = [
//       function (require, module) {
//         module.exports = exports;
//       },
//       {},
//     ];
//   };

//   var error;
//   for (var i = 0; i < entry.length; i++) {
//     try {
//       newRequire(entry[i]);
//     } catch (e) {
//       if (!error) {
//         error = e;
//       }
//     }
//   }

//   if (entry.length) {
//     var mainExports = newRequire(entry[entry.length - 1]);

//     if (typeof exports === "object" && typeof module !== "undefined") {
//       module.exports = mainExports;
//     } else if (typeof define === "function" && define.amd) {
//       define(function () {
//         return mainExports;
//       });
//     } else if (globalName) {
//       this[globalName] = mainExports;
//     }
//   }

//   parcelRequire = newRequire;

//   if (error) {
//     throw error;
//   }

//   return newRequire;
// })(
//   {
//     "sotagger.js": [
//       function (require, module, exports) {
//         /**
//          * Getting toxicity values
//          * @param {String} send_data Segregating toxic/abusive words
//          * @returns  response (object array)
//          */
//         async function getResult(send_data) {
//           const options = {
//             method: "POST",
//             headers: {
//               Accept: "application/json",
//               "Content-Type": "application/json",
//             },
//             body: JSON.stringify(send_data), // Assuming your endpoint expects a string directly
//           };

//           try {
//             const response = await fetch("http://127.0.0.1:5000/predict", options);
//             const data = await response.json();

//             // Handle the result as needed
//             console.log("Result:", data.result * data.probability);
//             console.log("Probability:", data.probability);

//             return data.result * data.probability;
//           } catch (error) {
//             console.error("Error:", error);
//             throw error;
//           }
//         }

//         /**
//          * Generating sentences
//          * @param {String} send_data
//          * @returns response (object)
//          */
//         async function genResult(send_data) {
//           const options = {
//             method: "POST",
//             headers: {
//               Accept: "application/json",
//               "Content-Type": "application/json",
//             },
//             body: JSON.stringify(send_data),
//           };

//           try {
//             const response = await fetch("http://127.0.0.1:5000/suggest", options);
//             const data = await response.json();

//             // Handle the result as needed
//             console.log("Result:", data.result);

//             return data.result;
//           } catch (error) {
//             console.error("Error:", error);
//             throw error;
//           }
//         }

//         /**
//          * Generating sentences
//          * @param {String} send_data
//          * @returns response (object)
//          */
//         async function getreposcore_s(send_data) {
//           const options = {
//             method: "POST",
//             headers: {
//               Accept: "application/json",
//               "Content-Type": "application/json",
//             },
//             body: JSON.stringify(send_data),
//           };

//           try {
//             const response = await fetch("http://127.0.0.1:5000/repocheck", options);
//             const data = await response.json();

//             // Handle the result as needed
//             console.log("Result:", data.result);

//             return data.result;
//           } catch (error) {
//             console.error("Error:", error);
//             throw error;
//           }
//         }

//         /**
//          * MAIN CODE STARTS FROM HERE
//          */
//         function main() {
//           /**
//            * Suggestion Panel
//            */
//           var suggestPanel = document.createElement("div");
//           suggestPanel.style.position = "fixed";
//           suggestPanel.style.fontSize = "15px";
//           suggestPanel.style.borderRadius = "15px";
//           suggestPanel.style.right = "100px";
//           suggestPanel.style.bottom = "10px";
//           suggestPanel.style.backgroundColor = "white";
//           suggestPanel.style.zIndex = 1000;
//           suggestPanel.style.visibility = "visible";
//           suggestPanel.style.width = "300px";
//           suggestPanel.style.width = "300px";
//           suggestPanel.style.height = "100px";
//           suggestPanel.style.padding = "10px";
//           suggestPanel.style.border = "1px solid black";
//           suggestPanel.style.overflow = "auto"; // make panel scrollable
//           suggestPanel.style.maxHeight = "2000px"; // set max height for panel

//           /**
//            * Chart Properties
//            */
//           var chartdiv = document.createElement("canvas");
//           chartdiv.style.position = "fixed";
//           chartdiv.style.borderRadius = "20px";
//           chartdiv.style.right = "10px";
//           chartdiv.style.top = "30px";
//           chartdiv.style.height = "300px";
//           chartdiv.style.overflow = "scroll";
//           chartdiv.style.width = "600px";
//           chartdiv.id = "chartid";
//           chartdiv.style.backgroundColor = "white";
//           chartdiv.style.color = "black";
//           chartdiv.style.border = "none";
//           chartdiv.style.padding = "8px";
//           chartdiv.style.zIndex = 2000;
//           chartdiv.style.visibility = "visible";
//           chartdiv.style.border = "1px solid white";
//           chartdiv.style.maxHeight = "600px";
//           chartdiv.style.maxWidth = "600px";

//           /**
//            * Chart Div Button
//            */
//           var chartdivbutton = document.createElement("button");
//           chartdivbutton.style.position = "fixed";
//           chartdivbutton.style.borderRadius = "20px";
//           chartdivbutton.style.right = "10px";
//           chartdivbutton.style.top = "5px";
//           chartdivbutton.style.backgroundColor = "white";
//           chartdivbutton.style.color = "black";
//           chartdivbutton.style.border = "none";
//           chartdivbutton.style.padding = "8px";
//           chartdivbutton.style.zIndex = 1000;
//           chartdivbutton.innerText = "Show Toxicity Scale";
//           chartdivbutton.style.visibility = "visible";
//           chartdivbutton.style.border = "1px solid black";
//           chartdivbutton.addEventListener("click", function () {
//             if (chartdiv.style.visibility == "visible") {
//               chartdiv.style.visibility = "visible";
//             } else {
//               chartdiv.style.visibility = "visible";
//             }
//           });

//           /**
//            * Suggest button
//            */
//           var suggestButton = document.createElement("button");
//           suggestButton.style.position = "fixed";
//           suggestButton.style.borderRadius = "20px";
//           suggestButton.style.right = "10px";
//           suggestButton.style.bottom = "10px";
//           suggestButton.style.backgroundColor = "blue";
//           suggestButton.style.color = "white";
//           suggestButton.style.border = "none";
//           suggestButton.style.padding = "8px";
//           suggestButton.style.zIndex = 1000;
//           suggestButton.innerText = "Suggest";
//           suggestButton.style.visibility = "visible";
//           suggestButton.style.border = "1px solid yellow";
//           suggestButton.addEventListener("click", function () {
//             if (suggestPanel.style.visibility == "visible") {
//               suggestPanel.style.visibility = "visible";
//             } else {
//               suggestPanel.style.visibility = "visible";
//             }
//           });

//           /**
//            * Highlight Button
//            */
//           var highlightButton = document.createElement("button");
//           highlightButton.style.position = "fixed";
//           highlightButton.style.borderRadius = "20px";
//           highlightButton.style.right = "15px";
//           highlightButton.style.bottom = "50px";
//           highlightButton.style.backgroundColor = "green";
//           highlightButton.style.color = "white";
//           highlightButton.style.border = "none";
//           highlightButton.style.padding = "8px";
//           highlightButton.style.zIndex = 1000;
//           highlightButton.innerText = "Search";
//           highlightButton.style.visibility = "visible";
//           highlightButton.style.border = "1px solid blue";

//           /**
//            * Hover button
//            * pops up above the currently hovered element
//            */
//           var hoverButton = document.createElement("button");
//           hoverButton.style.position = "fixed";
//           hoverButton.style.borderRadius = "50%";
//           hoverButton.style.right = "400px";
//           hoverButton.style.bottom = "10px";
//           hoverButton.style.backgroundColor = "red";
//           hoverButton.style.color = "white";
//           hoverButton.style.border = "none";
//           hoverButton.style.padding = "8px";
//           hoverButton.style.zIndex = 1000;
//           hoverButton.innerText = "!!";
//           hoverButton.style.visibility = "visible";
//           hoverButton.style.border = "1px solid yellow";

//           /**
//            * Toggle suggest panel
//            */
//           hoverButton.addEventListener("click", function () {
//             if (suggestPanel.style.visibility == "visible") {
//               suggestPanel.style.visibility = "visible";
//             } else {
//               suggestPanel.style.visibility = "visible";
//             }
//           });

//           /**
//            * Check Button
//            * pops up above the currently hovered element
//            */
//           var checkButton = document.createElement("button");
//           checkButton.style.position = "fixed";
//           checkButton.style.borderRadius = "50%";
//           checkButton.style.right = "400px";
//           checkButton.style.bottom = "10px";
//           checkButton.style.backgroundColor = "blue";
//           checkButton.style.color = "white";
//           checkButton.style.border = "none";
//           checkButton.style.padding = "8px";
//           checkButton.style.zIndex = 1000;
//           checkButton.innerText = "C";
//           checkButton.style.visibility = "visible";
//           checkButton.style.border = "1px solid yellow";
//           document.body.append(chartdivbutton);
//           document.body.appendChild(chartdiv);
//           document.body.appendChild(suggestButton);
//           document.body.appendChild(highlightButton);
//           document.body.appendChild(suggestPanel);
//           document.body.appendChild(hoverButton);
//           document.body.appendChild(checkButton);

//           /**
//            * refering to currently listened element
//            */
//           var currentElement = null;
//           /**
//            * using set to store target sentences
//            */
//           const target_sentences = new Set();
//           /**
//            * state for managing flow in different sites
//            */
//           var currentState = 0;

//           /**
//            * On input event
//            */
//           window.addEventListener("input", async function () {
//             // TODO OPTIONAL : Intensity based coloring scheme
//             // TODO OPTIONAL: Separate non-relevant text to words for phrases

//             suggestPanel.innerHTML = "";

//             /**
//              * the collection of elements having input class
//              */
//             const collection1 = document.getElementsByClassName(
//               "Am Al editable LW-avf tS-tW"
//             );

//             const array1 = [...collection1];

//             const elementlist = array1;

//             if (
//               elementlist != null &&
//               elementlist[0] != null &&
//               elementlist[0].innerText.length > 0
//             ) {
//               /**
//                * state for gmail
//                */
//               currentState = 0;
//               currentElement = elementlist[0];

//               // TODO LATER: Preprocessing

//               text = elementlist[0].innerText;

//               // TODO LATER: Context - based phrase tokenization

//               /**
//                * regex pattern to tokenize the sentences
//                */
//               const regex = /(?<=\.|\?|\!)\s+/;
//               const sentences = text.split(regex);

//               // TODO LATER: Context based paragaphs/ group of sentences

//               /**
//                * iterating over the sentences and appending target (toxic) sentences
//                */
//               for (let j = 0; j < sentences.length - 1; j++) {
//                 const currentSentence = sentences[j];

//                 var data = JSON.stringify({
//                   inputs: currentSentence,
//                 });

//                 await getResult(data).then((ans) => {
//                   console.log(ans);

//                   // * Defining the score metric *//
//                   let score = ans;
//                   // let obscene_score = 0.0;
//                   // let insult_score = 0.0;
//                   // let identity_hate_score = 0.0;
//                   // let severley_toxic_score = 0.0;
//                   // let threat_score = 0.0;
//                   // let score = 0.0;
//                   // let value = 0;
//                   // for (let j = 0; j < 6; j++) {
//                   //   if (!ans) {
//                   //     break;
//                   //   }
//                   //   if (ans[j].label === "toxic") toxic_score += ans[j].score;
//                   //   else if (ans[j].label === "obscene")
//                   //     obscene_score += ans[j].score;
//                   //   else if (ans[j].label === "insult")
//                   //     insult_score += ans[j].score;
//                   //   else if (ans[j].label === "identity_hate")
//                   //     identity_hate_score += ans[j].score;
//                   //   else if (ans[j].label === "severe_toxic")
//                   //     severley_toxic_score += ans[j].score;
//                   //   else if (ans[j].label === "threat")
//                   //     threat_score += ans[j].score;

//                   //   score += ans[j].score;
//                   // }

//                   /**
//                    * hardcoded parameter for toxicity scale
//                    */
//                   if (score >= threshold_score) {
//                     target_sentences.add(currentSentence);
//                   }
//                 });
//               }

//               hoverButton.style.visibility = "visible";
//               highlightButton.style.visibility = "visible";
//               if (target_sentences.size != 0) {
//                 suggestButton.style.visibility = "visible";
//                 highlightButton.style.visibility = "visible";
//               } else {
//                 suggestButton.style.visibility = "visible";
//                 highlightButton.style.visibility = "visible";
//                 return;
//               }
//             }
//           });

//           /**
//            * Events for Github Comment field
//            */
//           window.addEventListener("input", async function () {
//             suggestPanel.innerHTML = "";
//             const element = document.getElementById("new_comment_field");
//             if (element != null) {
//               /**
//                * state for github
//                */
//               currentState = 1;
//               currentElement = element;
//               /**
//                * setting up according to github dark theme
//                */
//               suggestButton.style.backgroundColor = "white";
//               suggestButton.style.color = "black";
//               suggestButton.style.border = "1px solid blue";

//               text = element.value;

//               const regex = /(?<=\.|\?|\!)\s+/;
//               const sentences = text.split(regex);

//               for (let j = 0; j < sentences.length - 1; j++) {
//                 const currentSentence = sentences[j];

//                 var data = JSON.stringify({
//                   inputs: currentSentence,
//                 });

//                 await getResult(data).then((ans) => {
//                   console.log(ans);
//                   // // * Defining the score metric *//
//                   // let toxic_score = 0.0;
//                   // let obscene_score = 0.0;
//                   // let insult_score = 0.0;
//                   // let identity_hate_score = 0.0;
//                   // let severley_toxic_score = 0.0;
//                   // let threat_score = 0.0;
//                   let score = ans;
//                   // let value = 0;
//                   // for (let j = 0; j < 6; j++) {
//                   //   if (!ans) {
//                   //     break;
//                   //   }
//                   //   if (ans[j].label === "toxic") toxic_score += ans[j].score;
//                   //   else if (ans[j].label === "obscene")
//                   //     obscene_score += ans[j].score;
//                   //   else if (ans[j].label === "insult")
//                   //     insult_score += ans[j].score;
//                   //   else if (ans[j].label === "identity_hate")
//                   //     identity_hate_score += ans[j].score;
//                   //   else if (ans[j].label === "severe_toxic")
//                   //     severley_toxic_score += ans[j].score;
//                   //   else if (ans[j].label === "threat")
//                   //     threat_score += ans[j].score;

//                   //   score += ans[j].score;
//                   // }

//                   if (score >= threshold_score) {
//                     target_sentences.add(currentSentence);
//                   }
//                 });
//               }

//               hoverButton.style.visibility = "visible";
//               suggestPanel.style.visibility = "visible";
//               highlightButton.style.visibility = "visible";
//               if (target_sentences.size != 0) {
//                 suggestButton.style.visibility = "visible";
//                 if (currentState == 0)
//                   highlightButton.style.visibility = "visible";
//               } else {
//                 suggestButton.style.visibility = "visible";
//                 highlightButton.style.visibility = "visible";
//                 return;
//               }
//             }
//           });

//           /**
//            * Gmail highlight feature
//            */
//           highlightButton.addEventListener("click", function () {
//             const collection1 = document.getElementsByClassName(
//               "Am Al editable LW-avf tS-tW"
//             );

//             const array1 = [...collection1];

//             const elementlist = array1;

//             if (currentState != 0) {
//               return;
//             }
//             /**
//              * Handling text to span conversion (recursive)
//              */
//             for (const sentence of target_sentences) {
//               newtext = elementlist[0].innerText;
//               /**
//                * Handling recursive additions
//                */
//               let spanRegex = new RegExp(sentence, "g");
//               newtext = newtext.replaceAll(
//                 spanRegex,
//                 `<span style='text-decoration: underline red;'>${sentence}</span>`
//               );
//               elementlist[0].innerHTML = newtext;
//             }
//           });

//           /**
//            * Gmail Suggest feature
//            */
//           suggestButton.addEventListener("click", async function () {
//             if (currentState != 0) return;
//             suggestPanel.innerHTML = "";
//             for (const sentence of target_sentences) {
//               var sentence_data = JSON.stringify({
//                 inputs: sentence,
//               });
//               let suggestion = "";
//               await genResult(sentence_data).then((ans) => {
//                 console.log(ans);
//                 // if (ans) suggestion = ans.generated_text;
//                 if (ans) suggestion = ans;
//                 else suggestion = sentence;
//               });

//               if (suggestion === sentence || sentence == suggestion) {
//                 suggestion = " ";
//               }

//               var suggestPanelText = document.createElement("div");
//               suggestPanelText.innerText = "Text : " + sentence;
//               if (suggestion === " ")
//                 suggestPanelText.innerText +=
//                   "\nSuggestion : (Better to remove it)";
//               /**
//                * this would be the suggested phrase
//                */ else
//                 suggestPanelText.innerText += "\nSuggestion : " + suggestion;
//               suggestPanelText.style.marginBottom = "10px";
//               suggestPanelText.style.padding = "5px";
//               suggestPanel.appendChild(suggestPanelText);

//               /**
//                * Panel Buttons
//                */
//               var suggestPanelButton = document.createElement("button");
//               suggestPanelButton.innerText = "Close";
//               suggestPanelButton.style.backgroundColor = "red";
//               suggestPanelButton.style.color = "white";
//               suggestPanelButton.style.fontSize = "15px";
//               suggestPanelButton.style.border = "none";
//               suggestPanelButton.style.padding = "5px";
//               suggestPanelButton.addEventListener("click", function () {
//                 suggestPanel.style.visibility = "visible";
//               });
//               suggestPanelButton.style.marginRight = "20px";
//               suggestPanelButton.style.bottom = "2px";
//               suggestPanelButton.style.top = "2px";
//               suggestPanel.appendChild(suggestPanelButton);

//               var suggestPanelButton1 = document.createElement("button");
//               suggestPanelButton1.innerText = "Replace";
//               suggestPanelButton1.style.backgroundColor = "red";
//               suggestPanelButton1.style.color = "white";
//               suggestPanelButton1.style.fontSize = "15px";
//               suggestPanelButton1.style.border = "none";
//               suggestPanelButton1.style.padding = "5px";
//               suggestPanelButton1.style.bottom = "2px";
//               suggestPanelButton1.style.top = "2px";

//               /**
//                * Handling span to text conversion (non-recursive)
//                */
//               suggestPanelButton1.addEventListener("click", function () {
//                 if (currentElement != null) {
//                   if (
//                     currentElement.innerHTML.includes(
//                       `<span style="text-decoration: underline red;">${sentence}</span>`
//                     )
//                   ) {
//                     let text = currentElement.innerHTML;
//                     let newText = text.replaceAll(
//                       `<span style="text-decoration: underline red;">${sentence}</span>`,
//                       suggestion
//                     );
//                     currentElement.innerHTML = newText;
//                     target_sentences.delete(sentence);
//                   } else if (currentElement.innerHTML.includes(sentence)) {
//                     let text = currentElement.innerHTML;
//                     let newText = text.replaceAll(sentence, suggestion);
//                     currentElement.innerHTML = newText;
//                     target_sentences.delete(sentence);
//                   }
//                 }
//               });
//               suggestPanel.appendChild(suggestPanelButton1);
//             }
//           });

//           /**
//            * Events for suggest button for gmail
//            */
//           suggestButton.addEventListener("click", async function () {
//             if (currentState != 1) return;
//             suggestPanel.innerHTML = "";
//             /**
//              * syled as per github page
//              */
//             suggestPanel.style.backgroundColor = "#161b22";
//             suggestPanel.style.border = "0.5px solid #7d8590";

//             for (const sentence of target_sentences) {
//               var sentence_data = JSON.stringify({
//                 inputs: sentence,
//               });
//               let suggestion = "";
//               await genResult(sentence_data).then((ans) => {
//                 console.log(ans);
//                 // if (ans) suggestion = ans.generated_text;
//                 if (ans) suggestion = ans;
//                 else suggestion = sentence;
//               });

//               if (suggestion === sentence || sentence == suggestion) {
//                 suggestion = " ";
//               }

//               var suggestPanelText = document.createElement("div");
//               suggestPanelText.innerText = "Text : " + sentence;
//               if (suggestion === " ")
//                 suggestPanelText.innerText +=
//                   "\nSuggestion : (Better to remove it)";
//               /**
//                * this would be the suggested phrase
//                */ else
//                 suggestPanelText.innerText += "\nSuggestion : " + suggestion;
//               suggestPanelText.style.marginBottom = "10px";
//               suggestPanelText.style.padding = "5px";
//               suggestPanel.appendChild(suggestPanelText);

//               /**
//                * Suggest Buttons
//                */
//               var suggestPanelButton = document.createElement("button");
//               suggestPanelButton.innerText = "Close";
//               suggestPanelButton.style.backgroundColor = "red";
//               suggestPanelButton.style.color = "white";
//               suggestPanelButton.style.fontSize = "15px";
//               suggestPanelButton.style.border = "none";
//               suggestPanelButton.style.padding = "5px";
//               suggestPanelButton.addEventListener("click", function () {
//                 suggestPanel.style.visibility = "visible";
//               });
//               suggestPanelButton.style.marginRight = "20px";
//               suggestPanelButton.style.bottom = "2px";
//               suggestPanelButton.style.top = "2px";
//               suggestPanel.appendChild(suggestPanelButton);

//               var suggestPanelButton1 = document.createElement("button");
//               suggestPanelButton1.innerText = "Replace";
//               suggestPanelButton1.style.backgroundColor = "red";
//               suggestPanelButton1.style.color = "white";
//               suggestPanelButton1.style.fontSize = "15px";
//               suggestPanelButton1.style.border = "none";
//               suggestPanelButton1.style.padding = "5px";
//               suggestPanelButton1.style.bottom = "2px";
//               suggestPanelButton1.style.top = "2px";

//               /**
//                * Handling span to text conversion (non-recursive)
//                */
//               suggestPanelButton1.addEventListener("click", function () {
//                 if (currentElement != null) {
//                   if (currentElement.value.includes(sentence)) {
//                     let text = currentElement.value;
//                     let newText = text.replaceAll(sentence, suggestion);
//                     currentElement.value = newText;
//                     target_sentences.delete(sentence);
//                   }
//                 }
//               });
//               suggestPanel.appendChild(suggestPanelButton1);
//             }
//           });

//           /**
//            *---------------------- caching logic ----------------------
//            */
//           const cache = {};
//           const cacheTime = 100000;
//           let cacheTimer = 0;

//           const getCacheTimer = (time) => {
//             const now = new Date().getTime();
//             if (cacheTimer < now + time) {
//               cacheTimer = now + time;
//             }
//             return cacheTimer;
//           };

//           const fetchWithCache = async (text, time) => {
//             let curText = JSON.parse(text).inputs;
//             const now = new Date().getTime();
//             if (!cache[curText] || cache[curText].cacheTimer < now) {
//               console.log(1111);
//               await getResult(text).then((ans) => {
//                 console.log(ans);
//                 cache[curText] = ans;
//                 cache[curText].cacheTimer = getCacheTimer(time);
//                 console.log(cache);
//                 console.log(cache[curText]);
//               });
//             }

//             return cache[curText];
//           };
//           /**
//            *-----------------------------------------------------------
//            */

//           var currentElement = null;
//           var elementlist = null;

//           /*
//            * Mouseover features and handling dynamic updates
//            */
//           window.addEventListener("mouseover", async function () {
//             /**
//              * Dynamic Hover
//              */
//             const spanElements = document.querySelectorAll(
//               "span[style='text-decoration: underline red;']"
//             );

//             spanElements.forEach((spanElement) => {
//               spanElement.addEventListener("mouseenter", function () {
//                 var rect = spanElement.getBoundingClientRect();
//                 hoverButton.style.top =
//                   rect.top - hoverButton.offsetHeight - 1 + "px";
//                 hoverButton.style.left = rect.left + "px";
//                 hoverButton.style.visibility = "visible";
//                 hoverButton.style.width = "30px";
//                 hoverButton.style.height = "30px";
//                 hoverButton.style.padding = "0px";
//               });
//             });

//             /**
//              * gmail collection
//              */
//             const collection1 = document.getElementsByClassName("ii gt");
//             /**
//              * github collection
//              */
//             const collection2 = document.getElementsByClassName(
//               "comment-body markdown-body js-preview-body"
//             );
//             /**
//              * play store comments collection
//              */
//             const collection3 = document.getElementsByClassName("h3YV2d");
//             const collection4 = document.getElementsByClassName("ras4vb");

//             const array1 = [...collection1];
//             const array2 = [...collection2];
//             const array3 = [...collection3];
//             const array4 = [...collection4];

//             const elementlist1 = array1.concat(array2);
//             const elementlist2 = elementlist1.concat(array3);
//             elementlist = elementlist2.concat(array4);

//             if (elementlist[0] && elementlist[0].innerText.length > 0) {
//               elementlist[0].addEventListener("mouseenter", async function () {
//                 currentElement = elementlist[0];
//                 console.log("here " + currentElement.innerText);
//                 let text = currentElement.innerText;
//                 text = text.substring(0, Math.min(text.length, 1000));
//                 var data = JSON.stringify({
//                   inputs: text,
//                 });

//                 let score = 0.0;

//                 let ans = await fetchWithCache(data, cacheTime);
//                 console.log(ans);
//                 // * Defining the score metric *//
//                 // for (let j = 0; j < 6; j++) {
//                 //   if (!ans) {
//                 //     break;
//                 //   }
//                 //   score += ans[j].score;
//                 // }
//                 score = ans
//                 if (score >= threshold_score) {
//                   currentElement.style.filter = "blur(3px)";
//                   console.log("True condition");
//                 } else {
//                   currentElement.style.filter = "none";
//                   console.log("False condition");
//                 }

//                 /**
//                  * get current position of element and assign it to checkButton based on position of currentElement
//                  */
//                 var rect = elementlist[0].getBoundingClientRect();
//                 checkButton.style.top =
//                   rect.top - checkButton.offsetHeight - 1 + "px";
//                 checkButton.style.left = rect.left + "px";
//                 checkButton.style.visibility = "visible";
//                 checkButton.style.width = "30px";
//                 checkButton.style.height = "30px";
//                 checkButton.style.padding = "0px";
//               });
//               elementlist[0].addEventListener("mouseleave", () =>
//                 setTimeout(() => {
//                   checkButton.style.visibility = "visible";
//                 }, 5000)
//               );
//               elementlist[0].addEventListener("click", function () {
//                 this.style.filter = "none";
//               });
//             }
//           });
//           let currentChart = null;
//           /**
//            * outside to avoid any mouseover issues
//            */
//           checkButton.addEventListener("click", async function () {
//             let text = currentElement.innerText;
//             var data = JSON.stringify({
//               inputs: text,
//             });

//             /**
//              * populating chart with the response values (toxic-bert)
//              */
//             await getResult(data).then((ans) => {
//               console.log("Response from getResult:", ans);
//               chartdivbutton.style.visibility = "visible";
//               let element = document.getElementById("chartid");
//               if (element == null) {
//                 return;
//               }
//               if (currentChart) {
//                 currentChart.destroy();
//                 currentChart = null;
//               }
//               console.log("In chart", ans);
//               currentChart = new Chart(element, {
//                 type: "pie",
//                 data: {
//                   labels: [
//                     "Toxicity", "Non-Toxicity"
//                     // ans[0].label,
//                     // ans[1].label,
//                     // ans[2].label,
//                     // ans[3].label,
//                     // ans[4].label,
//                     // ans[5].label,
//                   ],
//                   datasets: [
//                     {
//                       label: "CyberBully Details",
//                       data: [
//                         ans, 1 - ans
//                         // ans[0].score,
//                         // ans[1].score,
//                         // ans[2].score,
//                         // ans[3].score,
//                         // ans[4].score,
//                         // ans[5].score,
//                       ],
//                       backgroundColor: [
//                         "rgba(255, 99, 132, 0.8)",
//                         "rgba(75, 192, 192, 0.8)",
//                         // "rgba(54, 162, 235, 0.2)",
//                         // "rgba(255, 206, 86, 0.2)",
//                         // "rgba(75, 192, 192, 0.2)",
//                         // "rgba(153, 102, 255, 0.2)",
//                         // "rgba(255, 159, 64, 0.2)",
//                       ],

//                       borderColor: [
//                         "rgba(255,99,132,1)",
//                         "rgba(75, 192, 192,1)"
//                         // "rgba(54, 162, 235, 1)",
//                         // "rgba(255, 206, 86, 1)",
//                         // "rgba(75, 192, 192, 1)",
//                         // "rgba(153, 102, 255, 1)",
//                         // "rgba(255, 159, 64, 1)",
//                       ],
//                       borderWidth: 1,
//                     },
//                   ],
//                 },
//                 options: {
//                   responsive: true,
//                   legend: {
//                     display: true,
//                   },
//                   tooltips: {
//                     callbacks: {
//                       label: function (tooltipItem, data) {
//                         var label = data.labels[tooltipItem.index] || '';
//                         if (label) {
//                           label += ': ';
//                         }
//                         label += parseFloat(data.datasets[0].data[tooltipItem.index]).toFixed(2); // Displaying values up to 2 decimal places
//                         return label;
//                       }
//                     }
//                   },
//                 },
//               });
//             });
//           });
//         }

//         async function scrapeWhole() {
//           /**
//            * github comment collection
//            */
//           const collection1 = document.getElementsByClassName(
//             "d-block comment-body markdown-body  js-comment-body"
//           );
//           /**
//            * github header collection
//            */
//           const collection2 = document.getElementsByClassName(
//             "gh-header-title flex-auto wb-break-word f1 mr-0"
//           );
//           const array1 = [...collection1];
//           const array2 = [...collection2];

//           const elementlist = array1.concat(array2);

//           if (elementlist.length == 0) return;

//           var chartdiv = document.createElement("canvas");
//           chartdiv.style.position = "fixed";
//           chartdiv.style.borderRadius = "20px";
//           chartdiv.style.right = "10px";
//           chartdiv.style.top = "30px";
//           chartdiv.style.height = "300px";
//           chartdiv.style.overflow = "scroll";
//           chartdiv.style.width = "600px";
//           chartdiv.id = "chartid";
//           chartdiv.style.backgroundColor = "white";
//           chartdiv.style.color = "black";
//           chartdiv.style.border = "none";
//           chartdiv.style.padding = "8px";
//           chartdiv.style.zIndex = 2000;
//           chartdiv.style.visibility = "visible";
//           chartdiv.style.border = "1px solid white";
//           chartdiv.style.maxHeight = "600px";
//           chartdiv.style.maxWidth = "600px";

//           var chartdivbutton = document.createElement("button");
//           chartdivbutton.style.position = "fixed";
//           chartdivbutton.style.borderRadius = "20px";
//           chartdivbutton.style.right = "10px";
//           chartdivbutton.style.top = "5px";
//           chartdivbutton.style.backgroundColor = "white";
//           chartdivbutton.style.color = "black";
//           chartdivbutton.style.border = "none";
//           chartdivbutton.style.padding = "8px";
//           chartdivbutton.style.zIndex = 1000;
//           chartdivbutton.innerText = "Show Toxicity Scale";
//           chartdivbutton.style.visibility = "visible";
//           chartdivbutton.style.border = "1px solid yellow";
//           chartdivbutton.addEventListener("click", function () {
//             if (chartdiv.style.visibility == "visible") {
//               chartdiv.style.visibility = "visible";
//             } else {
//               chartdiv.style.visibility = "visible";
//             }
//           });

//           document.body.appendChild(chartdiv);
//           document.body.appendChild(chartdivbutton);

//           var i = 0;
//           var text = "";
//           for (i = 0; i < Math.min(elementlist.length, 4); i++) {
//             if (elementlist[i] && elementlist[i].innerText.length > 0) {
//               let innertext = elementlist[i].innerText;
//               /**
//                * optimization to avoid 400 error , reducing network payload
//                */
//               innertext = innertext.substring(
//                 0,
//                 Math.min(innertext.length, 1000)
//               );
//               text += innertext + "\n";
//               let data = JSON.stringify({
//                 inputs: text,
//               });

//               /**
//                * populatiing chart values
//                */
//               await getResult(data).then((ans) => {
//                 // let toxic_score = 0.0;
//                 // let obscene_score = 0.0;
//                 // let insult_score = 0.0;
//                 // let identity_hate_score = 0.0;
//                 // let severley_toxic_score = 0.0;
//                 // let threat_score = 0.0;
//                 let score = ans;
//                 // let value = 0;
//                 // for (let j = 0; j < 6; j++) {
//                 //   if (!ans) {
//                 //     break;
//                 //   }
//                 //   if (ans[j].label === "toxic") toxic_score += ans[j].score;
//                 //   else if (ans[j].label === "obscene")
//                 //     obscene_score += ans[j].score;
//                 //   else if (ans[j].label === "insult")
//                 //     insult_score += ans[j].score;
//                 //   else if (ans[j].label === "identity_hate")
//                 //     identity_hate_score += ans[j].score;
//                 //   else if (ans[j].label === "severe_toxic")
//                 //     severley_toxic_score += ans[j].score;
//                 //   else if (ans[j].label === "threat")
//                 //     threat_score += ans[j].score;

//                 //   score += ans[j].score;
//                 // }

//                 if (score >= threshold_score) {
//                   elementlist[i].style.filter = "blur(3px)";
//                 }
//                 elementlist[i].addEventListener("click", function () {
//                   this.style.filter = "none";
//                 });
//                 elementlist[i].addEventListener("mouseout", function () {
//                   if (score >= 1.5) this.style.filter = "blur(3px)";
//                 });
//               });
//             }
//           }
//           if (text != "") {
//             /**
//              * optimization to avoid 400 error , reducing network payload
//              */
//             text = text.substring(0, Math.min(text.length, 1000));
//             let data = JSON.stringify({
//               inputs: text,
//             });
//             await getResult(data).then((ans) => {
//               chartdivbutton.style.visibility = "visible";
//               let element = document.getElementById("chartid");
//               if (element == null) return;
//               var myChart = new Chart(element, {
//                 type: "bar",
//                 data: {
//                   labels: [
//                     "Toxicity"
//                     // ans[0].label,
//                     // ans[1].label,
//                     // ans[2].label,
//                     // ans[3].label,
//                     // ans[4].label,
//                     // ans[5].label,
//                   ],
//                   datasets: [
//                     {
//                       label: "CyberBully Details",
//                       data: [
//                         ans
//                         // ans[0].score,
//                         // ans[1].score,
//                         // ans[2].score,
//                         // ans[3].score,
//                         // ans[4].score,
//                         // ans[5].score,
//                       ],
//                       backgroundColor: [
//                         "rgba(255, 99, 132, 0.2)",
//                         // "rgba(54, 162, 235, 0.2)",
//                         // "rgba(255, 206, 86, 0.2)",
//                         // "rgba(75, 192, 192, 0.2)",
//                         // "rgba(153, 102, 255, 0.2)",
//                         // "rgba(255, 159, 64, 0.2)",
//                       ],

//                       borderColor: [
//                         "rgba(255,99,132,1)",
//                         // "rgba(54, 162, 235, 1)",
//                         // "rgba(255, 206, 86, 1)",
//                         // "rgba(75, 192, 192, 1)",
//                         // "rgba(153, 102, 255, 1)",
//                         // "rgba(255, 159, 64, 1)",
//                       ],
//                       borderWidth: 1,
//                     },
//                   ],
//                 },
//                 options: {
//                   scales: {
//                     yAxes: [
//                       {
//                         ticks: {
//                           beginAtZero: true,
//                           // max: 1,
//                         },
//                       },
//                     ],
//                   },
//                 },
//               });
//             });
//           }
//         }


//         async function getDataFromCache(url) {
//           return new Promise((resolve, reject) => {
//             chrome.storage.local.get(url, function (result) {
//               if (chrome.runtime.lastError) {
//                 reject(chrome.runtime.lastError);
//               } else {
//                 resolve(result[url]);
//               }
//             });
//           });
//         }

//         // Define a variable to store the result globally
//         let repoScoreResult = null;

//         async function get_url_s() {
//           // Listen for messages from the background script
//           chrome.runtime.onMessage.addListener(async function (message, sender, sendResponse) {
//             // Handle the received message
//             console.log("Message received in content script:", message);

//             if (message.url.startsWith("https://github.com/")) {
//               console.log("yes it is github");
//               try {
//                 const cachedData = await getDataFromCache(message.url);

//                 if (cachedData && Date.now() < cachedData.expiresAt) {
//                   console.log("Result from cache:", cachedData.data);
//                   // Store the cached result globally
//                   repoScoreResult = cachedData.data;
//                 } else {
//                   var result = await getreposcore_s(message.url);
//                   result = result * 1000;
//                   result = Number(result).toFixed(2);
//                   console.log("Result from API:", result);
//                   // Save the result to cache with expiration time
//                   saveDataToCache(message.url, result);
//                   // Store the result globally
//                   repoScoreResult = result;
//                 }
//                 initializeButton(); // Call initializeButton
//               } catch (error) {
//                 console.error("Error:", error);
//               }
//             }
//           });
//         }

//         function initializeButton() {
//           // Create Get Score Button
//           // getScoreButton = document.createElement("button");
//           // getScoreButton.textContent = "Get Repo Score";
//           // getScoreButton.id = "getScoreButton";
//           // getScoreButton.style.position = "fixed";
//           // getScoreButton.style.borderRadius = "20px";
//           // getScoreButton.style.right = "10px";
//           // getScoreButton.style.bottom = "60px";
//           // getScoreButton.style.backgroundColor = "blue";
//           // getScoreButton.style.color = "yellow";
//           // getScoreButton.style.border = "none";
//           // getScoreButton.style.padding = "8px";
//           // getScoreButton.style.visibility = "visible";
//           // getScoreButton.style.zIndex = 1000;

//           // Add click event listener to the button
//           // getScoreButton.addEventListener("click", function () {
//           //   // Display the result stored globally
//           //   console.log("yes getscorebutton is clicked");
//           //   getScoreButton.style.display = "none";
//           //   if (repoScoreResult !== null) {
//           //     resultBox.textContent = `Repo's Toxicity Score: ${repoScoreResult}`;
//           //     resultBox.style.display = "block"; // Make the resultBox visible
//           //   } else {
//           //     // If result is not available
//           //     console.log("Result not available");
//           //   }
//           // });

//           // Create Result Box
//           var resultBox = document.createElement("div");
//           resultBox.id = "resultBox";
//           resultBox.style.position = "fixed";
//           resultBox.style.borderRadius = "100px";
//           resultBox.style.right = "10px";
//           resultBox.style.bottom = "60px";
//           resultBox.style.backgroundColor = "blue";
//           resultBox.style.color = "yellow";
//           resultBox.style.padding = "10px";
//           resultBox.style.zIndex = 1000;
//           resultBox.style.display = "none"; // Change display property to 'block' to make it visible
//           resultBox.style.visibility = "visible"; 

//           if (repoScoreResult !== null) {
//             resultBox.textContent = `Repo's Toxicity Score: ${repoScoreResult}`;
//             resultBox.style.display = "block"; // Make the resultBox is visible
//             createScoreBar(repoScoreResult);
//           } else {
//             // If result is not available
//             console.log("Result not available");
//           }
//           // Append resultBox to the body
//           document.body.appendChild(resultBox);

//           // Append getScoreButton to the body
//           // document.body.appendChild(getScoreButton);
//         }

//         function createScoreBar(score) {
//           var scoreBar = document.createElement("div");
//           scoreBar.className = "score-bar";
//           scoreBar.style.position = "fixed";
//           scoreBar.style.border = "1px solid #000";
//           scoreBar.style.width = "200px"; 
//           scoreBar.style.height = "20px"; 
//           scoreBar.style.right = "10px";
//           scoreBar.style.top = "150px";

//           var scorePoint = document.createElement("div");
//           scorePoint.className = "score-point";
//           scorePoint.style.position = "absolute";
//           scorePoint.style.height = "100%";
//           scorePoint.style.width = "2px";
//           scorePoint.style.backgroundColor = "black"; 
//           scorePoint.style.left = (score / 100) * 200 + "px"; //score indicator

//           var greenWidth = 33.33; 
//           var orangeWidth = 33.33; 
//           var redWidth = 33.34; 

//           var greenSection = document.createElement("div");
//           greenSection.className = "green";
//           greenSection.style.position = "absolute";
//           greenSection.style.height = "100%";
//           greenSection.style.width = greenWidth + "%";
//           greenSection.style.backgroundColor = "green";
//           greenSection.style.left = "0"; 

//           var orangeSection = document.createElement("div");
//           orangeSection.className = "orange";
//           orangeSection.style.position = "absolute";
//           orangeSection.style.height = "100%";
//           orangeSection.style.width = orangeWidth + "%";
//           orangeSection.style.backgroundColor = "orange";
//           orangeSection.style.left = greenWidth + "%"; 

//           var redSection = document.createElement("div");
//           redSection.className = "red";
//           redSection.style.position = "absolute";
//           redSection.style.height = "100%";
//           redSection.style.width = redWidth + "%";
//           redSection.style.backgroundColor = "red";
//           redSection.style.left = (greenWidth + orangeWidth) + "%"; 

//           var message = document.createElement("div");
//           message.className = "score-message";
//           message.style.position = "absolute";
//           message.style.top = "-30px"; 
//           message.style.left = "0";
//           message.style.width = "200px";
//           message.style.textAlign = "center";
        
//           if (score <= 33.33) {
//             message.textContent = "It is OK";
//           } else if (score <= 66.66) {
//             message.textContent = "Not Ideal";
//           } else {
//             message.textContent = "Avoid";
//           }
        
//           scoreBar.appendChild(message);

//           scoreBar.appendChild(greenSection);
//           scoreBar.appendChild(orangeSection);
//           scoreBar.appendChild(redSection);
//           scoreBar.appendChild(scorePoint);

//           document.body.appendChild(scoreBar);
//         }

//         function saveDataToCache(url, data, expirationTime = 3600 * 1000) {
//           const newData = {
//             data: data,
//             expiresAt: Date.now() + expirationTime // Set expiration time
//           };
//           const newDataObj = {};
//           newDataObj[url] = newData;
//           chrome.storage.local.set(newDataObj, function () {
//             if (chrome.runtime.lastError) {
//               console.error("Error saving to cache:", chrome.runtime.lastError);
//             } else {
//               console.log("Data saved to cache:", newDataObj);
//             }
//           });
//         }



//         $(document).ready(function () {
//           get_url_s();
//           scrapeWhole();
//           main();
//         });
//       },
//       {},
//     ],
//   },
//   {},
//   ["sotagger.js"],
//   null
// );

// content.js
document.addEventListener('DOMContentLoaded', function() {
  const newDiv = document.createElement('div');
  newDiv.innerHTML = `
    <div class="commit-summary-box">
      <h1>Commit Summarization</h1>
      <p>This is where the summary would appear.</p>
    </div>
  `;
  newDiv.classList.add("custom-commit-box");

  // Append this div to the body or a specific part of GitHub page
  const container = document.querySelector('body');
  if (container) {
    container.appendChild(newDiv);
  }
});




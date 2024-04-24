

// // Sample JSON data of issues
// const issuesData = [
//   {
//     "issue_no": 1324,
//     "issue_link": "https://github.com/example/repo/issues/1",
//     "issue_title": "Fixing the login bug",
//     "similarity_per": "95%"
//   },
//   {
//     "issue_no": 9842,
//     "issue_link": "https://github.com/example/repo/issues/2",
//     "issue_title": "Update dependencies to newer versions",
//     "similarity_per": "80%"
//   },
//   {
//     "issue_no": 4353,
//     "issue_link": "https://github.com/example/repo/issues/3",
//     "issue_title": "Refactor the user authentication system",
//     "similarity_per": "89%"
//   },
//   {
//     "issue_no": 1354,
//     "issue_link": "https://github.com/example/repo/issues/4",
//     "issue_title": "Optimize database queries",
//     "similarity_per": "92%"
//   },
//   {
//     "issue_no": 5679,
//     "issue_link": "https://github.com/example/repo/issues/5",
//     "issue_title": "Improve UI responsiveness",
//     "similarity_per": "88%"
//   }
// ];

// // Function to sort issues by similarity percentage in descending order
// function sortIssuesBySimilarity(issues) {
//   return issues.sort((a, b) => parseFloat(b.similarity_per) - parseFloat(a.similarity_per));
// }

// // Function to truncate titles to a specified number of words
// function truncateTitle(title, maxWords = 8) {
//   const words = title.split(' ');
//   return words.length > maxWords ? words.slice(0, maxWords).join(' ') + '...' : title;
// }


// // Function to create and manage the commit summary box
// function appendCommitSummaryBox() {
//   const containerSelector = '.custom-commit-box';
//   if (document.querySelector(containerSelector)) return;

//   const sortedIssues = sortIssuesBySimilarity(issuesData);
//   const newDiv = document.createElement('div');
//   newDiv.classList.add("custom-commit-box");
  
//   const htmlContent = document.createElement('div');
//   htmlContent.innerHTML = `<h1>SIMILAR ISSUES</h1>` + generateHTML(sortedIssues.slice(0, 3));
//   newDiv.appendChild(htmlContent);

//   const toggleBtn = document.createElement('button');
//   toggleBtn.textContent = 'Show More';
//   toggleBtn.classList.add('toggle-btn');
//   toggleBtn.addEventListener('click', () => toggleIssuesDisplay(toggleBtn, sortedIssues, htmlContent));

//   newDiv.appendChild(toggleBtn);
//   document.body.appendChild(newDiv);
// }

// // Function to toggle the display of issues in the commit summary box
// function toggleIssuesDisplay(toggleBtn, sortedIssues, container) {
//   const isExtended = toggleBtn.textContent === 'Show More';
//   toggleBtn.textContent = isExtended ? 'Show Less' : 'Show More';
//   container.innerHTML = `<h1>SIMILAR ISSUES</h1>` + generateHTML(isExtended ? sortedIssues : sortedIssues.slice(0, 3));
// }

// // Helper function to generate HTML for issue entries
// function generateHTML(issues) {
//   return issues.map(issue =>
//     `<div class="issue-entry">
//       <a href="${issue.issue_link}">${truncateTitle(issue.issue_title)} <span class="issue-number">#${issue.issue_no}</span></a>
//       <span class="similarity">Similarity: ${issue.similarity_per}</span>
//     </div>`
//   ).join('');
// }


// // CSS styles for the commit box and entries
// const style = document.createElement('style');
// style.innerHTML = `
//   .custom-commit-box {
//     position: fixed;
//     bottom: 20px;
//     right: 20px;
//     width: 300px;
//     background-color: #333;
//     color: #fff;
//     border: 1px solid #555;
//     box-shadow: 0 2px 6px rgba(0,0,0,0.3);
//     padding: 10px;
//     z-index: 1000;
//     font-family: Arial, sans-serif;
//     overflow: auto;
//   }
//   .custom-commit-box h1 {
//     font-size: 16px;
//     margin-bottom: 10px;
//   }
//   .issue-entry {
//     margin-bottom: 10px;
//   }
//   .issue-entry a {
//     text-decoration: none;
//     color: #4da6ff;
//   }
//   .issue-entry .similarity {
//     display: block;
//     color: #bbb;
//     font-size: 12px;
//   }
// `;
// document.head.appendChild(style);

// // Function to remove the commit summary box
// function removeCommitSummaryBox() {
//   const existingBox = document.querySelector('.custom-commit-box');
//   if (existingBox) existingBox.remove();
// }

// // Observer to detect page changes relevant to GitHub issue tracking
// const observer = new MutationObserver((mutations, obs) => {
//   const url = window.location.href;
//   const githubIssueRegex = /^https:\/\/github\.com\/[\w\-]+\/[\w\-]+\/issues\/(\d+)(\/)?$/;

//   if (githubIssueRegex.test(url)) {
//     appendCommitSummaryBox();
//   } else {
//     removeCommitSummaryBox();
//   }
// });

// // Start observing for changes in the document
// observer.observe(document.body, {
//   childList: true,
//   subtree: true,
//   characterData: true
// });





// Sample JSON data of issues
var issuesData = [
  {
    issue_no: 241,
    issue_link: "https://github.com/shosetsuorg/shosetsu/pull/241",
    issue_title: "Temp fix for backup restore with external repos",
    similarity_per: "90%",
  },
  {
    issue_no: 240,
    issue_link: "https://github.com/shosetsuorg/shosetsu/issues/240",
    issue_title: "[Bug] [App lags]",
    similarity_per: "60%",
  },
  {
    issue_no: 237,
    issue_link: "https://github.com/shosetsuorg/shosetsu/pull/237",
    issue_title: "Fullscreen Settings for Reader",
    similarity_per: "88%",
  },
  {
    issue_no: 236,
    issue_link: "https://github.com/shosetsuorg/shosetsu/pull/236",
    issue_title: "UI Cleanup and improvements",
    similarity_per: "75%",
  },
  {
    issue_no: 235,
    issue_link: "https://github.com/shosetsuorg/shosetsu/pull/235",
    issue_title: "Multiple optimizations for performance",
    similarity_per: "55%",
  },
  {
    issue_no: 234,
    issue_link: "https://github.com/shosetsuorg/shosetsu/issues/234",
    issue_title: "[F-R] Chapter range download",
    similarity_per: "85%",
  },
  {
    issue_no: 232,
    issue_link: "https://github.com/shosetsuorg/shosetsu/issues/232",
    issue_title: "[Bug] [2.0.0-2344] Migrate source button malfunctioning",
    similarity_per: "60%",
  },
  {
    issue_no: 231,
    issue_link: "https://github.com/shosetsuorg/shosetsu/pull/231",
    issue_title: "Move package to app.shosetsu.android",
    similarity_per: "80%",
  },
];


// var issuesData2 = [
//   {
//     issue_no: 242,
//     issue_link: "https://github.com/shosetsuorg/shosetsu/pull/242",
//     issue_title: "Move app package to app.shosetsu.android",
//     similarity_per: "80%",
//   },
//   {
//     issue_no: 241,
//     issue_link: "https://github.com/shosetsuorg/shosetsu/pull/241",
//     issue_title: "Temp fix for backup restore with external repos",
//     similarity_per: "70%",
//   },
//   {
//     issue_no: 240,
//     issue_link: "https://github.com/shosetsuorg/shosetsu/issues/240",
//     issue_title: "[Bug] [App lags]",
//     similarity_per: "60%",
//   },
//   {
//     issue_no: 237,
//     issue_link: "https://github.com/shosetsuorg/shosetsu/pull/237",
//     issue_title: "Fullscreen Settings for Reader",
//     similarity_per: "88%",
//   },
//   {
//     issue_no: 236,
//     issue_link: "https://github.com/shosetsuorg/shosetsu/pull/236",
//     issue_title: "UI Cleanup and improvements",
//     similarity_per: "75%",
//   },
//   {
//     issue_no: 235,
//     issue_link: "https://github.com/shosetsuorg/shosetsu/pull/235",
//     issue_title: "Multiple optimizations for performance",
//     similarity_per: "55%",
//   },
//   {
//     issue_no: 234,
//     issue_link: "https://github.com/shosetsuorg/shosetsu/issues/234",
//     issue_title: "[F-R] Chapter range download",
//     similarity_per: "85%",
//   },
//   {
//     issue_no: 232,
//     issue_link: "https://github.com/shosetsuorg/shosetsu/issues/232",
//     issue_title: "[Bug] [2.0.0-2344] Migrate source button malfunctioning",
//     similarity_per: "60%",
//   },
//   {
//     issue_no: 231,
//     issue_link: "https://github.com/shosetsuorg/shosetsu/pull/231",
//     issue_title: "Move package to app.shosetsu.android",
//     similarity_per: "80%",
//   },
// ];


// Function to sort issues by similarity percentage in descending order
function sortIssuesBySimilarity(issues) {
  return issues.sort(
    (a, b) => parseFloat(b.similarity_per) - parseFloat(a.similarity_per)
  );
}

// Function to truncate titles to a specified number of words
function truncateTitle(title, maxWords = 8) {
  const words = title.split(" ");
  return words.length > maxWords
    ? words.slice(0, maxWords).join(" ") + "..."
    : title;
}

// Function to create and manage the commit summary box
function appendCommitSummaryBox() {
  const containerSelector = ".custom-commit-box";
  if (document.querySelector(containerSelector)) return;

  const sortedIssues = sortIssuesBySimilarity(issuesData);
  const newDiv = document.createElement("div");
  newDiv.classList.add("custom-commit-box");

  const htmlContent = document.createElement("div");
  htmlContent.innerHTML =
    "<h1>SIMILAR ISSUES</h1>" + generateHTML(sortedIssues.slice(0, 3));
  newDiv.appendChild(htmlContent);

  const toggleBtn = document.createElement("button");
  toggleBtn.textContent = "Show More";
  toggleBtn.classList.add("toggle-btn");
  toggleBtn.addEventListener("click", () =>
    toggleIssuesDisplay(toggleBtn, sortedIssues, htmlContent)
  );

  newDiv.appendChild(toggleBtn);
  document.body.appendChild(newDiv);
}

// Function to toggle the display of issues in the commit summary box
function toggleIssuesDisplay(toggleBtn, sortedIssues, container) {
  const isExtended = toggleBtn.textContent === "Show More";
  toggleBtn.textContent = isExtended ? "Show Less" : "Show More";
  container.innerHTML =
    "<h1>GITHUB ISSUES</h1>" +
    generateHTML(isExtended ? sortedIssues : sortedIssues.slice(0, 3));
}

// Helper function to generate HTML for issue entries
// function generateHTML(issues) {
//   return issues
//     .map(
//       (issue) =>
//         `<div class="issue-entry">
//       <a href="${issue.issue_link}">${truncateTitle(
//           issue.issue_title
//         )} <span class="issue-number">#${issue.issue_no}</span></a>
//       <span class="similarity">Similarity: ${issue.similarity_per}</span>
//     </div>`
//     )
//     .join("");
// }

function generateHTML(issues) {
  return issues.map(issue => {
    // Calculate the width of the green part based on the similarity percentage, scaled down to 90%
    const originalSimilarity = parseFloat(issue.similarity_per); // Convert percentage string to number
    const scaledSimilarity = originalSimilarity * 0.9; // Scale similarity to 90%
    const greenWidth = scaledSimilarity; // Percentage of green (adjusted)
    const grayWidth = 100 - scaledSimilarity; // Percentage of gray (adjusted)

    return `<div class="issue-entry">
      <a href="${issue.issue_link}">${truncateTitle(issue.issue_title)} <span class="issue-number">#${issue.issue_no}</span></a>
      <div class="similarity-bar" style="background: linear-gradient(to right, #008000 ${greenWidth}%, #646464 ${greenWidth}%, #646464 ${grayWidth}%); height: 10px; width: 100%; margin: auto; border-radius: 5px;"></div>
    </div>`;
  }).join('');
}




// CSS styles for the commit box and entries
const style = document.createElement("style");
style.innerHTML = `
  .custom-commit-box {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 300px;
    background-color: #333;
    color: #fff;
    border: 1px solid #555;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    padding: 10px;
    z-index: 1000;
    font-family: Arial, sans-serif;
    overflow: auto;
  }
  .custom-commit-box h1 {
    font-size: 16px;
    margin-bottom: 10px;
  }
  .issue-entry {
    margin-bottom: 10px;
  }
  .issue-entry a {
    text-decoration: none;
    color: #4da6ff;
  }
  .issue-entry .similarity {
    display: block;
    color: #bbb;
    font-size: 12px;
  }
`;
document.head.appendChild(style);

// Function to remove the commit summary box
function removeCommitSummaryBox() {
  const existingBox = document.querySelector(".custom-commit-box");
  if (existingBox) existingBox.remove();
}

// function to extract details about an issue
function extractGithubInfo(url) {
  const pattern = /https:\/\/github.com\/([^/]+)\/([^/]+)\/(.+)\/(\d+)/;
  const match = pattern.exec(url);

  if (match) {
    return {
      username: match[1],
      repositoryName: match[2],
      issueNumber: match[4],
    };
  } else {
    return null;
  }
}

// async function getResult(send_data) {
//   const options = {
//     method: "POST",
//     headers: {
//       Accept: "application/json",
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(send_data), // Assuming your endpoint expects a string directly
//   };
//   // console.log(send_data);
//   try {
//     const response = await fetch("https://10.23.105.31:5000/get_issues", options);
//     const data = await response.json();
//     console.log("data", data);
//     issuesData = data;
//     appendCommitSummaryBox();
//     return data;
//   } catch (error) {
//     console.error("Error:", error);
//     throw error;
//   }
// }

async function getResult(send_data) {
  try {
    const url = window.location.href;
    const issueNumber = url.split('/').pop();
    console.log("Issue Number:", issueNumber);

    let responseData;

    if (issueNumber === '242') {
      console.log("here")
      responseData = issuesData;
    } else {
      issuesData = [];
      issuesData.push(
        {
          issue_no: 242,
          issue_link: "https://github.com/shosetsuorg/shosetsu/pull/242",
          issue_title: "Move app package to app.shosetsu.android",
          similarity_per: "60%",
        },
        {
          issue_no: 208,
          issue_link: "https://github.com/shosetsuorg/shosetsu/issues/208",
          issue_title: "[Bug] [2186] Heavy lag occours and accumulate over time after normal use",
          similarity_per: "75%",
        },
        {
          issue_no: 240,
          issue_link: "https://github.com/shosetsuorg/shosetsu/issues/240",
          issue_title: "[Bug] [App lags]",
          similarity_per: "100%",
        }
      );
      
      responseData = issuesData;
    }

    appendCommitSummaryBox(); 
    return responseData;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

// Observer to detect page changes relevant to GitHub issue tracking
const observer = new MutationObserver(async (mutations, obs) => {
  const url = window.location.href;
  const githubIssueRegex =
    /^https:\/\/github\.com\/[\w\-]+\/[\w\-]+\/issues\/(\d+)(\/)?$/;

  const githubPullRegex =
    /^https:\/\/github\.com\/[\w\-]+\/[\w\-]+\/pull\/(\d+)(\/)?$/;
    
  if (githubIssueRegex.test(url) || githubPullRegex.test(url)) {
    const info = extractGithubInfo(url);
    issuesData = await getResult(info);
    // console.log("issuesData", issuesData);
    // appendCommitSummaryBox();
  } else {
    removeCommitSummaryBox();
  }
});

// Start observing for changes in the document
observer.observe(document.body, {
  childList: true,
  subtree: true,
  characterData: true,
});

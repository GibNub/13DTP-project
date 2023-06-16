// Remove all child elements of quesiton div
function clearQuestion(div) { 
    while (div.firstChild) {
        div.removeChild(questionDiv.lastChild)
    }
};

// Add question
function addWrittenQuestion(type) {
    const questionDiv = document.getElementById("create-quiz-question")
    clearQuestion(questionDiv);
    if (type == 0) {
        questionDiv.appendChild("{}")
    }
};
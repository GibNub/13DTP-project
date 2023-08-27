// Remove all child elements of form div
function clearDiv(div) { 
    while (div.firstChild) {
        div.removeChild(div.lastChild);
    };
};


// Create form for question depending on question type
function addQuestion(type) {
    const formDiv = document.getElementById("create-question");
    clearDiv(formDiv);
    const header = document.createElement("h2")
    const form = document.createElement("form");
    form.setAttribute("action", `/quiz/create/${type}`)
    form.setAttribute("method", "POST")
    if (type == 1) {
        header_text = document.createTextNode("Add boolean question")
        factQuestion(form)
    } else if (type == 2) {
        header_text = document.createTextNode("Add written question")
        writtenQuestion(form);
    } else if (type == 3) {
        header_text = document.createTextNode("Add multiple choice question")
        multiChoiceForm(form)
    } else {
        return
    }
    clearDiv(header)
    header.appendChild(header_text)
    formDiv.appendChild(header)
    formDiv.appendChild(form)

}

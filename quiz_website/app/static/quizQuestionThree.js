// Remove all child elements of form div
function clearQuestion(div) { 
    while (div.firstChild) {
        div.removeChild(div.lastChild);
    };
};


// Add form for question depending on question type
function addQuestion(type) {
    const formDiv = document.getElementById("create-question");
    clearQuestion(formDiv);
    const form = document.createElement("form");
    form.setAttribute("action", `{{ url_for('create', type=${type}) }}`);
    if (type == 1) {
        writtenQuestion(form)
    } else if (type == 2) {
        factQuestion(form);
    } else if (type == 3) {
        multiChoiceForm(form)
    } else {
        return
    }
    formDiv.appendChild(form)

}

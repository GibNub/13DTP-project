// Remove all child elements of form div
function clearQuestion(div) { 
    while (div.firstChild) {
        div.removeChild(div.lastChild);
    };
};


// Add form for question
function addQuestion(type) {
    const formDiv = document.getElementById("create-question");
    clearQuestion(formDiv);
    const form = document.createElement("form");
    form.setAttribute("action", `{{ url_for('create', type=${type}) }}`);
    if (type == 1) {
        writtenQuestion(form);
    } else if (type == 2) {
        factQuestion(form)
    } else if (type == 3) {
        multipleChoiceQuestion(form)
    } else {
        return
    }
    formDiv.appendChild(form)

}


// Written question
function writtenQuestion(form) {
    form.innerHTML = `
    {{ written_form.csrf_token }}
    {{ written_form.written_question }}
    {{ written_form.written_answer }}
    {{ written_form.submit }}
    `;
};


// True false question
function factQuestion(form) {
    form.innerHTML = `
    {{ fact_form.csrf_token }}
    {{ fact_form.true_statement }}
    {{ fact_form.false_statement }}
    {{ fact_form.submit }}
    `
};


// Multichoice question
function multipleChoiceQuestion(form) {
    form.innerHTML = `
    {{ multi_choice_form.csrf_token }}
    {{ multi_choice_form.multi_question }}
    {{ multi_choice_form.correct_answer }}
    {{ multi_choice_form.false_one }}
    {{ multi_choice_form.false_two }}
    {{ multi_choice_form.false_three }}
    `
};


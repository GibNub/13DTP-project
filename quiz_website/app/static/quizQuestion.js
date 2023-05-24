// Helper function to set multiple attributes to a field
function setAttr(element, attr) {
    for(let key in attr) {
    element.setAttribute(key, attr[key]);
  };
};


// Creates an input field 
function addTextField(fieldName, questionNumber) {
  const attr = {
    'type' : 'text',
    'name' : fieldName,
    'id' : `${fieldName}-${questionNumber}`
  };
  const field = document.createElement('input');
  setAttr(field, attr);
  return field;
};


// Select field
function addSelectField(fieldName, questionNumber) {
  const selectField = document.createElement('select');
  setAttr(selectField, {
    'name' : fieldName,
    'id' : `${fieldName}-${questionNumber}`
  });
  // Question types
  // 0 : True/false
  // 1 : Written
  // 2 : Multiple choice
  questionType = ['True False', 'Written', 'Multiple Choice']
  const selectLabel = document.createElement('option')
  selectLabel.append(document.createTextNode('--Select question type--'))
  selectField.appendChild(selectLabel)
  for (let x in questionType) {
    const option = document.createElement('option');
    const node = document.createTextNode(questionType[x]);
    option.setAttribute('value', x);
    option.appendChild(node);
    selectField.appendChild(option);
    console.log(selectField)
  };
  return selectField;
};


let questionNumber = 0
// Adds a new question field (question, answer, and type) to quiz form
function addQuestion() {
  const form = document.getElementById('quiz-question');
  const fieldDiv = document.createElement('div');
  setAttr(fieldDiv, {'class' : 'question'});
  fieldDiv.appendChild(addTextField('question', questionNumber))
  fieldDiv.appendChild(addTextField('answer', questionNumber))
  // dropdown
  fieldDiv.appendChild(addSelectField('question-type', questionNumber))
  form.appendChild(fieldDiv);
  questionNumber += 1
};


// Remove question div
function removeLastQuestion() {
  const form = document.getElementById('quiz-question');
  form.removeChild(form.lastElementChild);
};

// Helper function to set multiple attributes to a field
function setAttr(element, attr) {
    for(let key in attr) {
    element.setAttribute(key, attr[key]);
  };
};


// Creates a fie
function addField(fieldName, type, questionNumber) {
  const attr = {
    'type' : type,
    'name' : fieldName,
    'id' : `${fieldName}-${questionNumber}`
  };
  const field = document.createElement('input');
  setAttr(field, attr);
  return field;
};


let questionNumber = 0
// Adds a new question field (question, answer, and type) to quiz form
function addQuestion() {
  questionNumber += 1
  const form = document.getElementById('quiz-question');
  const names = ['question', 'answer', 'question-type'];
  const type = 'text'; // Add more field types later
  const fieldDiv = document.createElement('div');
  setAttr(fieldDiv, {'class' : 'question'});
  for (let n in names) {
    fieldDiv.appendChild(addField(names[n], type, questionNumber))
  };
  form.appendChild(fieldDiv);
};


function removeLastQuestion() {
  const form = document.getElementById('quiz-question');
  form.removeChild(form.lastElementChild);
};

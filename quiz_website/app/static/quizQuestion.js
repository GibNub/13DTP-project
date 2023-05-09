// Helper function to set multiple attributes to a field
function setAttr(element, attr) {
    for(let key in attr) {
    element.setAttribute(key, attr[key]);
  };
};


// Creates a fie
function addField(fieldName, type, questionNumber, form) {
  const attr = {
    'type' : type,
    'name' : fieldName,
    'id' : `${fieldname}-${questionNumber}`
  };
  const field = document.createElement('input');
  setAttr(field, attr);
  form.appendChild(field);
};


let questionNumber = 0
// Adds a new question field (question, answer, and type) to quiz form
function addQuestion() {
  const form = document.getElementById('quiz-question');
  const names = ['question', 'answer', 'qusetion-type'];
  const type = 'text';
  for (let n in names) {
    addField(names[n], type, form)
  };
};

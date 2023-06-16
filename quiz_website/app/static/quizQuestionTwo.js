let questionNumber = 0

// Question types
// 0 : True/false
// 1 : Written
// 2 : Multiple choice

// Nested list: first item is field name, second is placeholder text
const questionTypefields = {
    0 : [
            ['trueStatement', 'Enter true statement'],
            ['falseStatement', 'Enter false statement']
        ],
    1 : [
            ['question', 'Enter question'],
            ['answer', 'Enter answer']
        ],
    2 : [
            ['question', 'Enter question'],
            ['correctAnswer', 'Enter correct answer'],
            ['falseOne', 'Enter fake answer 1'],
            ['falseTwo', 'Enter fake answer 2'],
            ['falseThree', 'Enter fake answer 3']
        ]
}


// Helper function to set multiple attributes to a field
function setAttr(element, attr) {
  for(let key in attr) {
    element.setAttribute(key, attr[key]);
  };
};


// Creates an input field for each question
function createInputField(fieldName, questionNumber, placeholder) {
    const attr = {
      'type' : 'text',
      'name' : `${fieldName}-${questionNumber}`,
      'id' : `${fieldName}-${questionNumber}`,
      'placeholder' : placeholder,
    };
    const field = document.createElement('input');
    setAttr(field, attr);
    return field;
  };


// Adds a new question field (question, answer, and type) to quiz form
function addQuestion(type) {
  const form = document.getElementById('create-quiz-question');
  const questionDiv = document.createElement('div');
  setAttr(questionDiv, {'class' : 'question'});
  // Set field depending on question type
  const field = questionTypefields[type];
  for (let f in field) {
    questionDiv.appendChild(createInputField(field[f][0], questionNumber, field[f][1]));
  };
  form.appendChild(questionDiv);
  questionNumber += 1;;
};


// Remove question div
function removeLastQuestion() {
    const form = document.getElementById('create-quiz-question');
    form.removeChild(form.lastElementChild);
  };

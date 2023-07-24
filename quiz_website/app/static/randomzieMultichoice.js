function randomizeField(divId) {
    const parentDiv = document.getElementById(divId);
    for(let i = 0; i < parentDiv.children.length; i++) {
        parentDiv.appendChild(parent.children[Math.random() * i | 0])
    }
    
};
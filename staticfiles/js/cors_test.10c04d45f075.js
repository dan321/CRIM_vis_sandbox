fetch("https://crimproject.org/relationships/2608/?format=json", {type: "cors", method: "GET"})
.then(response => console.log(response))
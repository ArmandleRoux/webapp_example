// This code checks if user had previously selected a theme
// Gets the selected theme from the browsers local storage
// If theres no key-value pair named 'theme' in the local storage, returns a null
// start
let theme = localStorage.getItem("theme");

if (theme == "dark") {
  document.body.style.backgroundColor = "black";
  document.body.style.color = "white";
} else {
  document.body.style.backgroundColor = "white";
  document.body.style.color = "black";
}
//end

// Create a button element using DOM method, createElement
const button = document.createElement("button");

// Change buttons attribute (text) using button object property
button.textContent = "Change theme";

// Function that runs when 'Change theme' button is clicked
function changeTheme() {
  if (document.body.style.backgroundColor == "black") {
    document.body.style.backgroundColor = "white";
    document.body.style.color = "black";
    localStorage.setItem("theme", "light");
    // Browser developer tools -> Application tab ->
    // Local storage -> Click http://127.0.0.1... ->
    // You can view/show the key value pair locally for better understanding
  } else {
    document.body.style.backgroundColor = "black";
    document.body.style.color = "white";
    localStorage.setItem("theme", "dark");
    // Browser developer tools -> Application tab ->
    // Local storage -> Click http://127.0.0.1... ->
    // You can view/show the key value pair locally for better understanding
  }
}

// Now the button's onclick event points to/references the function changeTheme
button.onclick = changeTheme;

// Finally add the button element as the body tag's child
document.body.append(button);

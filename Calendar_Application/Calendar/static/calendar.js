/*

let dayNamesShown = document.getElementsByClassName('day-name');
let events = document.getElementsByTagName('p');
let dayBodies = document.getElementsByClassName('calendar-day');
let monthyear = document.getElementById('month-year');

const data = document.currentScript.dataset;
let eventList = data.eventList;
alert(eventList);


let today = new Date();
const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const monthsOfYear = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

// Set the month and year of the header
monthyear.innerHTML = monthsOfYear[today.getMonth()] + " " + today.getFullYear();


// Select current day as today
for (let i=0; i<dayNamesShown.length; i++) {
    console.log(dayNamesShown[i].innerHTML);
    if (dayNamesShown[i].innerHTML == daysOfWeek[today.getDay()]) {
        dayBodies[i].classList.add('today');
    }
}

// Add event listener for each day
for (let i=0; i<dayBodies.length; i++) {
    events[i].addEventListener('click', function() { eventClick(i) });
}


function eventClick(i) {
}

*/
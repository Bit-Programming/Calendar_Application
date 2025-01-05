document.addEventListener('DOMContentLoaded', function () {
    const days = document.querySelectorAll('.calendar-day');
    const addEventButton = document.getElementById('add-event-btn');
    const addEventModal = document.getElementById('add-event-modal');

    const modal = document.getElementById('event-modal');
    const closeEventBtn = document.querySelector('.close-event-btn');
    const closeAddEventBtn = document.querySelector('.close-add-event-btn');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    const findButton = document.getElementById('find');

    const viewType = document.getElementById('heading').dataset.view;

    const firstdate = document.getElementById('heading').dataset.currentDate;
    console.log("viewtype:", viewType);
    document.getElementById('find-date').valueAsDate = new Date(firstdate);

    // Extract year out of date
    switch (viewType) {
        case 'month': {
            document.getElementById('headingtext').href = "/Calendar/" + firstdate.split("-")[0] + "/year";
            break;
        }
        case 'week': {
            document.getElementById('headingtext').href = "/Calendar/" + firstdate.split("-")[0] + "-" + firstdate.split("-")[1] + "/month";
            break;
        }
        case 'day': {
            document.getElementById('headingtext').href = "/Calendar/" + firstdate + "/week";
            break;
        }
    }
    

    days.forEach(day => {
        day.addEventListener('click', function () {
            const date = this.closest('.day').querySelector('.day-name').textContent.split('(')[1].split(')')[0];
            const eventList = document.getElementById('event-list');
            document.getElementById('event-date').value = date;
            console.log("date:", date);
            document.getElementById('find-date').valueAsDate = new Date(date);
    
            // Fetch events for the clicked day
            fetch(`/Calendar/event/ajax/date/${date}/`)
                .then(response => {
                    if (!response.ok) {
                        // If the response status is not OK, return a simulated error response
                        return { error: `HTTP error! Status: ${response.status}` };
                    }
                    return response.json(); // Parse JSON only if the response is OK
                })
                .then(data => {
                    eventList.innerHTML = ''; // Clear previous events
                    
                    if (data.error) {
                        // Show "No events" if there's an error or events are missing
                        eventList.innerHTML = '<p>No events</p>';
                    } else {
                        // Populate the event list if there are events
                        data.events.forEach(event => {
                            const eventItem = document.createElement('p');
                            eventItem.innerHTML = `<b>${event.name}</b><br><i>${event.start_time} - ${event.end_time}</i><br>${event.description}`;
                            eventList.appendChild(eventItem);
                        });
                    }
                    // Show the modal
                    modal.style.display = 'flex';
                })
                .catch(() => {
                    // Handle unexpected fetch errors gracefully without logging
                    eventList.innerHTML = '<p>No events</p>';
                    modal.style.display = 'flex';
                });
        });
    });

    const eventColorSelect = document.getElementById('event-color');

    function updateSelectColor() {
        const selectedOption = eventColorSelect.options[eventColorSelect.selectedIndex];
        const selectedColor = selectedOption.getAttribute('data-color');

        eventColorSelect.style.backgroundImage = `linear-gradient(to right, ${selectedColor} 0%, ${selectedColor} 15px, transparent 15px, transparent 100%)`;
        eventColorSelect.style.backgroundRepeat = 'no-repeat';
        eventColorSelect.style.backgroundPosition = 'left center';
        eventColorSelect.style.backgroundSize = '100% 100%';
        eventColorSelect.style.paddingLeft = '20px'; // Adjust padding if necessary
    }

    // Set the initial color
    updateSelectColor();

    // Update color on change
    eventColorSelect.addEventListener('change', updateSelectColor);
    

    addEventButton.addEventListener('click', () => addEventModal.style.display = 'flex');
    closeAddEventBtn.addEventListener('click', () => addEventModal.style.display = 'none');
    closeEventBtn.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (e) => {
        if (e.target === addEventModal) addEventModal.style.display = 'none';
        if (e.target === modal) modal.style.display = 'none';
    });

    addEventModal.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(document.getElementById('add-event-form'));
        fetch('/Calendar/event/add/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Reload to display the new event
            } else {
                alert('Error: ' + data.error);
            }
        });
    });


    function convertTZ(date, tzString) {
        return new Date((typeof date === "string" ? new Date(date) : date).toLocaleString("en-US", {timeZone: tzString}));   
    }
    
    function navigateToDate(offset) {
        console.log("value", document.getElementById('heading').dataset.currentDate)
        // Sketchy
        const currentDate = new Date(new Date(document.getElementById('heading').dataset.currentDate).toLocaleString('en', {timeZone: 'UTC'}));
        

        console.log("currentDate", currentDate);

        let newDate = new Date(currentDate);

        let newDateStr = '';

        switch (viewType) {
            case 'day':
                newDate.setDate(currentDate.getDate() + offset);
                newDateStr = newDate.toISOString().split('T')[0];
                break;
            case 'week':
                newDate.setDate(currentDate.getDate() + offset * 7);
                newDateStr = newDate.toISOString().split('T')[0];
                break;
            case 'month':
                newDate.setMonth(currentDate.getMonth() + offset);
                newDateStr = newDate.toISOString().split('-')[0] + '-' + newDate.toISOString().split('-')[1];
                break;
            case 'year':
                newDate.setFullYear(currentDate.getFullYear() + offset);
                newDateStr = newDate.toISOString().split('-')[0];
                break;
        }

        console.log("newDate:", newDate);
        console.log("newDateStr:", newDateStr);
        
        window.location.href = `/Calendar/${newDateStr}/${viewType}`;
    }


    prevButton.addEventListener('click', () => navigateToDate(-1));
    nextButton.addEventListener('click', () => navigateToDate(1));


    findButton.addEventListener('click', () => {
        const date = document.getElementById('find-date').value;
        const views = document.getElementById('views');
        const viewType = views.options[views.selectedIndex].text;
        console.log("date:", date);
        console.log("viewType:", viewType);
        
        if (viewType === "Year") { // strip the year from the date
            window.location.href = `/Calendar/${date.split('-')[0]}/year`;
        }
        else if (viewType === "Month") { // strip the year and month from the date
            window.location.href = `/Calendar/${date.split('-')[0] + '-' + date.split('-')[1]}/month`;
        }
        else if (viewType === "Week") { // strip the year and month from the date
            window.location.href = `/Calendar/${date.split('-')[0] + '-' + date.split('-')[1] + '-' + date.split('-')[2]}/week`;
        }
        else if (viewType === "Day") { // strip the year and month from the date
            window.location.href = `/Calendar/${date}/day`;
        }
        
    });
});

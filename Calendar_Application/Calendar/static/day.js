const date = this.closest('.day').querySelector('.day-name').textContent.split('(')[1].split(')')[0];
const eventList = document.getElementById('event-list');
document.getElementById('event-date').value = date;

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
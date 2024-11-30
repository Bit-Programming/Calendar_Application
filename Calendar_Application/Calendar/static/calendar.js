document.addEventListener('DOMContentLoaded', function () {
    const days = document.querySelectorAll('.calendar-day');
    const addEventButton = document.getElementById('add-event-btn');
    const addEventForm = document.getElementById('add-event-form');

    const modal = document.getElementById('event-modal');
    const closeEventBtn = document.querySelector('.close-event-btn');
    const closeAddEventBtn = document.querySelector('.close-add-event-btn');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');

    days.forEach(day => {
        day.addEventListener('click', function () {
            const date = this.closest('.day').querySelector('.day-name').textContent.split('(')[1].split(')')[0];
            document.getElementById('event-date').value = date;

            // Fetch events for the clicked day
            fetch(`/Calendar/event/ajax/date/${date}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert('Error: ' + data.error);
                    } else {
                        const eventList = document.getElementById('event-list');
                        eventList.innerHTML = ''; // Clear previous events
                        data.events.forEach(event => {
                            const eventItem = document.createElement('p');
                            eventItem.innerHTML = `<b>${event.name}</b><br><i>${event.start_time} - ${event.end_time}</i><br>${event.description}`;
                            eventList.appendChild(eventItem);
                        });
                        modal.style.display = 'flex';
                    }
                });
        });
    });

    addEventButton.addEventListener('click', () => addEventForm.style.display = 'flex');
    closeAddEventBtn.addEventListener('click', () => addEventForm.style.display = 'none');
    closeEventBtn.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (e) => {
        if (e.target === addEventForm) addEventForm.style.display = 'none';
        if (e.target === modal) modal.style.display = 'none';
    });

    addEventForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
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
                alert('Event added successfully!');
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
        const viewType = document.getElementById('heading').dataset.view;

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

});

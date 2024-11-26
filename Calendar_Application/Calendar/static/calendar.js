document.addEventListener('DOMContentLoaded', function () {
    const eventElements = document.querySelectorAll('.event');
    const modal = document.getElementById('event-modal');
    const closeBtn = document.querySelector('.close-btn');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');

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

    eventElements.forEach(function (eventElement) {
        eventElement.addEventListener('click', function () {
            const eventId = this.dataset.eventId;
            fetch(`/Calendar/event/ajax/${eventId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert('Error: ' + data.error);
                    } else {
                        document.getElementById('event-name').textContent = data.name;
                        document.getElementById('event-date').textContent = data.event_date;
                        document.getElementById('event-description').textContent = data.description;
                        document.getElementById('event-start-time').textContent = data.start_time;
                        document.getElementById('event-end-time').textContent = data.end_time;
                        document.getElementById('event-location').textContent = data.place;
                        document.getElementById('event-color').textContent = data.color;
                        modal.style.display = 'flex';
                    }
                })
                .catch(console.error);
        });
    });

    closeBtn.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });
});

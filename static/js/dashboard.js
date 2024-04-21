const currentDate = new Date();

window.onload = function () {
    document.getElementById('currentDate').textContent = formatDate(currentDate);
    fetchHabitsForDate(currentDate);
}

// Function to format date
function formatDate(date) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Function to fetch habits for a specific date
async function fetchHabitsForDate(date) {
    const formattedDate = date.toISOString().split('T')[0]; // Format: YYYY-MM-DD
    const response = await fetch(`/habits?date=${formattedDate}`);
    const habits = await response.json();

    const habitsList = document.querySelector('.habit-list');
    habitsList.innerHTML = ''; // Clear existing habits

    for (const habit of habits) {
        const newHabitElement = document.createElement('div');
        newHabitElement.innerHTML = `<form id="habitForm_${habit.habit_id}" onchange="checkBox(event, this)">
                                                <input type="hidden" name="habit_id" value="${habit.habit_id}">
                                                <input type="checkbox" id="habit_${habit.habit_id}" name="completed" value="True" ${habit.is_completed ? 'checked' : ''}>
                                                <label class="habit-description" for="habit_${habit.habit_id}">${habit.habit_description}</label>
                                                <button type="button" onclick="showEditPopup('${habit.habit_id}', '${habit.habit_description}')">Edit</button>
                                                <button type="button" onclick="deleteHabit('${habit.habit_id}', event)">Delete</button>
                                            </form>`;
        habitsList.appendChild(newHabitElement);
    }
}

// Function to add a new habit
async function addHabit(event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    const response = await fetch('/addhabit', {
        method: 'POST',
        body: data,
    });

    const result = await response.json();
    if (result.success) {
        const habitsList = document.querySelector('.habit-list');
        const newHabitElement = document.createElement('div');
        newHabitElement.innerHTML = `<form id="habitForm_${result.habit_id}" onchange="checkBox(event, this)">
                                                <input type="hidden" name="habit_id" value="${result.habit_id}">
                                                <input type="checkbox" id="habit_${result.habit_id}" name="completed" value="True">
                                                <label class="habit-description" for="habit_${result.habit_id}">${data.get('habitdesc')}</label>
                                                <button type="button" onclick="showEditPopup('${result.habit_id}', '${data.get('habitdesc')}')">Edit</button>
                                                <button type="button" onclick="deleteHabit('${result.habit_id}', event)">Delete</button>
                                            </form>`;
        habitsList.appendChild(newHabitElement);
        form.reset();
    } else {
        alert(result.message);
    }
}

// Function to handle habit checkbox
function checkBox(event, form) {
    event.preventDefault();
    const checkbox = form.querySelector('[name="completed"]');
    const formData = new FormData(form);
    formData.append('completed', checkbox.checked ? 'True' : 'False');

    fetch('/checkbox', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Habit completion logged');
            } else {
                alert('Failed to log habit completion');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to show edit popup
function showEditPopup(habitId, currentDescription) {
    document.getElementById('editHabitId').value = habitId;
    document.getElementById('newHabitDescription').value = currentDescription;
    document.getElementById('editPopup').style.display = 'block';
}

// Function to close edit popup
function closeEditPopup() {
    document.getElementById('editPopup').style.display = 'none';
}

// Function to submit edited habit
function submitEdit(event) {
    event.preventDefault();
    const form = document.getElementById('editForm');
    const formData = new FormData(form);
    formData.append('date', getCurrentDateString()); // Append the date to the form data
    fetch('/edithabit', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Habit updated');
                document.querySelector(`label[for='habit_${form.elements['habit_id'].value}']`).textContent = form.elements['new_description'].value;
                closeEditPopup();
            } else {
                alert('Failed to update habit');
            }
            form.reset();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to delete a habit
function deleteHabit(habitId, event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append('habit_id', habitId);
    formData.append('date', getCurrentDateString()); // Append the date to the form data

    fetch('/deletehabit', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Habit deleted');
                const habitElement = document.getElementById(`habitForm_${habitId}`);
                habitElement.parentNode.removeChild(habitElement);
                closeEditPopup();
            } else {
                alert('Failed to delete habit');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to get current date in YYYY-MM-DD format
function getCurrentDateString() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    const day = currentDate.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Function to navigate to previous date
function previousDate() {
    currentDate.setDate(currentDate.getDate() - 1);
    updateDate();
}

// Function to navigate to next date
function nextDate() {
    currentDate.setDate(currentDate.getDate() + 1);
    updateDate();
}

// Function to update the date and habits for the selected date
function updateDate() {
    document.getElementById('currentDate').textContent = formatDate(currentDate);
    fetchHabitsForDate(currentDate);
}
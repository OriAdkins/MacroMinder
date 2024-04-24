// Function to format date
function formatDate(date) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
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

async function coachAddHabit(event) {
    event.preventDefault();

    // Retrieve user_id from hidden input
    const userId = document.getElementById('user_id').value;

    // Retrieve habit description from input field
    const habitDescription = document.getElementById('habitdesc').value;

    // Create data object including user_id and habit description
    const habitData = {
        user_id: userId,
        habitdesc: habitDescription
    };

    // Send POST request with JSON data
    const response = await fetch('/coachAddHabit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(habitData)
    });

    // Handle response
    const result = await response.json();
    if (result.success) {
        // Process successful response
        const habitsList = document.querySelector('.habit-list');
        const newHabitElement = document.createElement('div');
        newHabitElement.innerHTML = `<form id="habitForm_${result.habit_id}" onchange="checkBox(event, this)">
                                        <input type="hidden" name="habit_id" value="${result.habit_id}">
                                        <input type="checkbox" id="habit_${result.habit_id}" name="completed" value="True">
                                        <label class="habit-description" for="habit_${result.habit_id}">${habitData.habitdesc}</label>
                                        <button type="button" onclick="showEditPopup('${result.habit_id}', '${habitData.habitdesc}')">Edit</button>
                                        <button type="button" onclick="deleteHabit('${result.habit_id}', event)">Delete</button>
                                    </form>`;
        habitsList.appendChild(newHabitElement);
        // Reset input field
        document.getElementById('habitdesc').value = '';
    } else {
        // Handle unsuccessful response
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
                location.reload()
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

function previousDate() {
    // Send POST request to /prevday endpoint
    fetch('/prevday', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => {
        if (response.ok) {
            // Reload the page or update the content as needed
            location.reload(); // Reload the page to reflect the updated date
        } else {
            console.error('Failed to set previous day');
        }
    }).catch(error => {
        console.error('Error:', error);
    });

}

function nextDate() {
    // Send POST request to /nextday endpoint

    fetch('/nextday', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => {
        if (response.ok) {
            // Reload the page or update the content as needed
            location.reload(); // Reload the page to reflect the updated date
        } else {
            console.error('Failed to set next day');
        }
    }).catch(error => {
        console.error('Error:', error);
    });

}

// Function to log macros
async function logMacros(event) {
    event.preventDefault();

    const protein = document.getElementById('proteinInput').value;
    const calories = document.getElementById('caloriesInput').value;
    const weightlbs = document.getElementById('weightInput').value;

    const data = {
        protein: protein,
        calories: calories,
        weightlbs: weightlbs,
        date: getCurrentDateString()
    };

    const response = await fetch('/addmacros', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.success) {
        console.log('Macros logged');
        location.reload()
    } else {
        alert('Failed to log macros');
    }

    updateDate();
}

// Function to log macros
async function lifecoachLogMacros(event) {
    event.preventDefault();

    const protein = document.getElementById('proteinInput').value;
    const calories = document.getElementById('caloriesInput').value;
    const weightlbs = document.getElementById('weightInput').value;

    const user_id = document.getElementById('user_id').value; // Get user_id from hidden input

    const data = {
        user_id: user_id, // Include user_id in the data
        protein: protein,
        calories: calories,
        weightlbs: weightlbs,
        date: getCurrentDateString()
    };

    const response = await fetch('/coach/logmacros', { // Use the new endpoint for coaches
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.success) {
        console.log('Macros logged');
        location.reload()
    } else {
        alert('Failed to log macros');
    }

    updateDate();
}

function getCurrentDateString() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    const day = currentDate.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}
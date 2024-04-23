//let currentDate = new Date("{{ current_date }}");

window.onload = function () {
    //updateDateDisplay(currentDate);
    //document.getElementById('currentDate').textContent = formatDate(currentDate);
    //fetchHabitsForDate(currentDate);
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

// Function to get current date in YYYY-MM-DD format
function getCurrentDateString() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    const day = currentDate.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Function to navigate to previous date
//function previousDate() {
 //   currentDate.setDate(currentDate.getDate() - 1);
   // updateDate();
//}

function updateDateDisplay(date) {
    document.getElementById("currentDate").textContent = formatDate(date);
}

function previousDate() {
    // Send POST request to /prevday endpoint

    //currentDate.setDate(currentDate.getDate() - 1);
    //updateDateDisplay(currentDate);

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

    //currentDate.setDate(currentDate.getDate() + 1);
    //updateDateDisplay(currentDate);

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


// Get today's date for the habit tracker
//let today = new Date().toISOString().substr(0, 10);
//document.getElementById("currentDate").innerText = today;

// Function to fetch macros for a specific date
async function fetchMacrosForDate(date) {
    const formattedDate = date.toISOString().split('T')[0]; // Format: YYYY-MM-DD
    const response = await fetch(`/get_macros?date=${formattedDate}`);
    const macros = await response.json();

    document.getElementById('proteinInput').value = '';
    document.getElementById('caloriesInput').value = '';
    document.getElementById('weightInput').value = '';

    if (macros.length > 0) {
        document.getElementById('proteinInput').value = macros[0].protein;
        document.getElementById('caloriesInput').value = macros[0].calories;
        document.getElementById('weightInput').value = macros[0].weightlbs;
    }
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



// Function to show edit macros popup
function showEditMacrosPopup(macroId, currentProtein, currentCalories, currentWeight) {
    document.getElementById('editMacroId').value = macroId;
    document.getElementById('newProteinInput').value = currentProtein;
    document.getElementById('newCaloriesInput').value = currentCalories;
    document.getElementById('newWeightInput').value = currentWeight;
    document.getElementById('editMacrosPopup').style.display = 'block';
}

// Function to close edit macros popup
function closeEditMacrosPopup() {
    document.getElementById('editMacrosPopup').style.display = 'none';
}

// Function to submit edited macros
async function submitEditMacros(event) {
    event.preventDefault();
    const form = document.getElementById('editMacrosForm');
    const data = {
        macro_id: form.elements['macro_id'].value,
        protein: form.elements['new_protein'].value,
        calories: form.elements['new_calories'].value,
        weightlbs: form.elements['new_weight'].value
    };

    const response = await fetch('/editmacros', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.success) {
        console.log('Macros updated');
        closeEditMacrosPopup();
        updateDate();
    } else {
        alert('Failed to update macros');
    }
}

// Function to delete macros
async function deleteMacros(macroId, event) {
    event.preventDefault();

    const data = {
        macro_id: macroId
    };

    const response = await fetch('/deletemacros', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.success) {
        console.log('Macros deleted');
        updateDate();
    } else {
        alert('Failed to delete macros');
    }
}

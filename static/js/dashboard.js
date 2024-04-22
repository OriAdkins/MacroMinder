const currentDate = new Date();

window.onload = function () {
    document.getElementById('currentDate').textContent = formatDate(currentDate);
    fetchHabitsForDate(currentDate);
    fetchMacrosForDate(currentDate); // Add this line to fetch macros for the current date
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

        // Make inputs read-only
        document.getElementById('proteinInput').setAttribute('readonly', true);
        document.getElementById('caloriesInput').setAttribute('readonly', true);
        document.getElementById('weightInput').setAttribute('readonly', true);
    }
}
// ------------------- Macros -------------------
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

        document.getElementById('proteinDisplay').innerText = protein;
        document.getElementById('caloriesDisplay').innerText = calories;
        document.getElementById('weightDisplay').innerText = weightlbs;

        // Make inputs read-only
        document.getElementById('proteinInput').setAttribute('readonly', true);
        document.getElementById('caloriesInput').setAttribute('readonly', true);
        document.getElementById('weightInput').setAttribute('readonly', true);
    } else {
        alert('Failed to log macros');
    }
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
    } else {
        alert('Failed to delete macros');
    }
}
// ------------------- Habits -------------------
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

// Function to show habit edit popup
function showEditPopup(habitId, currentDescription) {
    document.getElementById('editHabitId').value = habitId;
    document.getElementById('newHabitDescription').value = currentDescription;
    document.getElementById('editPopup').style.display = 'block';
}

// Function to close habit edit popup
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
    fetchMacrosForDate(currentDate);
}

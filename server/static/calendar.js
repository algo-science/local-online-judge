function renderCalendar() {
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    const app = document.getElementById('app');
    app.innerHTML = `
        <div class="calendar-container">
            <div class="calendar-header">
                <button id="prev-month"><</button>
                <h2 id="month-year">${today.toLocaleString('default', { month: 'long' })} ${currentYear}</h2>
                <button id="next-month">></button>
            </div>
            <div class="calendar-grid"></div>
        </div>
        <div class="task-view" style="margin-top: 20px;">
            <h3>Tasks for <span id="selected-date"></span></h3>
            <ul id="task-list"></ul>
            <div class="form-group" style="margin-top: 10px;">
                <input type="text" id="new-task-input" placeholder="Add a new task...">
                <button onclick="addTask()">Add Task</button>
            </div>
        </div>
    `;

    const monthYear = document.getElementById('month-year');
    const calendarGrid = document.querySelector('.calendar-grid');
    const selectedDateEl = document.getElementById('selected-date');
    let selectedDate = today.toISOString().slice(0, 10);

    function generateCalendar(month, year) {
        calendarGrid.innerHTML = '';
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        monthYear.textContent = `${new Date(year, month).toLocaleString('default', { month: 'long' })} ${year}`;

        // Create headers
        ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].forEach(day => {
            const dayHeader = document.createElement('div');
            dayHeader.classList.add('calendar-day', 'calendar-header-day');
            dayHeader.textContent = day;
            calendarGrid.appendChild(dayHeader);
        });
        
        for (let i = 0; i < firstDay; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.classList.add('calendar-day');
            calendarGrid.appendChild(emptyCell);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement('div');
            dayCell.classList.add('calendar-day');
            dayCell.textContent = day;
            
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            dayCell.dataset.date = dateStr;

            if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayCell.classList.add('today');
            }
            
            dayCell.addEventListener('click', () => {
                document.querySelectorAll('.calendar-day').forEach(d => d.classList.remove('selected'));
                dayCell.classList.add('selected');
                selectedDate = dateStr;
                selectedDateEl.textContent = new Date(dateStr + 'T00:00:00').toLocaleDateString();
                loadTasks(selectedDate);
            });
            calendarGrid.appendChild(dayCell);
        }
    }

    async function loadTasks(dateStr) {
        const taskList = document.getElementById('task-list');
        taskList.innerHTML = '<li>Loading...</li>';
        try {
            const res = await fetch(`/api/calendar/${dateStr}`);
            const tasks = await res.json();
            taskList.innerHTML = tasks.length > 0
                ? tasks.map(task => `
                    <li class="${task.completed ? 'completed' : ''}">
                        <input type="checkbox" ${task.completed ? 'checked' : ''} onchange="updateTaskStatus('${dateStr}', ${task.id}, this.checked)">
                        <span>${task.description}</span>
                        <button onclick="deleteTask('${dateStr}', ${task.id})" class="btn-sm btn-danger" style="margin-left: 10px;">Delete</button>
                    </li>
                `).join('')
                : '<li>No tasks for this day.</li>';
        } catch (e) {
            taskList.innerHTML = '<li>Error loading tasks.</li>';
        }
    }

    window.addTask = async function() {
        const input = document.getElementById('new-task-input');
        const description = input.value.trim();
        if (description) {
            await fetch(`/api/calendar/${selectedDate}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description })
            });
            input.value = '';
            loadTasks(selectedDate);
        }
    }

    window.updateTaskStatus = async function(dateStr, taskId, completed) {
        await fetch(`/api/calendar/${dateStr}/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completed })
        });
        loadTasks(dateStr);
    }

    window.deleteTask = async function(dateStr, taskId) {
        if (confirm('Are you sure you want to delete this task?')) {
            await fetch(`/api/calendar/${dateStr}/${taskId}`, {
                method: 'DELETE'
            });
            loadTasks(dateStr);
        }
    }

    document.getElementById('prev-month').addEventListener('click', () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        generateCalendar(currentMonth, currentYear);
    });

    document.getElementById('next-month').addEventListener('click', () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        generateCalendar(currentMonth, currentYear);
    });

    generateCalendar(currentMonth, currentYear);
    
    // Select today's date and load its tasks by default
    const todayCell = document.querySelector(`.calendar-day[data-date="${selectedDate}"]`);
    if (todayCell) {
        todayCell.classList.add('selected');
        selectedDateEl.textContent = today.toLocaleDateString();
        loadTasks(selectedDate);
    }
}
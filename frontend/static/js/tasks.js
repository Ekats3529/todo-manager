import { getTasks, createTask, updateTask, deleteTask } from './api.js';

const taskList = document.getElementById('task-list');
const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');

async function renderTasks() {
  const tasks = await getTasks();
  taskList.innerHTML = '';
  tasks.forEach(task => {
    const li = document.createElement('li');
    li.textContent = task.title;
    li.style.textDecoration = task.completed ? 'line-through' : 'none';

    const doneBtn = document.createElement('button');
    doneBtn.textContent = task.completed ? 'Вернуть' : 'Выполнить';
    doneBtn.onclick = async () => {
      await updateTask(task.id, { completed: !task.completed });
      renderTasks();
    };

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Удалить';
    deleteBtn.onclick = async () => {
      await deleteTask(task.id);
      renderTasks();
    };

    li.appendChild(doneBtn);
    li.appendChild(deleteBtn);
    taskList.appendChild(li);
  });
}

taskForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!taskInput.value.trim()) return;
  await createTask(taskInput.value);
  taskInput.value = '';
  renderTasks();
});

renderTasks();

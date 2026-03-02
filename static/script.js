/* CGPA Calculator - Frontend JavaScript */

let subjects = [];

// DOM Elements
const subjectForm = document.getElementById('subjectForm');
const subjectNameInput = document.getElementById('subjectName');
const marksInput = document.getElementById('marks');
const creditsInput = document.getElementById('credits');
const tableBody = document.getElementById('tableBody');
const calculateBtn = document.getElementById('calculateBtn');
const resetBtn = document.getElementById('resetBtn');
const gradeInfoBtn = document.getElementById('gradeInfoBtn');
const resultsSection = document.getElementById('resultsSection');
const actionButtons = document.getElementById('actionButtons');
const toast = document.getElementById('toast');
const modal = document.getElementById('gradeModal');
const closeBtn = document.querySelector('.close');

// Event Listeners
subjectForm.addEventListener('submit', addSubject);
calculateBtn?.addEventListener('click', calculateCGPA);
resetBtn?.addEventListener('click', resetAll);
gradeInfoBtn.addEventListener('click', showGradeInfo);
closeBtn.addEventListener('click', closeModal);
window.addEventListener('click', closeModalOnClick);

/**
 * Add a subject to the list
 */
function addSubject(e) {
    e.preventDefault();

    const name = subjectNameInput.value.trim();
    const marks = parseFloat(marksInput.value);
    const credits = parseFloat(creditsInput.value);

    // Validation
    if (!name) {
        showToast('Please enter subject name', 'error');
        return;
    }

    if (isNaN(marks) || marks < 0 || marks > 100) {
        showToast('Marks must be between 0 and 100', 'error');
        return;
    }

    if (isNaN(credits) || credits <= 0) {
        showToast('Credits must be a positive number', 'error');
        return;
    }

    // Add subject
    subjects.push({
        name,
        marks,
        credits,
    });

    // Clear form
    subjectForm.reset();
    subjectNameInput.focus();

    // Update display
    updateTable();
    showToast(`${name} added successfully!`, 'success');

    // Show action buttons
    if (subjects.length > 0) {
        actionButtons.style.display = 'flex';
    }
}

/**
 * Update the subjects table
 */
function updateTable() {
    if (subjects.length === 0) {
        tableBody.innerHTML = `
            <tr class="empty-row">
                <td colspan="7" style="text-align: center; padding: 20px;">
                    No subjects added yet
                </td>
            </tr>
        `;
        resultsSection.style.display = 'none';
        return;
    }

    tableBody.innerHTML = subjects.map((subject, index) => `
        <tr>
            <td>${subject.name}</td>
            <td>${subject.marks.toFixed(1)}</td>
            <td>${subject.grade || '-'}</td>
            <td>${subject.gradePoints !== undefined ? subject.gradePoints.toFixed(2) : '-'}</td>
            <td>${subject.credits.toFixed(1)}</td>
            <td>${subject.weightedPoints !== undefined ? subject.weightedPoints.toFixed(2) : '-'}</td>
            <td>
                <button class="btn-delete" onclick="removeSubject(${index})">Remove</button>
            </td>
        </tr>
    `).join('');
}

/**
 * Remove a subject by index
 */
function removeSubject(index) {
    const subjectName = subjects[index].name;
    subjects.splice(index, 1);
    updateTable();
    showToast(`${subjectName} removed`, 'success');

    if (subjects.length === 0) {
        actionButtons.style.display = 'none';
        resultsSection.style.display = 'none';
    }
}

/**
 * Calculate CGPA by calling the backend API
 */
async function calculateCGPA() {
    if (subjects.length === 0) {
        showToast('Please add at least one subject', 'error');
        return;
    }

    const payload = {
        subjects: subjects.map(s => ({
            name: s.name,
            marks: s.marks,
            credits: s.credits
        }))
    };

    try {
        calculateBtn.disabled = true;
        calculateBtn.textContent = 'Calculating...';

        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            showToast(data.error || 'Calculation failed', 'error');
            return;
        }

        // Update subjects with calculated values
        data.subjects.forEach((subject, index) => {
            subjects[index].grade = subject.grade;
            subjects[index].gradePoints = subject.grade_points;
            subjects[index].weightedPoints = subject.weighted_points;
        });

        // Update table with grades
        updateTable();

        // Display results
        displayResults(data);
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        showToast('CGPA calculated successfully!', 'success');

    } catch (error) {
        showToast('An error occurred: ' + error.message, 'error');
        console.error('Error:', error);
    } finally {
        calculateBtn.disabled = false;
        calculateBtn.textContent = 'Calculate CGPA';
    }
}

/**
 * Display calculation results
 */
function displayResults(data) {
    document.getElementById('totalCredits').textContent = data.total_credits.toFixed(1);
    document.getElementById('totalWeightedPoints').textContent = data.total_weighted_points.toFixed(2);
    document.getElementById('cgpa').textContent = data.cgpa.toFixed(2);
}

/**
 * Reset all subjects
 */
function resetAll() {
    if (subjects.length === 0) {
        showToast('No subjects to reset', 'error');
        return;
    }

    if (confirm('Are you sure you want to reset all subjects? This action cannot be undone.')) {
        subjects = [];
        updateTable();
        resultsSection.style.display = 'none';
        actionButtons.style.display = 'none';
        subjectForm.reset();
        showToast('All subjects cleared', 'success');
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

/**
 * Show grade information modal
 */
async function showGradeInfo() {
    try {
        const response = await fetch(`/api/grade-info`);
        const data = await response.json();

        if (!response.ok) {
            showToast(data.error || 'Failed to load grade info', 'error');
            return;
        }

        // Build grade table
        const tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Marks Range</th>
                        <th>Grade</th>
                        <th>Grade Points</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.grades.map(g => `
                        <tr>
                            <td>${g.range}</td>
                            <td><strong>${g.grade}</strong></td>
                            <td>${g.points.toFixed(2)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;

        document.getElementById('gradeTable').innerHTML = tableHTML;
        modal.style.display = 'flex';

    } catch (error) {
        showToast('Error loading grade info: ' + error.message, 'error');
        console.error('Error:', error);
    }
}

/**
 * Close modal
 */
function closeModal() {
    modal.style.display = 'none';
}

/**
 * Close modal when clicking outside
 */
function closeModalOnClick(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateTable();
});

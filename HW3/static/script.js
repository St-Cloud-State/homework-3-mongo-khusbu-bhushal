async function submitApplication() {
    const name = document.getElementById('applicantName').value;
    const zipcode = document.getElementById('zipcode').value;

    const response = await fetch('/api/add_application', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, zipcode })
    });

    const data = await response.json();

    // ✅ Show confirmation message in a visible area
    document.getElementById('confirmationMessage').innerText = 
        `Application submitted successfully! Your Application ID is: ${data.application_id}`;

    // ✅ Automatically fill in the Application ID input field
    document.getElementById('applicationId').value = data.application_id;
}


async function checkStatus() {
    const applicationId = document.getElementById('applicationId').value;
    const response = await fetch(`/api/status/${applicationId}`);
    const data = await response.json();
    document.getElementById('statusDisplay').innerText = data.status || data.message;
}

async function updateStatus() {
    const applicationId = document.getElementById('applicationId').value;
    const new_status = document.getElementById('newStatus').value;

    const response = await fetch('/api/change_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ application_id: applicationId, new_status })
    });

    const data = await response.json();
    alert(data.message);
}

async function addNote() {
    const applicationId = document.getElementById('applicationId').value;
    const note = document.getElementById('note').value;

    const response = await fetch('/api/add_note', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ application_id: applicationId, note })
    });

    const data = await response.json();
    alert(data.message);
}

async function viewDetails() {
    const applicationId = document.getElementById('applicationId').value;
    const response = await fetch(`/api/details/${applicationId}`);
    const data = await response.json();

    document.getElementById('applicationDetails').innerText = JSON.stringify(data, null, 2);
}

// ============================
// 🌐 Backend Base URL
// ============================
const API_BASE = "http://127.0.0.1:8000/api";
const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

// ============================
// 🚪 Logout
// ============================
function logout() {
  localStorage.clear();
  window.location.href = "./index.html";
}

// ============================
// 🔐 LOGIN
// ============================
const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
      const res = await fetch(`${API_BASE}/auth/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (res.ok && data.access) {
        localStorage.setItem("token", data.access);
        localStorage.setItem("role", data.role);
        localStorage.setItem("username", data.username);

        if (data.role === "admin") {
          window.location.href = "./admin-dashboard.html";
        } else {
          window.location.href = "./patient-dashboard.html";
        }
      } else {
        alert("❌ Invalid username or password.");
      }
    } catch (err) {
      console.error("Login error:", err);
      alert("🚨 Server error. Check backend or network.");
    }
  });
}

// ============================
// 🧑 REGISTER
// ============================
const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("reg-username").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value.trim();

    try {
      const res = await fetch(`${API_BASE}/auth/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        alert("✅ Registration successful. Please log in.");
        registerForm.reset();
      } else {
        const msg = data.detail || Object.values(data).join(", ");
        alert(`❌ Registration failed: ${msg}`);
      }
    } catch (err) {
      console.error("Register error:", err);
      alert("🚨 Could not connect to server.");
    }
  });
}



// ============================
// ➕ Add Doctor
// ============================
const addDoctorForm = document.getElementById("add-doctor-form");
if (addDoctorForm) {
  addDoctorForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("doctor-name").value;
    const specialization = document.getElementById("doctor-specialization").value;

    const res = await fetch(`${API_BASE}/doctors/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name, specialization }),
    });

    if (res.ok) {
      addDoctorForm.reset();
      loadAdminDashboard();
    } else {
      alert("❌ Failed to add doctor.");
    }
  });
}

// ============================
// 🩺 Assign Doctor to Patient
// ============================
async function assignDoctor(patientId) {
  const selectedDoctor = document.getElementById(`doctor-select-${patientId}`).value;
  if (!selectedDoctor) return alert("Please select a doctor");

  // ✅ check for duplicate before sending to backend
  const mappingsRes = await fetch(`${API_BASE}/mappings/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const mappings = await mappingsRes.json();
  const alreadyMapped = mappings.find(m => m.patient === patientId && m.doctor == selectedDoctor);

  if (alreadyMapped) {
    alert("⚠️ This patient is already assigned to this doctor.");
    return;
  }

  // ✅ assign doctor only if not already mapped
  const res = await fetch(`${API_BASE}/mappings/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ patient: patientId, doctor: selectedDoctor }),
  });

  if (res.ok) {
    loadAdminDashboard();
  } else {
    const err = await res.json();
    console.error("Assign doctor error:", err);
    alert(`❌ Failed to assign doctor: ${err.detail || "Try again"}`);
  }
}

// ============================
// 👑 Admin Dashboard
// ============================
// ============================
// 👑 Admin Dashboard - Updated
// ============================
async function loadAdminDashboard() {
  if (role !== "admin") {
    window.location.href = "./patient-dashboard.html";
    return;
  }

  const [patients, doctors, mappings] = await Promise.all([
    fetch(`${API_BASE}/patients/`, { headers: { Authorization: `Bearer ${token}` } }).then(r => r.json()),
    fetch(`${API_BASE}/doctors/`, { headers: { Authorization: `Bearer ${token}` } }).then(r => r.json()),
    fetch(`${API_BASE}/mappings/`, { headers: { Authorization: `Bearer ${token}` } }).then(r => r.json())
  ]);

  // Render Patients Table
  const patientTable = document.getElementById("admin-patient-table");
  patientTable.innerHTML = "";

  patients.forEach((p) => {
    const mapping = mappings.find((m) => m.patient === p.id);
    const currentDoctor = mapping ? mapping.doctor : null;

    let doctorOptions = `<option value="">-- Select Doctor --</option>`;
    doctors.forEach((d) => {
      doctorOptions += `<option value="${d.id}" ${d.id === currentDoctor ? "selected" : ""}>${d.name}</option>`;
    });

 patientTable.innerHTML += `
  <tr id="row-${p.id}">
    <td>${p.id}</td>
    <td><input id="edit-name-${p.id}" class="editable" type="text" value="${p.name}"></td>
    <td><input id="edit-age-${p.id}" class="editable" type="number" value="${p.age}"></td>
    <td><input id="edit-disease-${p.id}" class="editable" type="text" value="${p.disease}"></td>
    <td>
      <select id="doctor-select-${p.id}">
        ${doctorOptions}
      </select>
    </td>
    <td>
      <button type="button" onclick="updatePatient(${p.id})">💾 Update</button>
      <button type="button" onclick="deletePatient(${p.id})">🗑️ Delete</button>
    </td>
  </tr>
`;

  });

  // Render Doctors Table
  const doctorTable = document.getElementById("admin-doctor-table");
  doctorTable.innerHTML = "";

  doctors.forEach((d) => {
    const assignedPatients = mappings
      .filter((m) => m.doctor === d.id)
      .map((m) => {
        const patient = patients.find((p) => p.id === m.patient);
        return patient ? patient.name : "Unknown";
      });

    doctorTable.innerHTML += `
      <tr>
        <td>${d.id}</td>
        <td>${d.name}</td>
        <td>${d.specialization}</td>
        <td>${assignedPatients.length > 0 ? assignedPatients.join(", ") : "No patients"}</td>
      </tr>
    `;
  });
}


// ============================
// 🧑 PATIENT DASHBOARD with visible message
// ============================
async function ensurePatientExists() {
  const res = await fetch(`${API_BASE}/patients/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const patients = await res.json();

  const userPatient = patients.length > 0 ? patients[0] : null;

  if (!userPatient) {
    document.getElementById("symptom-form").style.display = "block";
    document.getElementById("patient-table-container").style.display = "none";
  } else {
    document.getElementById("symptom-form").style.display = "none";
    document.getElementById("patient-table-container").style.display = "table";
    loadPatientDashboard();
  }
}



async function submitPatientDetails() {
  const age = document.getElementById("form-age").value.trim();
  const symptoms = document.getElementById("form-symptoms").value.trim();

  if (!age || !symptoms) return alert("Please enter all fields.");

  const res = await fetch(`${API_BASE}/patients/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      name: localStorage.getItem("username"),
      age: age,
      disease: symptoms
    })
  });

  if (res.ok) {
    ensurePatientExists();
    loadPatientDashboard();
  } else {
    alert("❌ Failed to save details.");
  }
}

// ============================
// ✏️ Update Patient Details — Final Fixed
// ============================
async function updatePatient(id) {
  // 🧠 Always declare your variables first
  const patientIdNum = Number(id);
  const name = document.getElementById(`edit-name-${id}`).value.trim();
  const age = document.getElementById(`edit-age-${id}`).value.trim();
  const disease = document.getElementById(`edit-disease-${id}`).value.trim();
  const newDoctorId = Number(document.getElementById(`doctor-select-${id}`).value);

  // 1️⃣ Update patient details
  const res = await fetch(`${API_BASE}/patients/${patientIdNum}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name, age, disease }),
  });

  if (!res.ok) {
    alert("❌ Failed to update patient details");
    return;
  }

  // 2️⃣ Fetch all mappings
  const mappingsRes = await fetch(`${API_BASE}/mappings/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const mappings = await mappingsRes.json();

  // 🧭 Properly find the mapping for THIS patient
  const existingMapping = mappings.find(m => Number(m.patient) === patientIdNum);

  // 3️⃣ Delete old mapping if it exists and changed
  if (existingMapping && existingMapping.doctor !== newDoctorId) {
    await fetch(`${API_BASE}/mappings/${existingMapping.id}/`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    });
  }

  // 4️⃣ Add new mapping if selected
  if (newDoctorId && (!existingMapping || existingMapping.doctor !== newDoctorId)) {
    await fetch(`${API_BASE}/mappings/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ patient: patientIdNum, doctor: newDoctorId }),
    });
  }

  // 5️⃣ UI Feedback
  const row = document.getElementById(`row-${id}`);
  row.style.background = "#e6ffe6";
  setTimeout(() => (row.style.background = ""), 1000);

  // 6️⃣ Delay refresh to avoid race conditions
  setTimeout(loadAdminDashboard, 300);
}


// ============================
// 🗑️ Delete Patient
// ============================
async function deletePatient(id) {
  if (!confirm("Are you sure you want to delete this patient?")) return;

  const res = await fetch(`${API_BASE}/patients/${id}/`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.ok) {
    loadAdminDashboard();
  } else {
    alert("❌ Failed to delete patient.");
  }
}


async function loadPatientDashboard() {
  const res = await fetch(`${API_BASE}/patients/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const patients = await res.json();

  // 👉 Backend already filters by logged-in user
  const userPatient = patients.length > 0 ? patients[0] : null;

  const tableBody = document.getElementById("patient-table");
  tableBody.innerHTML = "";

  if (userPatient) {
    // Fetch mapping to find assigned doctor
    const mappingsRes = await fetch(`${API_BASE}/mappings/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const mappings = await mappingsRes.json();
    const userMapping = mappings.find(m => m.patient === userPatient.id);

    let assignedDoctorName = "Not Assigned";
    if (userMapping) {
      const doctorRes = await fetch(`${API_BASE}/doctors/${userMapping.doctor}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const doctor = await doctorRes.json();
      assignedDoctorName = doctor.name;
    }

    tableBody.innerHTML = `
      <tr>
        <td>${userPatient.name}</td>
        <td>${userPatient.age}</td>
        <td>${userPatient.disease}</td>
        <td>${assignedDoctorName}</td>
        <td>
          <input type="text" id="update-symptoms" placeholder="New symptoms">
          <button onclick="updateSymptoms(${userPatient.id})">Update</button>
        </td>
      </tr>
    `;
  }
}





// ============================
// 📄 Page Load Handlers
// ============================
// ============================
// 📄 Page Load Handlers
// ============================
if (window.location.pathname.includes("admin-dashboard.html")) {
  loadAdminDashboard();
}

if (window.location.pathname.includes("patient-dashboard.html")) {
  ensurePatientExists();        // 🩺 Call modal logic for first time users
  loadPatientDashboard();       // 📋 Load patient data if available
}


## 🏥 Healthcare Management System
### A backend-focused healthcare management system with a minimal user interface. The project enables secure authentication and role-based access, allowing administrators to efficiently manage patient and doctor data. Patients are seamlessly mapped to doctors, ensuring organized and streamlined healthcare service management.
---

### 📂 Project Structure

```
healthcare_project/
│
├── healthcare/                          # Main Django project folder
│   ├── healthcare/                      # Django core settings (project folder)
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── api/                             # Example: Django app for APIs
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── manage.py                        # Django entry point
│   │
│   ├── healthcare-frontend/             # Static frontend
│   │   ├── index.html
│   │   ├── admin-dashboard.html
│   │   ├── patient-dashboard.html
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│
├── .git/
├── requirements.txt                     # Python dependencies
├── README.md
└── .env                                 # (Optional) Environment variables

```

---

## ✨ Features

* 🔐 **User Authentication** — Secure login and registration for patients and admins.
* 🧑‍⚕️ **Role-Based Dashboards** — Separate dashboards for patients and administrators.
* 🩺 **Patient Management** — Add, view, and update patient records.
* 📅 **Appointment Scheduling** — Streamlined appointment booking and tracking (planned/optional).
* 📊 **Responsive Frontend** — Lightweight frontend with HTML, CSS, and JavaScript.

---

## 🛠️ Tech Stack

| Component  | Technology                    |
| ---------- | ----------------------------- |
| Backend    | Python, Django REST Framework |
| Frontend   | HTML5, CSS3, JavaScript       |
| Database   | PostgreSQL                    |
| Versioning | Git                           |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd healthcare
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
# or
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*(Make sure `Django` and `djangorestframework` are installed.)*

### 4. Set up the Database

* Configure `settings.py` with your PostgreSQL credentials.
* Run the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Backend will be available at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🖥️ Frontend Setup

Simply open `healthcare-frontend/index.html` in your browser or serve it through a simple local server:

```bash
cd healthcare-frontend
python3 -m http.server 8080
```

Frontend will be accessible at **[http://localhost:8080/](http://localhost:8080/)**

---

## 🖼️ Frontend Preview

Here’s a quick look at the frontend screens:

| Page                     | Description                          | Screenshot (Example)                                                             |
| ------------------------ | ------------------------------------ | -------------------------------------------------------------------------------- |
| `index.html`             | Landing/Login page /register page                  | ![Login Page  ](https://github.com/vyshnaviGadamsetty/healthcare-backend/blob/f810e00325c6ec2af60a4116a6429356fe0421e8/screenshots/registerration.png)               |
| `patient-dashboard.html` | Patient’s dashboard to view records  | ![Patient Dashboard](https://github.com/vyshnaviGadamsetty/healthcare-backend/blob/f810e00325c6ec2af60a4116a6429356fe0421e8/screenshots/patient-dashboard.png) |
| `admin-dashboard.html`   | Admin’s dashboard to manage patients | ![Admin Dashboard](https://github.com/vyshnaviGadamsetty/healthcare-backend/blob/f810e00325c6ec2af60a4116a6429356fe0421e8/screenshots/admin-dashboard.png)     |
| `requesting doctor`   | Patient requesting docotor by telling their symptons | ![Request Dashboard](https://github.com/vyshnaviGadamsetty/healthcare-backend/blob/f810e00325c6ec2af60a4116a6429356fe0421e8/screenshots/requesting-doctor.png)     |
| `assigning docotr`   | Assigning a doctor to a patient| ![Assign Dashboard](https://github.com/vyshnaviGadamsetty/healthcare-backend/blob/f810e00325c6ec2af60a4116a6429356fe0421e8/screenshots/assigning-doctor.png)     |


---

## 🔐 API Endpoints (Sample)

| Method | Endpoint              | Description         |
| ------ | --------------------- | ------------------- |
| POST   | `/api/auth/register/` | Register a new user |
| POST   | `/api/auth/login/`    | Login and get token |
| GET    | `/api/patients/`      | List all patients   |
| POST   | `/api/patients/`      | Add a new patient   |
| GET    | `/api/doctors/`       | List all doctors    |

*(These may vary depending on your final views and serializers.)*

---

## 🧪 Testing

Run unit tests with:

```bash
python manage.py test
```

---

## 📌 Future Improvements

* [ ] Doctor module with appointment history
* [ ] Advanced analytics dashboard
* [ ] Notifications & reminders
* [ ] Deployment using Docker / cloud

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License**.


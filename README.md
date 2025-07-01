# 🚗 Parking Management Web Application

This is a Flask-based web application for managing parking lot bookings. It provides functionality for both users and administrators, including booking, releasing, and managing parking slots.

## 🔧 Technologies Used

- **Python**  
- **Flask** (with Blueprints, Flask-SQLAlchemy, Flask-Session)  
- **SQLite**  
- **HTML, CSS, Bootstrap**  
- **Jinja2 Templating**  

---

## ▶️ How to Run the Application

1. **Clone the Repository** (or unzip the folder):
   ```bash
   git clone https://github.com/yourusername/parking-app.git
   cd parking-app
   ```

2. **Create Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Visit in Browser**:
   Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

---

## 🔑 Default Credentials

- **Admin ID:** `admin`  
- **Password:** `admin123`

New users can register on the login page.

---

## 📌 Notes

- All data is stored in `parking.db` (SQLite).
- Reservation IDs are auto-incremented.
- Admin and User routes are separated using Flask Blueprints.
- Sessions are managed using `Flask-Session`.

---

## 📽️ Demo Video

See the video walkthrough here:  
[🔗 Project Video Link](https://drive.google.com/file/d/your_video_link_here/view?usp=sharing)

---

## 📄 License

This project is submitted as part of the MAD-1 course under Online Degree Program.

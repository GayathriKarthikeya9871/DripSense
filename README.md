# 💧 DripSense -- Detecting the invisible and alerting the inevitable.
An interactive IoT-inspired water leakage monitoring and management dashboard built using **Streamlit**.  
This system simulates real-time water flow monitoring, automated leak detection, maintenance workflows, and system health analytics for residential apartments.

---

## 📌 Overview

Water leakage in residential buildings can cause structural damage, financial loss, and water wastage.  
This project demonstrates a scalable, data-driven solution for:

- 📊 Real-time water usage monitoring
- 🚨 Automated leak detection
- 🛠 Maintenance workflow tracking
- 📈 System health visualization
- 👥 Role-based dashboard access

The application is built with a clean UI and interactive analytics powered by Plotly.

---

## 🚀 Key Features

- 🏢 Block-wise apartment monitoring (A, B, C Blocks)
- 📡 Simulated real-time water flow updates
- 🔔 Intelligent leak detection alerts
- 🛠 Maintenance ticket workflow tracking
- 📜 Maintenance history logging
- 📈 Interactive charts & health gauge visualization
- 🔐 Multi-role login system (Admin / Maintenance / Resident)

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | Streamlit |
| Data Processing | Pandas |
| Visualization | Plotly |
| Architecture | Modular single-file app |

---

## 📂 Project Structure

```
Smart-Water-Leakage-Detection/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ▶️ Running the Application Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

The application will open in your browser at:

```
http://localhost:8501
```

---

## 🌍 Deployment

This application can be deployed on:

- Streamlit Community Cloud
- Render
- Railway

For Streamlit Cloud deployment:
- Ensure the repository is public
- Confirm `app.py` is the main entry file
- Include `requirements.txt`

---

## 📈 Future Improvements

- Real IoT hardware integration (ESP32 sensors)
- Database integration (PostgreSQL / MongoDB)
- Authentication using OAuth
- Cloud deployment with CI/CD pipeline
- SMS/Email alert system

---

## 👩‍💻 Author

**Yalakala Gayathri Karthikeya**  
Computer Science (Data Science) Undergraduate  
GitHub: https://github.com/YOUR_USERNAME

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

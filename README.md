Here’s the revised content with the web app link included:

---

# Fintrack – Expense Tracking Web App 🚀  

**Fintrack** is a modern web app for managing expenses efficiently. Built with FastAPI and Streamlit, it supports robust CRUD operations, insightful visualizations, and automated testing.  

🌐 **Live Demo**: [fintrack-app.streamlit.app](https://fintrack-app.streamlit.app)  

---

## 🌟 Key Features  
- **Expense Management**: Perform Create, Read, Update, and Delete (CRUD) operations seamlessly.  
- **Visual Insights**:  
  - 📊 **Pie Charts**: Visualize expense distribution by category (Plotly).  
  - 📈 **Line Charts**: Track monthly expense trends.  
  - 📋 **Tables**: Detailed tabular expense data.  
- **Reliability**:  
  - ✅ Automated CRUD testing with Pytest.  
  - 🗂️ Application logs saved to `server.log`.  

---

## 🛠️ Installation  

### 1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/yourusername/fintrack.git
cd fintrack
```  

### 2️⃣ **[Optional] Create and Activate Virtual Environment**  
- **Windows**:  
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```  
- **Mac/Linux**:  
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```  

⚡ *Skip this step if you prefer using your global Python environment.*  

### 3️⃣ **Install Dependencies**  
```bash
pip install -r requirements.txt
```  

---

## 🚀 Running the Application  

### 1️⃣ **Start the Backend**  
```bash
uvicorn backend.server:app --reload
```  

### 2️⃣ **Launch the Frontend**  
```bash
cd ./frontend
streamlit run app.py
```  

Access the app in your browser at `http://localhost:8501`.  

---

## 🧪 Testing  
Run automated tests for CRUD operations:  
```bash
pytest tests/
```  

---

## 📄 Logs  
- Logs are saved in `server.log` for tracking events and debugging.  

---

## 🛠️ Tech Stack  
- **Frontend**: Streamlit  
- **Backend**: FastAPI  
- **Visualization**: Plotly  
- **Testing**: Pytest  
- **Logging**: Python’s logging module  

---

Feel free to contribute or suggest improvements! ✨

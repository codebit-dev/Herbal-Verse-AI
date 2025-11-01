# 🌿 Herbal-Verse-AI

> **Herbal-Verse-AI** is an AI-powered virtual herbal assistant that helps users explore the world of medicinal plants, discover their benefits, and interactively learn about natural remedies.

![Demo](https://raw.githubusercontent.com/codebit-dev/Herbal-Verse-AI/refs/heads/main/banner.png)

---

## 🧠 Overview

**Herbal-Verse-AI** combines the power of Artificial Intelligence with herbal science to create an intelligent and educational experience for plant enthusiasts, students, and natural medicine lovers.

The app allows users to:
- Ask AI about herbal uses, medicinal properties, and remedies.  
- Explore a database of herbs with detailed descriptions and images.  
- Learn about preparation methods, benefits, and precautions.  
- Order herbs online from verified herbal partners *(coming soon!)*  
- Join community discussions and share herbal knowledge.  
- Enjoy an aesthetic, responsive web interface.

---

## 🧩 Key Features

✅ **AI-Powered Chat** – Ask natural questions like “Which herbs help with sleep?” or “What is Ashwagandha used for?”  
🌿 **Herb Information** – View scientific & traditional info about each herb.  
🛒 **Order Herbs Online** – Users can explore and place herbal orders from trusted sellers or local stores.  
💬 **Community Support** – Discuss remedies, share insights, and ask other users about herbal practices.  
🖼️ **Image Gallery** – Explore herbs visually using real images from Google or the dataset.  
🧭 **Interactive UI** – Simple navigation with 3D/animated visuals for an immersive experience.  
💾 **Session Memory (Optional)** – Keeps your previous chat or selected herbs.  
📚 **Extensible** – Easily add new herbs or AI models.  
⚙️ **Flask Backend** – Lightweight, secure, and easy to deploy.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML, CSS, JavaScript, Three.js (for 3D visuals) |
| **Backend** | Python Flask |
| **AI Engine** | Google Gemini API / Generative AI |
| **Database** | SQLite (local) or PostgreSQL (production) |
| **Deployment** | Render / Railway / Localhost |
| **Environment** | .env for API keys and secret configuration |

---

## 📁 Folder Structure

```
Herbal-Verse-AI/
│
├── app.py                # Main Flask app
├── static/               # CSS, JS, images, 3D assets
│   ├── css/
│   ├── js/
│   └── images/
├── templates/            # HTML frontend templates
│   ├── index.html
│   ├── chat.html
│   ├── herb_info.html
│   ├── community.html
│   └── order.html
├── .env                  # Environment variables (Gemini API key, Flask secret)
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── LICENSE               # License (MIT recommended)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/codebit-dev/Herbal-Verse-AI.git
cd Herbal-Verse-AI
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate       # For Windows
# OR
source venv/bin/activate    # For macOS/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the project root and add:

```
FLASK_SECRET_KEY=your_secret_key
GOOGLE_API_KEY=your_gemini_api_key
```

### 5️⃣ Run the Application
```bash
python app.py
```

Now visit 👉 http://127.0.0.1:5000 in your browser.

---

## 🌐 Deployment

You can easily deploy this Flask app using:

### 🔹 Railway (Recommended for Simplicity)
1. Push your repo to GitHub.  
2. Create a new Railway project.  
3. Connect your GitHub repository.  
4. Add environment variables from `.env`.  
5. Deploy — it auto-detects Flask apps!

### 🔹 Render
1. Create a new web service.  
2. Connect your repo.  
3. Set build command:
   ```bash
   pip install -r requirements.txt
   ```
4. Set start command:
   ```bash
   gunicorn app:app
   ```

---

## 🖼️ Screenshots

| Home Page | Chat Page | Herb Info |
|------------|------------|------------|
| ![Home](https://raw.githubusercontent.com/codebit-dev/Herbal-Verse-AI/refs/heads/main/1.png?auto=format\&fit=crop\&w=1350\&q=80) | ![Chat](https://raw.githubusercontent.com/codebit-dev/Herbal-Verse-AI/refs/heads/main/3.png?auto=format\&fit=crop\&w=1350\&q=80) | ![Info](https://raw.githubusercontent.com/codebit-dev/Herbal-Verse-AI/refs/heads/main/2.png?auto=format\&fit=crop\&w=1350\&q=80) |

---

## 💬 Community Support

Join our growing community of herbal enthusiasts and developers!

- 🌱 Ask questions, share remedies, or report missing herbs  
- 💡 Suggest new features or UI improvements  
- 🤝 Connect with herbal experts and contributors  

> The **Community Hub** is accessible via the “Discuss” or “Community” section in the app.

---

## 🛒 Herb Ordering (New Feature)

Users can now explore herbs and:
- View trusted sources or local stores to order from  
- Check availability, price, and health precautions  
- Place herbal orders directly through integrated platforms *(feature in beta)*  

> ⚠️ This feature currently redirects to verified herbal partners or simulated ordering endpoints.

---

## 🧪 Testing

To verify the setup locally:
```bash
pytest
```

Or test manually:
1. Search for a herb.  
2. Ask AI: “What are the benefits of Tulsi?”  
3. Explore herb details and gallery.  
4. Visit Community tab and try the ordering section.

---

## 🗺️ Roadmap

- [ ] Add voice input & speech output  
- [ ] Add login/user profiles  
- [x] Add community discussion forum  
- [x] Add herb order & delivery module  
- [ ] Add multilingual support (Hindi, Bengali, etc.)  
- [ ] Integrate 3D herb models using Three.js  
- [ ] Deploy a mobile-friendly version  

---

## 🤝 Contributing

We welcome contributions from the open-source community!

1. Fork the repository  
2. Create your feature branch  
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes  
   ```bash
   git commit -m "Add new feature"
   ```
4. Push and submit a Pull Request  

Please make sure to include clear commit messages and test your feature before PR submission.

---

## 👨‍💻 Author

**Developed by:** Team Eternals  
💡 “Plants are nature’s original medicine — Herbal-Verse-AI helps you rediscover them.”

---

## 💖 Acknowledgements

- [Google Gemini API](https://ai.google.dev) for powering AI answers  
- [Flask](https://flask.palletsprojects.com/) for backend framework  
- [Unsplash](https://unsplash.com/) for herb images  
- [Three.js](https://threejs.org/) for 3D visualization  
- All open-source contributors supporting AI + Nature projects 🌱  

---

### 🌟 Star the repo if you like this project!  
Your support helps grow **Herbal-Verse-AI** and bring natural knowledge to more people 🌿💚  

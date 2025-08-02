# 🚀 AutoblogX

**AI-powered Blog Automation Platform**

AutoblogX is a production-ready, full-stack platform that helps automate your blog workflow — from generating SEO-optimized content to publishing it across your websites with AI-generated images and videos. Built using FastAPI, Next.js, and PostgreSQL, it's designed for developers, marketers, and business owners seeking smarter content publishing.

---

<img src="https://i.ibb.co/gLdT1rp6/autoblog.png" alt="autoblog" border="0">

## ✨ Key Features

- ✍️ AI-generated blog posts with trending topic detection
- 🖼 Auto-generated images and media via generative AI
- 📹 AI-powered video generation for blog embeds and social content
- 🧠 Admin dashboard built with modern React + Tailwind CSS
- 🌐 One-click publishing to WordPress, Next.js, and other CMS
- 🗂 Supports multi-site management (e.g., mejba.me, ramlit.com, etc.)
- 🔐 Secure login/register API with JWT authentication (FastAPI)

---

## 🧱 Tech Stack

**Frontend:**
- Next.js + Tailwind CSS
- SWR / Axios for data fetching
- Secure user login/registration pages

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- Alembic for DB migrations
- JWT for auth
- PostgreSQL database

---

## 📦 Project Structure

```
autoblogx/
├── backend/
│   ├── app/
│   │   ├── api/               # FastAPI route handlers
│   │   ├── core/              # DB config, security, env setup
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Business logic
│   ├── main.py                # Entry point
│   ├── alembic/               # DB migrations
│   └── .env                   # Environment variables
├── frontend/                  # Next.js frontend
└── docker-compose.yml         # Multi-service setup
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mejba13/autoblogx.git
cd autoblogx
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Authentication

AutoblogX uses JWT-based authentication. Once you register and log in, you'll receive an `access_token` that must be included in headers like:

```http
Authorization: Bearer <your_token>
```

---

## 📮 API Endpoints

- `POST /auth/register` — Register new users
- `POST /login` — Login and receive JWT token
- `GET /posts` — Fetch blog posts (secured)
- `POST /generate` — Trigger AI blog post generation
- `POST /media/image` — Generate image from prompt
- `POST /media/video` — Generate blog-ready video

---

## 🛠 .env Example

```
DATABASE_URL=postgresql://user:password@localhost:5432/autoblogx
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🔗 Let's Connect  

- **Instagram**: [engr_mejba_ahmed](https://www.instagram.com/engr_mejba_ahmed/)  
- **TikTok**: [engr_mejba_ahmed](https://www.tiktok.com/@engr_mejba_ahmed)  
- **YouTube**: [Engr Mejba Ahmed](https://www.youtube.com/channel/UCfLIuNxRfXT7HmvvB9Ld0SA)  
- **Twitter**: [@mejba_92](https://x.com/mejba_92)  
- **LinkedIn**: [Engr Mejba Ahmed](https://www.linkedin.com/in/engr-mejba-ahmed-795ab3165/)  
- **Facebook**: [Engr Mejba Ahmed](https://www.facebook.com/engrmejbaahmed/)  
- **Reddit**: [engrmejbaahmed](https://www.reddit.com/user/engrmejbaahmed/)  
- **Pinterest**: [engrmejbaahmed](https://www.pinterest.com/engrmejbaahmed/)  
- **GitLab**: [engr-mejba-ahmed](https://gitlab.com/engr-mejba-ahmed)  
- **LeetCode**: [engrmejbaahmed](https://leetcode.com/u/engrmejbaahmed/)  
- **HackerOne**: [Engr Mejba Ahmed](https://hackerone.com/engrmejbaahmed?type=user)  
- **HackerRank**: [Dashboard](https://www.hackerrank.com/dashboard)  
- **Bugcrowd**: [EngrMejbaAhmed](https://bugcrowd.com/EngrMejbaAhmed)  
- **Medium**: [Engr Mejba Ahmed](https://medium.com/@engr-mejba-ahmed)  
- **TryHackMe**: [EngrMejbaAhmed](https://tryhackme.com/r/p/EngrMejbaAhmed)  
- **Codewars**: [mejba13](https://www.codewars.com/users/mejba13)  
- **GitHub**: [mejba13](https://github.com/mejba13)  
- **PentesterLab**: [lucid_hacker_721](https://pentesterlab.com/profile/lucid_hacker_721)  
- **DEV.to**: [Engr Mejba Ahmed](https://dev.to/engrmejbaahmed)  
- **Quora**: [Engr Mejba Ahmed](https://www.quora.com/profile/Engr-Mejba-Ahmed)
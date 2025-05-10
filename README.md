# AutoBlogX

AutoBlogX is an AI-powered content automation platform built with Django and Hugging Face APIs. It is designed to automatically generate premium-quality, SEO-optimized blog content based on trending or user-defined topics. The system also generates images and short videos using generative AI models, making it a complete end-to-end solution for bloggers, marketers, and content-driven platforms.

---

## 🚀 Features

* ✨ **AI-Generated Blog Posts**

  * Uses top-tier open-source models (like Mistral, SDXL, and ModelScope)
  * Fully SEO-optimized and human-like

* 🌍 **Trending Topic Analysis**

  * Auto-fetches current and relevant keywords/topics from the web

* 🌈 **Image Generation**

  * Automatically creates blog cover images with Stable Diffusion

* 🎥 **Video Snippets**

  * Converts text prompts into short video clips for richer multimedia blogs

* 🚪 **Secure Django Admin**

  * Password-protected admin panel with post preview and publishing options

* 🔍 **HF API Integration**

  * Easy connection with Hugging Face Inference API

---

## ⚙️ Tech Stack

* **Backend**: Django (REST Framework)
* **AI Models**: Hugging Face (Text: Mistral-7B, Image: SDXL, Video: ModelScope)
* **Database**: SQLite (development) / PostgreSQL (recommended for production)
* **Deployment Ready**: GitHub, Docker (optional), Hugging Face Inference API

---

## 📁 Project Structure

```bash
autoblogx/
├── backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services/
│   │   ├── generator.py      # Blog text generator
│   │   ├── image_gen.py      # Image generator
│   │   └── trend_fetcher.py  # Trending topic retriever
├── templates/
├── static/
├── media/
├── .env
├── manage.py
└── README.md
```

---

## 🔧 Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/mejba13/autoblogx.git
cd autoblogx

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Add your Hugging Face token and model URL to .env
HF_TOKEN=your_hf_token
API_URL=https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2

# 5. Run server
python manage.py runserver
```

---

## ✅ Roadmap

* [x] Text generation from prompt
* [x] Auto image creation
* [x] Hugging Face API integration
* [ ] Schedule-based publishing
* [ ] WordPress auto-push integration
* [ ] Multilingual content support

---

## 👨‍💻 About the Author

**Engr Mejba Ahmed** is a full-stack engineer passionate about automation, AI, and cybersecurity. With over a decade of experience, he builds smart tools that blend machine learning, APIs, and human-centric design.

---

## 🔗 Let's Connect

* **Portfolio**: [GitHub Profile](https://github.com/mejba13)
* **Instagram**: [engr\_mejba\_ahmed](https://www.instagram.com/engr_mejba_ahmed/)
* **TikTok**: [engr\_mejba\_ahmed](https://www.tiktok.com/@engr_mejba_ahmed)
* **YouTube**: [Engr Mejba Ahmed](https://www.youtube.com/channel/UCfLIuNxRfXT7HmvvB9Ld0SA)
* **Twitter**: [@mejba\_92](https://x.com/mejba_92)
* **LinkedIn**: [Engr Mejba Ahmed](https://www.linkedin.com/in/engr-mejba-ahmed-795ab3165/)
* **Facebook**: [Engr Mejba Ahmed](https://www.facebook.com/engrmejbaahmed/)
* **Reddit**: [engrmejbaahmed](https://www.reddit.com/user/engrmejbaahmed/)
* **Pinterest**: [engrmejbaahmed](https://www.pinterest.com/engrmejbaahmed/)
* **GitLab**: [engr-mejba-ahmed](https://gitlab.com/engr-mejba-ahmed)
* **LeetCode**: [engrmejbaahmed](https://leetcode.com/u/engrmejbaahmed/)
* **HackerOne**: [Engr Mejba Ahmed](https://hackerone.com/engrmejbaahmed?type=user)
* **HackerRank**: [Dashboard](https://www.hackerrank.com/dashboard)
* **Bugcrowd**: [EngrMejbaAhmed](https://bugcrowd.com/EngrMejbaAhmed)
* **Medium**: [Engr Mejba Ahmed](https://medium.com/@engr-mejba-ahmed)
* **TryHackMe**: [EngrMejbaAhmed](https://tryhackme.com/r/p/EngrMejbaAhmed)
* **Codewars**: [mejba13](https://www.codewars.com/users/mejba13)
* **PentesterLab**: [lucid\_hacker\_721](https://pentesterlab.com/profile/lucid_hacker_721)
* **DEV.to**: [Engr Mejba Ahmed](https://dev.to/engrmejbaahmed)
* **Quora**: [Engr Mejba Ahmed](https://www.quora.com/profile/Engr-Mejba-Ahmed)

---

> ✨ Contributions, stars, and forks are always welcome. Let’s build smarter content automation together!

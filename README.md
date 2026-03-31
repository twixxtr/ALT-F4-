# ALT+F4: AI-Powered Cybersecurity Intelligence Platform

ALT+F4 is a production-grade, multi-dimensional cybersecurity suite designed to protect users from modern digital threats. Powered by Gemini AI, it provides intelligent detection, deep analysis, and actionable insights across phishing, system logs, and digital media.

## 🚀 Key Features

### 🛡️ 1. Multi-Pillar Security Analysis
- **Phishing Detector:** Advanced analysis of messages, emails, and URLs to detect scams using behavioral patterns rather than just blacklists. Supports screenshot analysis for visual phishing detection.
- **Log Analyzer:** Detects anomalies, unauthorized access patterns, and potential system breaches within raw server or application logs.
- **Media Authenticity Checker:** Analyzes images for signs of AI generation, manipulation, or deepfakes to ensure digital trust.

### 🌐 2. Inclusive & Global AI
- **Multi-Language Support:** Native support for **English**, **Hindi (हिंदी)**, and **Malayalam (മലയാളം)**.
- **Auto-Detect Technology:** The system automatically identifies the input language and provides the entire analysis (findings, advice, and impact) in that specific language.

### 📊 3. Unified Intelligence Dashboard
- **Global Risk Index:** A real-time, dynamic gauge that calculates an aggregate security posture based on all recent scanning activity.
- **Activity Timeline:** A chronologically tracked alert center that logs all security events with severity-coded indicators.
- **Live Performance Metrics:** Tracks total scans, threats mitigated, and the most frequent attack vectors.

### 🧠 4. Cognitive Accessibility Features
- **"Explain Simply" Mode:** Transforms technical security findings into jargon-free, easy-to-understand explanations for non-technical users.
- **Trusted vs Suspicious Comparison:** Generates a side-by-side comparison of the suspicious input against what a "Trusted" version would look like, educating the user on the specific red flags.
- **Impact Prediction:** AI-driven forecasting of what could happen if a threat is ignored, helping users understand the stakes.

### ⚡ 5. Actionable UX
- **Quick Action Buttons:** Immediate resolution options like "Block Sender", "Report Scam", and "Mark as Unsafe" to streamline the response workflow.
- **Premium Interface:** A glassmorphic, responsive design with smooth transitions and real-time UI feedback.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3 (Modern Glassmorphism), Vanilla JavaScript
- **Backend:** Python (Flask)
- **AI Engine:** Google Gemini AI (Generative AI SDK)
- **Styling:** Custom CSS with FontAwesome & Google Fonts (Poppins)

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd creative-website-landing-page-with-illustrated-shapes
   ```

2. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Install Dependencies:**
   ```bash
   pip install flask flask-cors google-generativeai python-dotenv
   ```

4. **Run the Backend:**
   ```bash
   python app.py
   ```

5. **Run the Frontend:**
   You can use a simple HTTP server to serve the `index.html`:
   ```bash
   python -m http.server 8000
   ```
   Access the app at `http://localhost:8000`.

---

## 🛡️ Security & Privacy
ALT+F4 is designed as a demonstration platform for AI-powered security intelligence. All analyses are processed in real-time. For production environments, ensure appropriate data handling and API rate limiting is implemented.

---
*Developed for the AI Cybersecurity Hackathon.*

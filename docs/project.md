# Maguru - AI Coding Learning Platform

> **Vision**: Platform edtech berbasis AI yang membantu siswa Indonesia belajar coding dengan pendekatan interaktif, personal, dan adaptif.

---

## 📋 Project Overview

### Konsep Singkat
Maguru adalah platform pembelajaran coding berbasis AI di mana siswa belajar melalui alur interaktif: **Teori → Praktik dengan AI Chatbot → Kuis → Prasyarat Review (jika gagal)**.

### Target User
- Siswa dengan **basic knowledge** (tidak absolute beginner)
- Fokus bahasa: **Python**
- Belajar mandiri dengan AI sebagai co-teacher

### Tech Stack MVP
| Component | Technology | Rationale |
|-----------|------------|-----------|
| **UI Framework** | Streamlit | Rapid prototyping, Python-native, sufficient for MVP |
| **AI Framework** | LangChain (LCEL + LangGraph) | Industry standard for AI applications, flexible chain composition |
| **LLM** | GPT-3.5-turbo | Cost efficiency while maintaining quality |
| **Auth** | Anonymous (no login) | Reduce friction for MVP, focus on learning experience |
| **Data Storage** | Streamlit Session State | In-memory storage sufficient for anonymous sessions |

---

## 🎯 Core Features (MVP) - Detailed Descriptions

### 1. Interactive Learning Flow

#### Purpose
Menciptakan pengalaman belajar yang natural dan engaging seperti belajar dengan tutor manusia, di mana siswa bisa berinteraksi, bertanya, dan mendapatkan feedback secara real-time.

#### Functionality Detail

**Course Selection Phase**
- Siswa melihat daftar course yang tersedia dengan deskripsi singkat
- Setiap course menampilkan informasi: difficulty level, estimated duration, learning objectives
- Siswa dapat memilih course sesuai dengan minat dan tingkat kemampuannya

**AI Greeting & Orientation**
- Setelah memilih course, AI menyapa siswa secara personal menggunakan nama yang diinput
- AI menjelaskan apa yang akan dipelajari dalam course ini dengan bahasa yang mudah dipahami
- AI menanyakan kesiapan siswa dan memastikan tidak ada pertanyaan sebelum memulai
- Contoh sapaan: "Halo Budi! Terima kasih telah memilih kelas Python Basics. Kita akan mempelajari konsep dasar pemrograman Python mulai dari variables, data types, hingga control flow. Apakah kamu siap untuk memulai perjalanan belajar ini?"

**Theory Content Delivery**
- Materi disajikan dalam format yang terstruktur: concept explanation, examples, dan practice tasks
- Setiap session dirancang untuk dapat diselesaikan dalam 15-20 menit
- Materi menggunakan bahasa Indonesia dengan analogi yang relevan untuk siswa Indonesia
- Visual aids seperti diagram, ilustrasi, atau code snippets untuk memperjelas konsep

**Interactive Chatbot Q&A**
- Chatbot tersedia selama sesi belajar untuk menjawab pertanyaan siswa
- Siswa dapat meminta penjelasan tambahan, contoh lain, atau clarification pada bagian yang membingungkan
- Chatbot juga dapat mengajukan checkpoint questions untuk memastikan pemahaman siswa
- Konteks percakapan di-maintain sepanjang session untuk memberikan pengalaman yang natural

**Practice & Quiz Session**
- Setelah mempelajari materi, siswa diberikan kuis untuk menguji pemahaman
- Kuis terdiri dari multiple choice questions dan code completion exercises
- Siswa menerima immediate feedback untuk setiap jawaban
- AI menjelaskan mengapa jawaban benar atau salah dengan penjelasan yang mendidik

#### User Value
- Siswa merasa didampingi selama proses belajar, tidak hanya consuming konten pasif
- Dapat memperoleh clarification instantly tanpa menunggu tutor
- Build confidence melalui progressive assessment dengan feedback yang membangun

---

### 2. AI Capabilities

#### 2.1 Code Explanation

**Purpose**
Membantu siswa memahami cara kerja kode secara mendalam, bukan hanya menghafal syntax.

**Functionality**
- AI menerima snippet kode sebagai input dari siswa
- AI menjelaskan setiap baris atau blok kode dengan bahasa yang sederhana
- Penjelasan mencakup: apa yang dilakukan kode, mengapa ditulis cara itu, dan apa dampaknya
- AI memberikan analogi real-world untuk mempermudah pemahaman konsep abstrak
- AI menunjukkan common mistakes yang sering terjadi pada konsep tersebut

**Interaction Flow**
- Siswa dapat paste code dan meminta penjelasan lengkap
- Siswa dapat menanyakan bagian spesifik dari kode ("jelaskan baris 3-5")
- Siswa dapat meminta penjelasan "seperti saya umur 5 tahun" untuk konsep yang sulit

**Example Scenario**
Siswa bertanya: "Kenapa di Python tidak pakai titik koma?"
AI menjelaskan dengan perbandingan bahasa lain, konsep readability in Python, dan best practices.

#### 2.2 Hint Generation System (3-Level Progressive Hints)

**Purpose**
Membantu siswa yang stuck pada practice task atau coding challenge tanpa langsung memberikan jawaban, sehingga tetap ada learning process.

**Functionality**

**Level 1 - Gentle Hint**
- Memberikan petunjuk subtan yang mengarah ke solusi tanpa membocorkan jawaban
- Fokus pada reminding konsep yang relevan atau pointing ke arah yang benar
- Contoh: "Coba pikirkan, tipe data apa yang cocok untuk menyimpan teks?"

**Level 2 - Conceptual Hint**
- Menjelaskan konsep yang mungkin belum dipahami siswa
- Memberikan contoh yang mirip tapi tidak identik dengan problem
- Contoh: "Di Python, string digunakan untuk teks. Untuk membuat string, kamu bisa menggunakan tanda kutip. Coba lihat contoh di materi tadi."

**Level 3 - Direct Hint**
- Hampir memberikan solusi tapi tetap memerlukan sedikit thinking dari siswa
- Menunjukkan approach yang benar dengan missing pieces
- Contoh: "Untuk membuat variabel city dengan nilai 'Jakarta', tulis: city = 'Jakarta'. Coba terapkan pola yang sama untuk soal kamu."

**Interaction Design**
- Siswa dapat meminta hint kapan saja saat stuck
- Sistem mendorong siswa mencoba sendiri dulu sebelum meminta hint
- Ada cooldown atau limit untuk mencegah over-reliance pada hints
- AI mengingat hint level yang sudah diberikan dalam session yang sama

#### 2.3 Quiz Feedback System

**Purpose**
Memberikan pembelajaran dari kuis, bukan hanya penilaian. Setiap jawaban, benar atau salah, menjadi momen belajar.

**Functionality**

**For Correct Answers**
- Celebrate achievement dengan positive reinforcement
- Explain WHY the answer is correct untuk reinforce understanding
- Connect ke konsep lain yang related untuk extended learning
- Contoh: "Benar! Variabel di Python memang dibuat dengan assignment statement. Ini berbeda dengan beberapa bahasa lain yang butuh keyword seperti 'var' atau 'let'."

**For Incorrect Answers**
- Gently correct tanpa making siswa feel bad
- Explain the misconception yang mungkin terjadi
- Show correct answer dengan penjelasan langkah demi langkah
- Offer untuk review kembali materi terkait
- Contoh: "Hampir tepat! Jawaban yang benar adalah 'name = value'. Di Python kita tidak butuh keyword 'var' seperti di JavaScript. Variabel langsung dibuat dengan assignment."

**Learning Analytics**
- Track patterns untuk mengidentifikasi areas where siswa consistently struggles
- Gunakan data ini untuk personalized recommendations

#### 2.4 Adaptive Learning Flow

**Purpose**
Menyesuaikan learning path berdasarkan performance siswa, memastikan gap knowledge di-address sebelum lanjut ke materi yang lebih advanced.

**Functionality**

**Performance Assessment**
- Setelah kuis, sistem menganalisis jawaban siswa untuk identify weak areas
- Sistem memetakan concepts yang belum dikuasai berdasarkan patterns dalam incorrect answers

**Prerequisite Recommendation**
- Jika score < 70%, sistem mengidentifikasi prerequisite topics yang perlu di-review
- Sistem menampilkan rekomendasi dengan penjelasan mengapa review ini penting
- Contoh: "Berdasarkan hasil kuis, kamu masih kesulitan dengan konsep variable assignment. Disarankan untuk review Session 1.1 tentang Variables sebelum lanjut."

**Review Mode**
- Siswa dapat memilih untuk langsung ke review session atau mencoba kuis lagi
- Review session menyajikan ulang materi dengan approach yang berbeda (more examples, different explanations)
- Setelah review, mini-quiz diberikan untuk verify understanding
- Progress hanya dilanjutkan setelah siswa demonstrates mastery

**Retry Mechanism**
- Unlimited retry attempts untuk kuis
- Setiap retry menawarkan question variations untuk prevent memorization
- Sistem tracks improvement across attempts

#### 2.5 Q&A Chatbot

**Purpose**
Menjadi learning companion yang selalu tersedia untuk menjawab pertanyaan siswa kapan saja selama session.

**Functionality**

**Context-Aware Responses**
- Chatbot memiliki context tentang materi yang sedang dipelajari siswa
- Responses are tailored to current session dan learning progress
- Chatbot dapat reference specific examples atau explanations dari materi

**Multi-Turn Conversations**
- Chatbot maintains conversation history untuk natural dialogue flow
- Dapat handle follow-up questions dan clarifications
- Remembers previous questions dari siswa dalam session yang sama

**Knowledge Scope**
- Jawab pertanyaan tentang materi yang sedang dipelajari
- Jelaskan konsep Python terkait session topics
- Berikan additional examples untuk practice
- Redirect jika pertanyaan di luar scope (tapi tetap helpful)

**Personality & Tone**
- Friendly, encouraging, dan patient
- Using Indonesian language dengan natural expressions
- Age-appropriate language untuk target audience
- Celebrate progress dan provide support during struggles

---

### 3. Assessment System

#### Purpose
Mengukur pemahaman siswa secara objektif dan memberikan feedback yang actionable untuk improvement.

#### Quiz Format

**Multiple Choice Questions**
- Test conceptual understanding dengan distractors yang didesain untuk reveal common misconceptions
- Setiap opsi jawaban memiliki explanation untuk mengapa benar/salah
- Questions progress dari basic recall ke application dan analysis

**Code Completion Exercises**
- Present incomplete code snippet dengan missing parts
- Siswa harus fill in the blank dengan correct syntax or logic
- Test practical understanding of syntax dan problem-solving
- Multiple possible approaches dapat di-accept untuk flexibility

**Scoring System**
- Setiap question memiliki point value berdasarkan difficulty
- Passing threshold: 70% untuk ensure adequate understanding
- Score displayed dengan breakdown by topic untuk identify strengths dan weaknesses

#### Feedback Mechanism

**Immediate Feedback**
- Setiap jawaban langsung dinilai setelah submission
- Detailed explanation diberikan untuk setiap question
- Siswa dapat review answers sebelum final submission

**Performance Summary**
- Overall score dengan pass/fail indication
- Topic breakdown showing areas of strength dan weakness
- Comparison dengan previous attempts (if applicable)
- Personalized next steps based pada performance

#### Progress Tracking

**Visual Indicators**
- Progress bar menunjukkan completion percentage dari course
- Checklist style display untuk completed sessions
- Badge atau milestone indicators untuk achievements
- Color coding untuk status (completed, in-progress, locked)

**Session State Persistence**
- Progress disimpan dalam session state untuk anonymous users
- Completed sessions tetap tracked selama browser session aktif
- Quiz history disimpan untuk review dan improvement tracking

---

## 📐 Content Structure

### Hierarchy Design

**Course Level**
- Top-level container untuk entire subject matter
- Contoh: "Python Basics" mencakup everything dari hello world sampai basic data structures

**Module Level**
- Grouping of related topics yang membentuk coherent learning unit
- Setiap module berfokus pada specific theme atau skill set
- Contoh: "Variables & Data Types", "Control Flow", "Functions"

**Session Level**
- Individual learning units yang dapat diselesaikan dalam satu sitting
- Setiap session memiliki learning objectives yang spesifik
- Combination of: theory content, examples, practice tasks, dan quiz assessment

**Quiz Level**
- Assessment points biasanya di akhir setiap module
- Comprehensive evaluation dari semua sessions dalam module
- Determines readiness untuk lanjut ke module berikutnya

### Content Organization Principles

**Progressive Complexity**
- Setiap session builds upon knowledge dari previous sessions
- Prerequisite relationships clearly defined
- Sistem enforce completion order untuk ensure learning path integrity

**Micro-Learning Approach**
- Content broken down menjadi bite-sized chunks
- Setiap session fokus pada 1-2 core concepts
- Prevent cognitive overload dan enable better retention

**Scaffolding Design**
- Early sessions provide more guidance dan structure
- Later sessions gradually reduce support untuk build independence
- Practice tasks evolve dari guided ke open-ended

---

## 🏗️ System Architecture

### User Journey Overview

**Entry Point**
Siswa masuk ke platform dan langsung melihat available courses dengan clear value propositions.

**Selection & Orientation**
Setelah memilih course, AI menginisiasi conversation untuk establish context dan build rapport.

**Learning Loop**
Theory → Practice → Check Understanding → Quiz → Pass/Fail Decision

**Progression**
Successful completion unlocks next content. Failure triggers adaptive review flow.

**Completion**
Final assessment dan recognition of achievement.

### Application Layer Architecture

**Streamlit UI Layer**
- Renders interface elements yang user interacts with
- Manages user input dan display outputs
- Provides navigation antar different pages/views

**Session State Layer**
- Maintains user progress data throughout session
- Stores chat history untuk context-aware conversations
- Tracks completed sessions dan quiz scores
- No external database required untuk MVP

**LangChain AI Layer**
- Orchestrates AI interactions menggunakan chains dan graphs
- Manages prompts, model calls, dan response processing
- Implements different AI behaviors untuk different use cases

**Data Layer**
- Static course content dalam YAML dan Markdown formats
- Quiz definitions dengan structured data
- Configuration files untuk system behavior

---

## 🤖 AI Behavior & Interactions

### AI Personality Design

**Characteristics**
- Friendly dan approachable, like a supportive tutor
- Professional yet casual tone untuk reduce intimidation
- Patient dengan repeated questions atau confusion
- Encouraging dan celebrates small wins
- Culturally appropriate untuk Indonesian students

**Communication Style**
- Uses natural Indonesian expressions, not stilted translations
- Incorporates relevant analogies dari Indonesian context
- Balances simplicity dengan technical accuracy
- Adapts complexity level based pada student responses

### Interaction Patterns

**Proactive Engagement**
- AI initiates checkpoint questions untuk verify understanding
- AI offers hints ketika detect prolonged inactivity
- AI suggests review topics based pada quiz performance

**Responsive Support**
- AI answers questions dengan relevant context dari current session
- AI provides additional examples when requested
- AI adapts explanations based pada follow-up questions

**Adaptive Difficulty**
- AI gauges student level dari responses dan adjusts complexity
- AI provides simpler explanations jika detect confusion
- AI introduces advanced concepts untuk students yang ready

---

## 📊 Prerequisite Review System

### Trigger Conditions

**Automatic Activation**
- Review mode triggers ketika quiz score falls below 70%
- System identifies specific concepts yang tidak dikuasai berdasarkan question analysis

**User-Initiated**
- Siswa dapat request review even setelah passing (untuk reinforcement)
- Siswa dapat memilih specific topics untuk review bukan full module

### Review Flow

**Assessment Phase**
- System analyzes quiz results untuk identify knowledge gaps
- Maps incorrect answers kepada specific concepts atau sessions
- Generates personalized review plan

**Recommendation Presentation**
- Clear explanation mengapa review diperlukan
- Specific topics identified untuk review dengan rationale
- Estimated time untuk review completion

**Review Execution**
- Targeted content delivery untuk identified weak areas
- Different approach dari original presentation (new examples, alternative explanations)
- Interactive check-ins selama review untuk verify understanding

**Verification**
- Mini-quiz setelah review completion untuk assess improvement
- Passing mini-quiz unlocks original quiz retry
- Continued failure loops back ke additional review resources

---

## 🎨 User Experience Design

### Visual Design Principles

**Clarity & Simplicity**
- Clean, distraction-free interface untuk focus pada learning
- Clear visual hierarchy untuk guide attention
- Consistent design patterns untuk predictability

**Progress Indication**
- Always-visible progress tracking untuk motivation
- Clear indication dari current position dalam learning path
- Visual celebration untuk milestones dan achievements

**Accessibility**
- High contrast text untuk readability
- Clear typography dengan appropriate sizing
- Responsive design untuk various screen sizes

### Interaction Design

**Low Friction**
- Minimal clicks atau steps untuk access learning content
- Quick loading times untuk maintain engagement
- Intuitive navigation tanpa extensive learning curve

**Feedback Rich**
- Immediate response untuk semua user actions
- Clear confirmation untuk submissions dan completions
- Helpful error messages yang guide resolution

**Engagement Maintaining**
- Varied interaction types (reading, typing, selecting) untuk maintain interest
- Achievements dan milestones untuk motivation
- Personalized elements (name usage, progress tracking) untuk connection

---

## 💾 Data Persistence Strategy

### Session-Based Storage

**What Gets Stored**
- Current course, module, dan session progress
- Quiz scores dan history dari attempts
- Chat history dalam current session untuk context maintenance
- User preferences atau settings jika applicable

**What Doesn't Get Stored**
- Cross-session data (anonymous users start fresh each browser session)
- Long-term analytics atau user profiles
- Sensitive personal information

**Storage Mechanism**
- Streamlit session state objects
- In-memory storage tied kepada browser session
- Automatic cleanup ketika session ends

---

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Week 1)
**Goal**: Basic structure dengan static content delivery

**Deliverables**
- Functional Streamlit app dengan multi-page navigation
- Course content structure dalam YAML/Markdown
- Basic session state management
- Content loading dan rendering system
- Static theory content display

### Phase 2: Core AI Features (Week 1-2)
**Goal**: Interactive learning dengan basic AI capabilities

**Deliverables**
- LCEL chain implementation untuk code explanation
- Basic chatbot UI dengan message history
- Quiz system dengan validation dan scoring
- Simple feedback mechanism
- Progress tracking visualization

### Phase 3: Advanced AI Features (Week 2)
**Goal**: Adaptive learning dengan intelligent tutoring

**Deliverables**
- Hint generation system dengan 3-level progressive hints
- Quiz feedback chain dengan detailed explanations
- LangGraph implementation untuk adaptive learning flow
- Prerequisite review logic dan recommendation system
- Context-aware chatbot dengan session memory

### Phase 4: Polish & Optimization (Week 2-3)
**Goal**: Production-ready MVP dengan quality user experience

**Deliverables**
- Comprehensive error handling
- UI/UX improvements berdasarkan usability testing
- Performance optimization untuk faster AI responses
- Edge case handling untuk robust system behavior
- Documentation untuk deployment dan maintenance

---

## 📁 Project Structure

**Root Directory**
- `app.py` - Main Streamlit application entry point
- `requirements.txt` - Python dependencies list
- `.env` - Environment variables untuk API keys dan config

**Data Directory**
- Course content dalam structured YAML dan Markdown files
- Quiz definitions dengan standardized format
- Static assets seperti images atau diagrams jika needed

**LangChain Directory**
- Chain definitions untuk different AI behaviors
- Graph implementations untuk complex flows
- Prompt templates untuk consistent AI interactions

**UI Directory**
- Page components untuk different views
- Reusable UI components seperti chatbot, progress bars
- Styling dan layout configurations

**Utils Directory**
- Session management utilities
- Content loading dan parsing functions
- Quiz validation dan scoring logic
- Helper functions untuk common operations

---

## 🔧 Technical Dependencies

**Core Framework**
- Streamlit untuk web application interface
- LangChain sebagai AI orchestration framework
- LangGraph untuk complex multi-step AI flows

**LLM Integration**
- LangChain OpenAI integration untuk model access
- OpenAI API (GPT-3.5-turbo) untuk language model

**Data Processing**
- PyYAML untuk content file parsing
- Python standard library untuk basic operations

**Configuration**
- python-dotenv untuk environment variable management
- Standard configuration files untuk system settings

---

## 🎯 Success Metrics (MVP)

**Engagement Metrics**
- Session completion rate - persentase siswa yang menyelesaikan minimal satu full session
- Average session duration - ideal range 15-20 menit per session
- Chat interaction frequency - jumlah pertanyaan per session (target 2-5)

**Learning Effectiveness**
- Quiz pass rate improvement - perbandingan pass rate antara first attempt dan after review
- Retention rate - siswa yang kembali untuk sesi berikutnya dalam course
- Time to mastery - rata-rata attempts needed untuk passing each quiz

**User Experience**
- AI response time - target <5 detik untuk chatbot responses
- Navigation efficiency - clicks atau steps needed untuk access learning content
- Error rate - technical errors atau bugs encountered per session

**Quality Indicators**
- Content clarity - user feedback pada explanation quality
- Helpfulness of AI - perceived value dari AI interactions
- Overall satisfaction - net promoter score atau similar metric

---

## 🔮 Future Enhancements (Post-MVP)

**Platform Expansion**
- User authentication dengan persistent profiles
- Multiple programming language tracks (JavaScript, Go, Rust)
- Mobile applications untuk on-the-go learning
- Offline mode capability dengan content synchronization

**Learning Features**
- Live code editor dengan real execution environment
- Collaborative projects dan peer learning features
- Gamification dengan achievements, leaderboards, dan rewards
- Spaced repetition system untuk long-term retention

**Content & Curriculum**
- Advanced course offerings (web development, data science, ML)
- Industry projects dan real-world case studies
- Integration dengan external learning resources
- Community-contributed content dengan quality moderation

**Analytics & Insights**
- Detailed learning analytics dashboard
- Parent atau teacher reporting interfaces
- AI-driven learning path optimization
- Performance benchmarking against peers

**Monetization Strategies**
- Premium subscription tier dengan advanced features
- Institutional licensing untuk schools dan bootcamps
- Corporate training programs
- Certification programs dengan industry recognition

---

**Document Version**: 2.0
**Last Updated**: 2025-02-10
**Status**: Ready for Implementation
**Focus**: Detailed Feature Descriptions (No Pseudocode)

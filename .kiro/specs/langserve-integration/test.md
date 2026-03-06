# LangServe Integration - Manual Testing Checklist

**Version**: 1.1 (Updated for Tasks 6-11)
**Date**: ___________
**Tester**: ___________
**Environment**: Local Development

---

## Prerequisites

- [x] Backend running on `http://localhost:8000`
- [x] Frontend running on `http://localhost:3000`
- [x] User logged in to the application

---

## 1. Backend Health Check

- [x] Open `http://localhost:8000/health` in browser
- [x] Response shows: `{"status":"ok","service":"Maguru AI API","version":"1.0.0"}`

---

## 2. Chatbot FAB Visibility

- [x] Open any course Learn page (e.g., `/course/python-basics/learn`)
- [x] FAB (circular chat icon) visible in **bottom-right corner**
- [x] FAB has **amber/orange gradient** color
- [x] FAB shows **pulse animation** when closed

---

## 3. Chatbot Panel - Open/Close

- [x] Click FAB → Panel **slides in from right**
- [x] FAB icon changes to **X** when panel is open
- [x] Panel has **fixed width ~400px** on desktop
- [x] Click **X button** in header → Panel closes
- [x] Click FAB again → Panel re-opens

---

## 4. Chatbot UI Elements

- [x] Header shows **"AI Tutor"** title
- [x] Header shows **Course name** and **Topic name**
- [x] **Empty state** shows: "Your AI Learning Assistant"
- [x] **Quick prompts** visible: "Explain this topic simply", "Give me examples", "Quiz me on this"

---

## 5. Send Message & Streaming

- [x] Type question in input field
- [x] Click **Send button** (or press Enter)
- [x] User message appears immediately in chat
- [x] **AI response streams in** (text appears gradually)
- [x] **Streaming indicator** (3 bouncing dots) shows while AI responds
- [x] Input field is **disabled** during streaming

---

## 6. AI Message Display

- [x] AI message has **gradient avatar** (amber/orange)
- [x] AI message supports **markdown formatting** (bold, lists, etc.)
- [x] AI message supports **code blocks** with syntax highlighting
- [x] AI message shows **timestamp**

---

## 7. Mobile Responsive

- [x] Open on **mobile viewport** (< 768px)
- [x] FAB still visible in bottom-right
- [x] Chatbot panel opens **full-screen** on mobile
- [x] **Overlay background** appears when panel is open
- [x] Click outside panel → Panel closes

---

## 8. Error Handling

- [x] Stop the LangServe backend (Ctrl+C in terminal)
- [x] Try sending a message in chatbot
- [x] **Error message** appears: "Failed to get response" or similar
- [x] Restart backend and try again → Works normally

---

## 9. Clear Messages

- [x] Send multiple messages
- [x] Click **Trash icon** in header
- [x] All messages are cleared
- [x] Empty state appears again

---

## 11. Chat History Persistence

- [ ] Send first message: "What is a variable?"
- [ ] AI responds
- [ ] Send follow-up: "Can you give an example?"
- [ ] AI responds with **context from previous message**
- [ ] Verify chat shows **both messages**
- [ ] Close chatbot (click X)
- [ ] Re-open chatbot
- [ ] **Chat history is preserved** (all messages still visible)

---

## 12. AI Chain Endpoints (via API or UI)

### 12.1 Code Explanation
- [ ] Open browser DevTools → Network tab
- [ ] Send code snippet question: "Explain this code: `x = 5 + 3`"
- [ ] Verify `/explain-code/stream` endpoint called
- [ ] Response includes code explanation

### 12.2 Hint Generator
- [ ] Ask for hint: "Give me a hint about variables"
- [ ] Verify `/hint/stream` endpoint called (if integrated)
- [ ] Response includes progressive hint

### 12.3 Quiz Feedback
- [ ] Answer a quiz question incorrectly
- [ ] Verify `/quiz-feedback/stream` endpoint called (if integrated)
- [ ] Response includes constructive feedback

### 12.4 Greeting Generation
- [ ] Start new chat session
- [ ] Verify AI greeting appears (if integrated)
- [ ] Greeting is personalized

---

## 13. Accessibility Testing

### 13.1 Keyboard Navigation
- [ ] Press **Tab** repeatedly → Focus moves to FAB
- [ ] Press **Enter/Space** on FAB → Chatbot opens
- [ ] Press **Tab** → Focus moves to input field
- [ ] Type message → Press **Enter** → Message sends
- [ ] Press **Escape** → Chatbot closes

### 13.2 Focus Management
- [ ] Open chatbot → Focus in input field
- [ ] Press **Tab** → Focus cycles through interactive elements
- [ ] Focus stays **within chatbot panel** while open
- [ ] Close chatbot → Focus returns to FAB

### 13.3 Screen Reader
- [ ] Enable screen reader (NVDA/VoiceOver)
- [ ] Tab to FAB → Hear "Open AI Tutor, button"
- [ ] Open chatbot → Hear "AI Tutor, dialog"
- [ ] New message arrives → Hear announcement
- [ ] All buttons have descriptive labels

---

## 14. Tablet Responsive (768px)

- [ ] Open DevTools → Toggle device toolbar
- [ ] Set viewport to **768x1024** (iPad)
- [ ] FAB visible in bottom-right
- [ ] Chatbot panel opens (not full-screen)
- [ ** Panel width scales appropriately (~350px)
- [ ] All UI elements remain clickable

---

## 15. Chat History Limit (Token Optimization)

- [ ] Send **15+ messages** in conversation
- [ ] Open DevTools → Network tab
- [ ] Check last request payload
- [ ] Verify `chat_history` contains **only last 10 messages**
- [ ] Response is still fast (not slowed by huge history)

---

## 16. Content Truncation (Token Optimization)

- [ ] Navigate to lesson with **long content** (>1000 chars)
- [ ] Open DevTools → Network tab
- [ ] Send chatbot question
- [ ] Check request payload
- [ ] Verify `session_content` is **truncated to ~1000 chars**
- [ ] Response ends with `...` if truncated

---

## Test Results

**Total Tests**: 16 sections / ~65 checkpoints
**Passed**: _____
**Failed**: _____
**Notes**: ___________________________________________________________________

---

## Issues Found

| # | Description | Severity | Status |
|---|-------------|----------|--------|
| 1 | | | |
| 2 | | | |

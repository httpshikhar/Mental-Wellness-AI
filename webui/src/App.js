import React, { useState } from 'react';
import Typing from 'react-typing-effect';
import { Audio } from 'react-loader-spinner';
import { motion } from 'framer-motion';
import { speakText } from './speak'; // ✅ Importing from speak.js

const App = () => {
  const [userMessage, setUserMessage] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);

  const sendMessage = async () => {
    if (!userMessage.trim()) return;

    try {
      const res = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 'user123',
          message: userMessage,
        }),
      });

      const data = await res.json();
      const reply = data.response;
      setAiResponse(reply);
      setUserMessage('');

      // 🗣️ Speak the text
      setIsSpeaking(true);
      await speakText(reply);
      setIsSpeaking(false);

    } catch (err) {
      console.error('Error:', err);
      setIsSpeaking(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>🧠 AI Mental Wellness Chatbot</h1>

      <div style={styles.chatBox}>
        {aiResponse && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            style={styles.aiBubble}
          >
            <Typing text={aiResponse} speed={50} eraseDelay={999999} />
            {isSpeaking && (
              <div style={{ marginTop: 10 }}>
                <Audio height="30" width="30" color="#4fa94d" ariaLabel="audio-loading" visible={true} />
              </div>
            )}
          </motion.div>
        )}
      </div>

      <div style={styles.inputContainer}>
        <input
          type="text"
          placeholder="Talk to your AI buddy..."
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)}
          style={styles.input}
        />
        <button onClick={sendMessage} style={styles.sendBtn}>Send</button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '40px',
    fontFamily: 'Segoe UI, sans-serif',
    maxWidth: '600px',
    margin: 'auto',
    textAlign: 'center',
  },
  chatBox: {
    minHeight: '100px',
    marginBottom: '20px',
    marginTop: '20px',
  },
  aiBubble: {
    background: '#f0f4ff',
    padding: '12px 16px',
    borderRadius: '16px',
    display: 'inline-block',
    maxWidth: '90%',
  },
  inputContainer: {
    display: 'flex',
    gap: '10px',
    justifyContent: 'center',
  },
  input: {
    padding: '10px',
    width: '60%',
    borderRadius: '8px',
    border: '1px solid #ccc',
  },
  sendBtn: {
    padding: '10px 16px',
    background: '#4fa94d',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
  },
};

export default App;

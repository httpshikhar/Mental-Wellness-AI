import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet, ActivityIndicator, Alert
} from 'react-native';
import * as FileSystem from 'expo-file-system';
import { Audio } from 'expo-av';
import axios from 'axios';
import { Buffer } from 'buffer';

global.Buffer = Buffer;

export default function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [recording, setRecording] = useState(null);
  const [loadingTTS, setLoadingTTS] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    try {
      const res = await axios.post('http://128.100.7.149:5000/chat', {
        user_id: 'shikhar123',
        message: input,
      });

      const botMessage = { role: 'assistant', content: res.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error('Chat API Error:', err);
    }
  };

  const startRecording = async () => {
    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
    } catch (err) {
      console.error('Recording Error:', err);
    }
  };

  const stopRecording = async () => {
    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);

      const formData = new FormData();
      formData.append('file', {
        uri,
        type: 'audio/m4a',
        name: 'audio.m4a',
      });

      const response = await fetch('http://128.100.7.149:5000/transcribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        body: formData,
      });

      const data = await response.json();
      if (data.text) {
        setInput(data.text);
      } else {
        alert('Transcription failed.');
      }
    } catch (err) {
      console.error('STT Error:', err);
      alert('Speech-to-text failed.');
    }
  };

  const renderItem = ({ item }) => (
    <View style={[styles.message, item.role === 'user' ? styles.user : styles.bot]}>
      <Text style={styles.messageText}>{item.content}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        keyExtractor={(_, index) => index.toString()}
        renderItem={renderItem}
        contentContainerStyle={{ padding: 20 }}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Type or speak your message..."
        />
        <TouchableOpacity onPress={handleSend} style={styles.button}>
          <Text>Send</Text>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={recording ? stopRecording : startRecording}
          style={styles.button}
        >
          <Text>{recording ? '🛑' : '🎙️'}</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    borderTopWidth: 1,
    borderColor: '#ccc',
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 8,
    marginRight: 10,
  },
  button: {
    backgroundColor: '#eee',
    borderRadius: 20,
    padding: 10,
    marginLeft: 5,
  },
  message: {
    marginBottom: 12,
    padding: 10,
    borderRadius: 10,
    maxWidth: '80%',
  },
  user: {
    backgroundColor: '#dcf8c6',
    alignSelf: 'flex-end',
  },
  bot: {
    backgroundColor: '#eee',
    alignSelf: 'flex-start',
  },
  messageText: {
    fontSize: 16,
  },
});

import React, { useState } from 'react';
import {
  SafeAreaView,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import axios from 'axios';
import * as Animatable from 'react-native-animatable';
import { Ionicons } from '@expo/vector-icons';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post('http://128.100.7.63:5000/chat', {
        user_id: 'shikhar123',
        message: input,
      });

      const botMessage = {
        id: Date.now().toString(),
        text: res.data.response,
        sender: 'assistant',
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMsg = {
        id: Date.now().toString(),
        text: "Oops! Couldn't reach the server. Try again.",
        sender: 'assistant',
      };
      setMessages((prev) => [...prev, errorMsg]);
    }

    setLoading(false);
  };

  const renderMessage = ({ item }) => (
    <View
      style={[
        styles.messageBubble,
        item.sender === 'user' ? styles.userBubble : styles.botBubble,
      ]}
    >
      <Text style={styles.messageText}>{item.text}</Text>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={renderMessage}
        contentContainerStyle={styles.chat}
      />

      {loading && (
        <Animatable.View
          animation="pulse"
          iterationCount="infinite"
          style={styles.typingBubble}
        >
          <Text style={styles.typingText}>🤖 Typing...</Text>
        </Animatable.View>
      )}

      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        style={styles.inputContainer}
      >
        <TouchableOpacity style={styles.micButton}>
          <Ionicons name="mic" size={24} color="#555" />
        </TouchableOpacity>
        <TextInput
          style={styles.input}
          placeholder="Type something..."
          value={input}
          onChangeText={setInput}
          onSubmitEditing={sendMessage}
        />
        <TouchableOpacity onPress={sendMessage} style={styles.sendButton}>
          <Ionicons name="send" size={22} color="#fff" />
        </TouchableOpacity>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafe',
  },
  chat: {
    padding: 10,
    paddingBottom: 80,
  },
  messageBubble: {
    padding: 12,
    marginVertical: 6,
    maxWidth: '75%',
    borderRadius: 20,
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#d0f0fd',
  },
  botBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#e0e0e0',
  },
  messageText: {
    fontSize: 16,
  },
  inputContainer: {
    flexDirection: 'row',
    position: 'absolute',
    bottom: 10,
    left: 10,
    right: 10,
    backgroundColor: '#fff',
    padding: 8,
    borderRadius: 25,
    alignItems: 'center',
    elevation: 3,
  },
  input: {
    flex: 1,
    paddingHorizontal: 12,
    fontSize: 16,
  },
  sendButton: {
    backgroundColor: '#2978b5',
    padding: 10,
    borderRadius: 20,
    marginLeft: 6,
  },
  micButton: {
    padding: 8,
    marginRight: 6,
  },
  typingBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#eee',
    padding: 10,
    marginLeft: 10,
    borderRadius: 20,
    marginBottom: 10,
  },
  typingText: {
    fontSize: 14,
    color: '#555',
  },
});

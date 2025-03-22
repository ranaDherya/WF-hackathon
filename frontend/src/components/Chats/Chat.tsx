import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./Chat.css";

interface ChatAreaProps {
  selectedChat: string;
  chats: { id: number; sender: string; message: string }[];
  fetchChats: (chatId: string) => void;
}

const API_URL = "http://localhost:8000/api/v1";

const ChatArea: React.FC<ChatAreaProps> = ({
  selectedChat,
  chats,
  fetchChats,
}) => {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chats]); // Auto-scrolls when messages update

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { sender: "user", message: input };

    try {
      await axios.post(`${API_URL}/chats/${selectedChat}/send`, newMessage, {
        headers: { "Content-Type": "application/json" }, // ✅ Ensure JSON format
      });
      fetchChats(selectedChat); // Refresh chat history
      setInput("");
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="chat-area">
      <div className="chat-history">
        {chats.map((chat) => (
          <div key={chat.id} className={`chat-message ${chat.sender}`}>
            {chat.message}
          </div>
        ))}
        <div ref={messagesEndRef} /> {/* Invisible anchor for scrolling */}
      </div>
      <div className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatArea;

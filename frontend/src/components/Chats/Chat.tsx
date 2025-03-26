import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./Chat.css";

interface ChatAreaProps {
  selectedChat: string;
  chats: { id: number; sender: string; message: string; fileUrl?: string }[];
  fetchChats: (chatId: string) => void;
}

const API_URL = "http://localhost:8000/api/v1";

const ChatArea: React.FC<ChatAreaProps> = ({
  selectedChat,
  chats,
  fetchChats,
}) => {
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chats]);

  const sendMessage = async () => {
    if (!input.trim() && !selectedFile) return; // Ensure something is sent

    const formData = new FormData();
    formData.append("message", input); // Send user query

    try {
      await axios.post(`${API_URL}/chats/${selectedChat}/send`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      fetchChats(selectedChat);
      setInput("");
      // setSelectedFile(null);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const uploadFile = async () => {
    const formData = new FormData();
    if (!selectedFile) return;
    if (selectedFile) {
      formData.append("file", selectedFile); // Attach CSV file
    }

    try {
      const res = await axios.post(`${API_URL}/dataset`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log(res);
      fetchChats(selectedChat);
      // setInput("");
      setSelectedFile(null);
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
            {chat.fileUrl && (
              <a href={chat.fileUrl} target="_blank" rel="noopener noreferrer">
                📂 {chat.fileUrl.split("/").pop()}
              </a>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button onClick={uploadFile}>Upload</button>
      </div>
      <div className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        {/* <input type="file" accept=".csv" onChange={handleFileChange} /> */}
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatArea;

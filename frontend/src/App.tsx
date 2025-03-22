import React, { useState, useEffect } from "react";
import axios from "axios";
import LeftPanel from "./components/LeftPanel/LeftPanel";
import ChatArea from "./components/Chats/Chat";
import RightPanel from "./components/Alert/Alert";
import "./App.css";

const API_URL = "http://localhost:8000/api/v1";

export default function App() {
  const [selectedChat, setSelectedChat] = useState<string | null>(null);
  const [chats, setChats] = useState<{ id: string; name: string }[]>([]);
  const [messages, setMessages] = useState<
    { id: number; sender: string; message: string }[]
  >([]);

  // Fetch available chats
  const fetchChatsList = async () => {
    try {
      const response = await axios.get(`${API_URL}/chats`);
      setChats(response.data);
      if (response.data.length > 0 && !selectedChat) {
        setSelectedChat(response.data[0].id); // Auto-select first chat
      }
    } catch (error) {
      console.error("Error fetching chat list:", error);
    }
  };

  // Fetch messages for the selected chat
  const fetchMessages = async (chatId: string) => {
    try {
      const response = await axios.get(`${API_URL}/chats/${chatId}`);
      setMessages(response.data);
    } catch (error) {
      console.error("Error fetching chat messages:", error);
    }
  };

  // Function to switch chat and fetch messages
  const switchChat = (chatId: string) => {
    setSelectedChat(chatId);
    fetchMessages(chatId);
  };

  // Create a new chat
  const createNewChat = async () => {
    try {
      const response = await axios.post(`${API_URL}/chats`);
      setChats((prevChats) => [...prevChats, response.data]);
      switchChat(response.data.id);
    } catch (error) {
      console.error("Error creating new chat:", error);
    }
  };

  // Delete a chat
  const deleteChat = async (chatId: string) => {
    try {
      await axios.delete(`${API_URL}/chats/${chatId}`);
      setChats((prevChats) => prevChats.filter((chat) => chat.id !== chatId));
      fetchChatsList();

      if (selectedChat === chatId) {
        setSelectedChat(chats.length > 0 ? chats[0].id : null);
        if (chats.length > 0) fetchMessages(chats[0].id);
      }
    } catch (error) {
      console.error("Error deleting chat:", error);
    }
  };

  useEffect(() => {
    fetchChatsList();
  }, []);

  useEffect(() => {
    if (selectedChat) {
      fetchMessages(selectedChat);
    }
  }, [selectedChat]);

  return (
    <div className="container">
      <LeftPanel
        chats={chats}
        switchChat={switchChat}
        createNewChat={createNewChat}
        deleteChat={deleteChat}
      />
      {selectedChat && (
        <ChatArea
          selectedChat={selectedChat}
          chats={messages}
          fetchChats={fetchMessages}
        />
      )}
      <RightPanel />
    </div>
  );
}

import React, { useState } from "react";
import ConfirmModal from "../PopUp/PopUp";
import "./LeftPanel.css";

interface Chat {
  id: string;
  name: string;
}

interface LeftPanelProps {
  chats: Chat[];
  switchChat: (chatId: string) => void;
  createNewChat: () => void;
  deleteChat: (chatId: string) => void;
}

const LeftPanel: React.FC<LeftPanelProps> = ({
  chats,
  switchChat,
  createNewChat,
  deleteChat,
}) => {
  const [selectedChatId, setSelectedChatId] = useState<string | null>(null);
  const [selectedChatToDelete, setSelectedChatToDelete] = useState<
    string | null
  >(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleChatClick = (chatId: string) => {
    setSelectedChatId(chatId);
    switchChat(chatId); // Ensuring chat switching works properly
  };

  const handleDeleteClick = (chatId: string) => {
    setSelectedChatToDelete(chatId);
    setIsModalOpen(true);
  };

  const handleConfirmDelete = () => {
    if (selectedChatToDelete) {
      deleteChat(selectedChatToDelete);
    }
    setIsModalOpen(false);
  };

  return (
    <div className="left-panel">
      <div className="left-panel-header">
        <h3>Chats</h3>
        <button className="new-chat-btn" onClick={createNewChat}>
          + New Chat
        </button>
      </div>
      <ul className="chat-list">
        {chats.map((chat) => (
          <li
            key={chat.id}
            className={`chat-item ${
              chat.id === selectedChatId ? "active" : ""
            }`}
            onClick={() => handleChatClick(chat.id)}
          >
            <span>{chat.name}</span>
            <button
              className="delete-btn"
              onClick={(e) => {
                e.stopPropagation(); // Prevents click event from selecting the chat
                handleDeleteClick(chat.id);
              }}
            >
              🗑
            </button>
          </li>
        ))}
      </ul>
      <ConfirmModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onConfirm={handleConfirmDelete}
      />
    </div>
  );
};

export default LeftPanel;

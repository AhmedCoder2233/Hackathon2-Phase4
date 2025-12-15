// frontend/app/chat/page.tsx
"use client";

import React from 'react';
import ChatkitWrapper from '../../components/chatkit-ui/ChatkitWrapper'; // Import ChatkitWrapper
import { useCallback, useState } from "react";
import clsx from "clsx";


const ChatPage = () => {

  const [threadId, setThreadId] = useState<string | null>(null);

  const containerClass = clsx(
    "min-h-screen bg-gradient-to-br transition-colors duration-300",
    "from-slate-100 via-white to-slate-200 text-slate-900",
  );

  const handleThreadChange = useCallback((id: string | null) => {
    console.log('🔄 Thread ID updated:', id);
    setThreadId(id);
  }, []);

  const handleResponseCompleted = useCallback(() => {
    console.log('✅ Response completed for thread:', threadId);
  }, [threadId]);

  return (
    <div className="flex flex-col h-screen">
      <header className="bg-gray-800 text-white p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">Chat</h1>
        {/* Placeholder for future user/logout info */}
      </header>
      <main className="flex-1 flex flex-col">
        {/* ChatKit component will be rendered here */}
        <ChatkitWrapper onResponseCompleted={handleResponseCompleted} onThreadChange={handleThreadChange}/> {/* Render the ChatkitWrapper component */}
      </main>
    </div>
  );
};

export default ChatPage;

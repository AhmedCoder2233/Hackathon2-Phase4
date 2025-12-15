import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { useSession } from "../../app/lib/auth-client";

type ChatKitPanelProps = {
  onThreadChange: (threadId: string | null) => void;
  onResponseCompleted: () => void;
};

export default function ChatKitPanel({
  onThreadChange,
  onResponseCompleted,
}: ChatKitPanelProps) {
  
  const { data: session, isPending } = useSession();

 const chatkit = useChatKit({
  api: {
    url: 'http://localhost:8000/support/chatkit',
    domainKey: 'localdev',
    
    // ✅ FETCH FUNCTION PROPERLY ADD KARO
    fetch: async (url, options = {}) => {
      console.log("🔍 ChatKit Request:", url);
      console.log("🔑 Session:", session);
      
      // Agar session nahi hai
      if (!session?.user.id) {
        console.warn("⚠️ No access token available");
        // Token ke bina request bhejo (testing ke liye)
        return fetch(url, options);
      }

      console.log("✅ Sending with token:", session?.user.id.substring(0, 20));
      
      return fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${session?.user.id}`,
          'Content-Type': 'application/json',
        },
      });
    }
  },
  
  theme: {
    color: {
      grayscale: {
        hue: 220,
        tint: 6,
        shade: -4,
      },
      accent: {
        primary: "#0f172a",
        level: 1,
      },
    },
    radius: "round",
  },
  
  startScreen: {
    greeting: "Hello how can i assist you?",
  },
  
  composer: {
    placeholder: "Ask the concierge a question",
  },
  
  threadItemActions: {
    feedback: false,
  },
  
  onResponseEnd: () => {
    onResponseCompleted();
  },
  
  onThreadChange: ({ threadId }) => {
    onThreadChange(threadId ?? null);
  },
  
  onError: ({ error }) => {
    console.error("ChatKit error", error);
  },
});

  // Loading state handle karo
  if (isPending) {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <p>Loading chat...</p>
      </div>
    );
  }

  // Agar session nahi hai
  if (!session) {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <p>Please log in to use chat</p>
      </div>
    );
  }

  return (
    <div className="relative h-full w-full overflow-hidden border border-slate-200/60 bg-white shadow-card dark:border-slate-800/70 dark:bg-slate-900">
      <ChatKit control={chatkit.control} className="block h-full w-full" />
    </div>
  );
}
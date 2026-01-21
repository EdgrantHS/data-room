import { Conversation, ConversationContent } from "@/components/ai/conversation"
import { Reasoning, ReasoningTrigger, ReasoningContent } from "@/components/ai/reasoning"

interface Message {
  role: "user" | "assistant" | "system"
  content: string
  image?: string
}

interface ChatMessagesProps {
  messages: Message[]
  currentPlan: string | null
  isProcessing: boolean
}

export function ChatMessages({ messages, currentPlan, isProcessing }: ChatMessagesProps) {
  return (
    <div className="flex-1 overflow-y-auto">
      <Conversation className="h-full">
        <ConversationContent>
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`rounded-lg px-4 py-2 ${
                msg.role === "user" 
                  ? "bg-primary text-primary-foreground max-w-[80%]" 
                  : msg.role === "system"
                  ? "bg-muted w-screen text-gray-400 items-center text-center text-2xl"
                  : "bg-secondary text-secondary-foreground max-w-[80%]"
              }`}>
                {msg.content}
                {msg.image && (
                  <img src={msg.image} alt="Generated chart" className="mt-2 max-w-full rounded" />
                )}
              </div>
            </div>
          ))}
          {isProcessing && (
            <div className="flex justify-start">
              <div className="rounded-lg px-4 py-2 bg-secondary text-secondary-foreground max-w-[80%]">
                <span className="animate-pulse">Thinking...</span>
              </div>
            </div>
          )}
          {currentPlan && (
            <Reasoning isStreaming={false}>
              <ReasoningTrigger />
              <ReasoningContent>{currentPlan}</ReasoningContent>
            </Reasoning>
          )}
        </ConversationContent>
      </Conversation>
    </div>
  )
}

export type { Message }

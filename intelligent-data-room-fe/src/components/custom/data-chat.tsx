import { useState, type FormEvent } from "react";
import { ChatMessages, type Message } from "./chat-messages";
import { ChatInput } from "./chat-input";
import { handleFileUpload, handlePromptSubmit } from "./chat-handlers";

export function DataChat() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "system", content: "Please upload a CSV file to begin." },
  ]);
  const [dataframeId, setDataframeId] = useState<string | null>(null);
  const [currentPlan, setCurrentPlan] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [inputValue, setInputValue] = useState("");

  const onFileUpload = (files: File[]) => {
    handleFileUpload(files, setDataframeId, setMessages, setIsProcessing);
  };

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!dataframeId || !inputValue.trim()) return;

    const prompt = inputValue;
    setInputValue("");
    await handlePromptSubmit(
      dataframeId,
      prompt,
      messages,
      setMessages,
      setCurrentPlan,
      setIsProcessing,
    );
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSubmit(e as any);
    }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col bg-secondary items-center overflow-y-scroll">
      <div className="w-screen flex justify-center pb-4 max-w-6xl border-x-2 border-b-2">
        <div className="pb-4 pt-2 px-8 border-b bg-muted-foreground text-center rounded-b-4xl">
          <h1 className="text-2xl font-bold text-primary-foreground">Intelligent Data Room</h1>
          <p className="text-sm text-primary-foreground/70">Upload your CSV and start querying your data!</p>
        </div>
      </div>
      <div className="h-screen flex-col flex max-w-6xl w-full border-x-2">
        <ChatMessages messages={messages} currentPlan={currentPlan} isProcessing={isProcessing} />
        <ChatInput
          dataframeId={dataframeId}
          inputValue={inputValue}
          isProcessing={isProcessing}
          onFileUpload={onFileUpload}
          onInputChange={setInputValue}
          onSubmit={onSubmit}
          onKeyDown={onKeyDown}
        />
      </div>
    </div>
  );
}

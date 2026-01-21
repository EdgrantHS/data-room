import { type FormEvent } from "react";
import {
  Dropzone,
  DropzoneEmptyState,
  DropzoneContent,
} from "@/components/ui/shadcn-io/dropzone";
import { Textarea } from "@/components/ui/textarea";

interface ChatInputProps {
  dataframeId: string | null;
  inputValue: string;
  isProcessing: boolean;
  onFileUpload: (files: File[]) => void;
  onInputChange: (value: string) => void;
  onSubmit: (e: FormEvent) => void;
  onKeyDown: (e: React.KeyboardEvent) => void;
}

export function ChatInput({
  dataframeId,
  inputValue,
  isProcessing,
  onFileUpload,
  onInputChange,
  onSubmit,
  onKeyDown,
}: ChatInputProps) {
  return (
    <div className="border-t p-4">
      {!dataframeId ? (
        <Dropzone
          accept={{ csv: [".csv"], xlsx: [".xlsx"] }}
          maxFiles={1}
          onDrop={onFileUpload}
          disabled={isProcessing}
        >
          <DropzoneEmptyState />
          <DropzoneContent />
        </Dropzone>
      ) : (
        <form onSubmit={onSubmit} className="flex gap-2">
          <Textarea
            value={inputValue}
            onChange={(e) => onInputChange(e.target.value)}
            placeholder="Ask a question about your data..."
            disabled={isProcessing}
            className="flex-1 bg-white"
            onKeyDown={onKeyDown}
          >
          </Textarea>
        </form>
      )}
    </div>
  );
}

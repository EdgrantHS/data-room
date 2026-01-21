import axios from "axios"
import * as XLSX from "xlsx"
import type { Message } from "./chat-messages"

const API_BASE = "http://localhost:8000"

// Handle file upload and update state accordingly
export async function handleFileUpload(
  files: File[],
  setDataframeId: (id: string) => void,
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>,
  setIsProcessing: (processing: boolean) => void
) {
  if (files.length === 0) return

  setIsProcessing(true)
  try {
    const file = files[0]
    let fileToUpload = file

    // Convert xlsx to csv if needed
    if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
      const arrayBuffer = await file.arrayBuffer()
      const workbook = XLSX.read(arrayBuffer, { type: 'array' })
      const firstSheet = workbook.Sheets[workbook.SheetNames[0]]
      const csvContent = XLSX.utils.sheet_to_csv(firstSheet)
      
      // Create a new CSV file
      const csvBlob = new Blob([csvContent], { type: 'text/csv' })
      fileToUpload = new File([csvBlob], file.name.replace(/\.xlsx?$/, '.csv'), { type: 'text/csv' })
    }

    const formData = new FormData()
    formData.append("file", fileToUpload)

    const { data } = await axios.post(`${API_BASE}/upload`, formData)
    
    setDataframeId(data.dataframe_id)
    setMessages(prev => [...prev, 
      { role: "assistant", content: `File "${data.filename}" uploaded successfully. You can now ask questions about your data.` }
    ])
  } catch (error) {
    setMessages(prev => [...prev, 
      { role: "assistant", content: `Upload failed: ${error}` }
    ])
  } finally {
    setIsProcessing(false)
  }
}

// Handle prompt submission, generate plan, execute it, and update messages
export async function handlePromptSubmit(
  dataframeId: string,
  prompt: string,
  messages: Message[],
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>,
  setCurrentPlan: (plan: string | null) => void,
  setIsProcessing: (processing: boolean) => void
) {
  setMessages(prev => [...prev, { role: "user", content: prompt }])
  setIsProcessing(true)

  try {
    // Get last 5 messages for context
    const recentMessages = messages.slice(-5)
    const conversationHistory = recentMessages
      .map(msg => `${msg.role}: ${msg.content}`)
      .join('\n')
    
    const fullPrompt = conversationHistory 
      ? `Conversation history:\n${conversationHistory}\n\nCurrent question: ${prompt}`
      : prompt

    // Generate plan
    const planFormData = new FormData()
    planFormData.append("dataframe_id", dataframeId)
    planFormData.append("prompt", fullPrompt)

    const { data: planData } = await axios.post(`${API_BASE}/generate-plan`, planFormData)
    setCurrentPlan(planData.plan)

    // Execute plan
    const executeFormData = new FormData()
    executeFormData.append("dataframe_id", dataframeId)
    executeFormData.append("plan", planData.plan)

    const { data: executeData } = await axios.post(`${API_BASE}/execute-plan`, executeFormData)

    // Check if response is base64 image
    const response = executeData.response
    if (response.startsWith("data:image")) {
      setMessages(prev => [...prev, { role: "assistant", content: "Here's the visualization:", image: response }])
    } else {
      setMessages(prev => [...prev, { role: "assistant", content: response }])
    }

    setCurrentPlan(null)
  } catch (error) {
    setMessages(prev => [...prev, { role: "assistant", content: `Error: ${error}` }])
    setCurrentPlan(null)
  } finally {
    setIsProcessing(false)
  }
}

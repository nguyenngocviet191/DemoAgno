'use client'
import { useState, useRef } from 'react'
import { toast } from 'sonner'
import { TextArea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { usePlaygroundStore } from '@/store'
import useAIChatStreamHandler from '@/hooks/useAIStreamHandler'
import { useQueryState } from 'nuqs'
import Icon from '@/components/ui/icon'
import { Paperclip, Send, X } from 'lucide-react'
const ChatInput = () => {
  const { chatInputRef } = usePlaygroundStore()

  const { handleStreamResponse } = useAIChatStreamHandler()
  const [selectedAgent] = useQueryState('agent')
  const [inputMessage, setInputMessage] = useState('')
  // input attched files
  const [attachedFiles, setAttachedFiles] = useState<File[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)

  const isStreaming = usePlaygroundStore((state) => state.isStreaming)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files) {
      setAttachedFiles([...attachedFiles, ...Array.from(files)])
    }
  }

  const handleRemoveFile = (index: number) => {
    setAttachedFiles(attachedFiles.filter((_, i) => i !== index))
  }


  const handleSubmit = async () => {
    if (!inputMessage.trim() && attachedFiles.length === 0) return
    console.log('Sending:', inputMessage, attachedFiles)
    const currentMessage = inputMessage
    const currentFiles = attachedFiles
    setInputMessage('')
    setAttachedFiles([])
    console.log(`gửi ${(attachedFiles.length)} file(s)`);
    try {
      await handleStreamResponse(currentMessage, currentFiles)
    } catch (error) {
      toast.error(
        `Error in handleSubmit: ${
          error instanceof Error ? error.message : String(error)
        }`
      )
    }
  }

  return (
    <div className="relative mx-auto flex w-full max-w-2xl flex-col  p-3 shadow-sm">
      {/* Danh sách file preview */}
      {attachedFiles.length > 0 && (
        <div className="mb-2 flex flex-wrap gap-2">
          {attachedFiles.map((file, index) => (
            <div key={index} className="relative flex items-center gap-2 p-2 border rounded-md">
              {file.type.startsWith('image/') ? (
                <img
                  src={URL.createObjectURL(file)}
                  alt="Preview"
                  className="w-16 h-16 object-cover rounded-md"
                />
              ) : (
                <span className="text-sm">{file.name}</span>
              )}
              <button
                onClick={() => handleRemoveFile(index)}
                className="absolute top-0 right-0 bg-gray-700 text-white rounded-full p-1 hover:bg-red-500"
              >
                <X className="size-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Ô nhập tin nhắn và nút đính kèm */}
      <div className="flex items-center rounded-full border border-[rgba(var(--color-border-default))] px-4 py-2">
        {/* Nút đính kèm */}
        <button
          className="text-gray-100 hover:text-gray-700"
          onClick={() => fileInputRef.current?.click()}
        >
          <Paperclip className="size-5" />
        </button>
        <input
          type="file"
          multiple
          ref={fileInputRef}
          className="hidden"
          onChange={handleFileChange}
        />

        {/* Ô nhập văn bản */}
        <textarea
          placeholder="Type something..."
          rows={2}
          className="mx-3 flex-1 border-none bg-transparent focus:outline-none h-auto max-h-16 overflow-hidden resize-none"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)} 
        />

        {/* Nút gửi */}
        <button className="text-gray-100 hover:text-gray-700" onClick={handleSubmit}>
          <Send className="size-5" />
        </button>
      </div>
    </div>
  )

}

export default ChatInput

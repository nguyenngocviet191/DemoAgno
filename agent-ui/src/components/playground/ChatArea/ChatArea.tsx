'use client'

import ChatInput from './ChatInput'
import MessageArea from './MessageArea'
import NewChatButton from '@/components/playground/Sidebar/NewChatButton'
const ChatArea = () => {
  return (
    <main className="relative flex flex-grow flex-col w-full h-full">
      <div className="sticky top-0 ml-auto px-4 pt-2 pb-2">
        <NewChatButton/>
      </div>
      <MessageArea />
      <div className="sticky bottom-0 ml-9 px-4 pt-2 pb-2">
        <ChatInput />
      </div>
    </main>
  )
}

export default ChatArea

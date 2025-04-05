'use client'
import Sidebar from '@/components/playground/Sidebar/Sidebar'
import { ChatArea } from '@/components/playground/ChatArea'
import { Suspense } from 'react'
import  ChatbotSettings from '@/components/playground/ChatbotSettings'
import { useBotInfo} from '@/store'
import Sessions from '@/components/playground/Sidebar/Sessions'
import { AgentList } from '@/components/playground/Sidebar/AgentList'

import { usePlaygroundStore } from '@/store'

export default function Home() {
  const isOpen = useBotInfo((s) => s.isOpen);
  const {isMounted,isEndpointActive} = usePlaygroundStore()

  return (
    <Suspense fallback={<div>Loading...</div>}>
        {/* Sidebar */}
        <div className="flex flex-row" >
          <Sidebar />
          {/* <div className="flex flex-col h-screen bg-background/80"> */}
          <div className="flex flex-col h-screen">
          {/* Header */}
          <div className="PageHeader flex flex-shrink-0 border-b border-border px-3 py-2">
            This is Header
          </div>
          <div className="flex flex-row flex-1 gap-5 overflow-hidden">
            {/* Main Content */}
           
              {/* Conditional Sessions Component */}
              <div className="flex flex-col left-2 max-w-[300px]">
              <AgentList />
                      {/* {selectedModel && agentId && (
                        <ModelDisplay model={selectedModel} />
                      )} */}
              {isMounted && isEndpointActive && (
   
                  <Sessions />
         
              )}
              </div>
              {/* Chat Area */}
              <ChatArea />
              {/* Chatbot Settings */}
              {isOpen && <ChatbotSettings />}
            
          </div>
                </div>
        </div>
    </Suspense>
  );
}


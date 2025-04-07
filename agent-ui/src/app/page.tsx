'use client'
import Sidebar from '@/components/playground/Sidebar/Sidebar'
import Avatar from '@/components/Avartar'
import Endpoint from '@/components/playground/Sidebar/Endpoint'
import { ChatArea } from '@/components/playground/ChatArea'
import { Suspense } from 'react'
import  ChatbotSettings from '@/components/playground/ChatbotSettings'
import { useBotInfo} from '@/store'
import Sessions from '@/components/playground/Sidebar/Sessions'
import { AgentList } from '@/components/playground/Sidebar/AgentList'
import { useThemeStore } from '@/store/themeStore'; // Ensure this matches the export in themeStore
import { usePlaygroundStore } from '@/store'

export default function Home() {
  const isOpen = useBotInfo((s) => s.isOpen);
  const {isMounted,isEndpointActive} = usePlaygroundStore()

  return (
    <Suspense fallback={<div>Loading...</div>}>
        {/* Sidebar */}
        <div className="flex flex-row w-full ">
          
              <div className="flex flex-col left-2 max-w-[300px] border-r border-border">
                <Endpoint />
                <div className="flex min-h-[300px] max-h-[600px]">
                  <AgentList />
                </div>
                        {/* {selectedModel && agentId && (
                          <ModelDisplay model={selectedModel} />
                        )} */}
                {isMounted && isEndpointActive && ( <Sessions />)}
              </div>
                <div className="max-w-[800px] border-r border-border">
                {/* Chat Area */}
                <ChatArea />
              </div>
              <div>
                Workscreen
              </div>
              {/* Chatbot Settings */}
              {isOpen && <ChatbotSettings />}
          </div>

    </Suspense>
  );
}


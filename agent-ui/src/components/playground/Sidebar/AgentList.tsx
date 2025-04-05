'use client'

import * as React from 'react'
import { usePlaygroundStore } from '@/store'
import { useQueryState } from 'nuqs'
import Icon from '@/components/ui/icon'
import { useEffect } from 'react'
import useChatActions from '@/hooks/useChatActions'

export function AgentList() {
  const { agents, setMessages, setSelectedModel, setHasStorage } =
    usePlaygroundStore()
  const { focusChatInput } = useChatActions()
  const [agentId, setAgentId] = useQueryState('agent', {
    parse: (value) => value || undefined,
    history: 'push'
  })
  const [, setSessionId] = useQueryState('session')

  // Set the model when the component mounts if an agent is already selected
  useEffect(() => {
    if (agentId && agents.length > 0) {
      const agent = agents.find((agent) => agent.value === agentId)
      if (agent) {
        setSelectedModel(agent.model.provider || '')
        setHasStorage(!!agent.storage)
        if (agent.model.provider) {
          focusChatInput()
        }
      } else {
        setAgentId(agents[0].value)
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [agentId, agents, setSelectedModel])

  const handleOnClick = (value: string) => {
    const newAgent = value === agentId ? '' : value
    const selectedAgent = agents.find((agent) => agent.value === newAgent)
    setSelectedModel(selectedAgent?.model.provider || '')
    setHasStorage(!!selectedAgent?.storage)
    setAgentId(newAgent)
    setMessages([]) // Clear messages when agent changes
    setSessionId(null) // Reset session ID
    if (selectedAgent?.model.provider) {
      focusChatInput()
    }
  }

  return (
    <div className="w-full max-h-80 overflow-y-auto p-2 bg-primaryAccent rounded-lg shadow-lg">
      <div className="text-xs font-medium uppercase text-primary">Select an Agent</div>
      <div className="flex flex-col gap-2">
        {agents.map((agent) => (
          <div
            key={agent.value}
            onClick={() => handleOnClick(agent.value)}
            className={`flex items-center gap-3 p-2 rounded-lg cursor-pointer 
              ${agentId === agent.value ? 'bg-primary/10 text-primary font-medium' : 'hover:bg-primary/5'}`}
          >
            <Icon type={'agent'} size="xs" />
            <span className="text-sm font-medium">{agent.label}</span>
          </div>
        ))}
        {agents.length === 0 && (
          <div className="text-center text-sm text-muted">No agents found</div>
        )}
      </div>
    </div>
  )
}
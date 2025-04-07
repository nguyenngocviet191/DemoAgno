'use client'
import { Button } from '@/components/ui/button'
// import { AgentSelector } from '@/components/playground/Sidebar/AgentSelector'

import useChatActions from '@/hooks/useChatActions'
import { usePlaygroundStore } from '@/store'
import { motion, AnimatePresence } from 'framer-motion'
import { useState, useEffect } from 'react'
import Icon from '@/components/ui/icon'
import { getProviderIcon } from '@/lib/modelProvider'
import Sessions from './Sessions'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useThemeStore } from '@/store/themeStore'; // Ensure this matches the export in themeStore
import { useQueryState } from 'nuqs'

import { Skeleton } from '@/components/ui/skeleton'
import clsx from 'clsx'
import { Home, Settings, Info } from 'lucide-react'
const SidebarHeader = () => (
  <div className="flex items-center gap-2">
    <Icon type="agno" size="xs" />
    <span className="text-xs font-medium uppercase text-white">Agent UI</span>
  </div>
)

const SidebarFooter = () => (
  <div className="sticky bottom-0 flex items-center gap-2">
    {/* <Icon type="agno" size="xs" /> */}
    <span className="text-xs font-medium uppercase text-white">Setting</span>
  </div>
)


const links = [
  { name: 'Home', href: '/', icon: Home },
  { name: 'Studio', href: '/studio', icon: Info },
  { name: 'Settings', href: '/settings', icon: Settings },
]

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const { clearChat, focusChatInput, initializePlayground } = useChatActions()
  const {
    isMounted,
    setIsMounted,
    messages,
    selectedEndpoint,
    isEndpointActive,
    selectedModel,
    hydrated,
    isEndpointLoading
  } = usePlaygroundStore()
  const pathname = usePathname()
  const { theme, toggleTheme } = useThemeStore();

  // const [isMounted, setIsMounted] = useState(false)
  const [agentId] = useQueryState('agent')
  useEffect(() => {
    setIsMounted(true)
    
    if (hydrated) initializePlayground()
  }, [selectedEndpoint, initializePlayground, hydrated])
  const handleNewChat = () => {
    clearChat()
    focusChatInput()
  }
  return (
    <main className="relative flex flex-grow  h-full">
      <motion.aside
        className="relative flex  flex-col  overflow-hidden px-2 py-3  border-r border-border"
        initial={{ width: '8rem' }}
        animate={{ width: isCollapsed ? '3rem' : '8rem' }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      >
        <motion.button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="absolute right-2 top-2 z-10 p-1"
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          type="button"
          whileTap={{ scale: 0.95 }}
        >
          <Icon
            type="sheet"
            size="xs"
            className={`transform ${isCollapsed ? 'rotate-180' : 'rotate-0'}`}
          />
        </motion.button>
        <motion.div
          className="w-60 space-y-5"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: isCollapsed ? 0 : 1, x: isCollapsed ? -20 : 0 }}
          transition={{ duration: 0.3, ease: 'easeInOut' }}
          style={{
            pointerEvents: isCollapsed ? 'none' : 'auto'
          }}
        >
          {/* <SidebarHeader /> */}
          <nav className="flex flex-col gap-2 mt-4 font-medium">
          {links.map(({ name, href, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={clsx(
                'px-2 py-2 rounded hover:bg-gray-400',
                pathname === href && 'bg-gray-600 font-semibold'
              )}
            >
             <div className="flex flex-row gap-2">
               <Icon className="w-5 h-5" />
               {name}
             </div>
            </Link>
          ))}
        </nav>
          {/* <SidebarFooter /> */}
          <button
            onClick={toggleTheme}
            className="sticky bottom-0 border border-border p-4 max-h-[30px] rounded text-xs font-medium uppercase"
          >
            {theme === 'light' ? 'Dark' : 'Light'} Mode
          </button>
      
      
        </motion.div>

      </motion.aside>
      
    </main>
  )
}

export default Sidebar

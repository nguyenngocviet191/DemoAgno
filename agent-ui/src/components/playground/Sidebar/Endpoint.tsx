'use client'
import { Button } from '@/components/ui/button'
import { usePlaygroundStore } from '@/store'
import { useThemeStore } from '@/store/themeStore'; // Ensure this matches the export in themeStore
import { useState, useEffect } from 'react'
import useChatActions from '@/hooks/useChatActions'
import { useQueryState } from 'nuqs'
import { isValidUrl } from '@/lib/utils'
import { toast } from 'sonner'
import Icon from '@/components/ui/icon'
import { motion, AnimatePresence } from 'framer-motion'
import { truncateText } from '@/lib/utils'
// const ModelDisplay = ({ model }: { model: string }) => (
//     <div className="flex h-9 w-full items-center gap-3 rounded-xl border border-primary/15 bg-accent p-3 text-xs font-medium uppercase text-muted">
//       {(() => {
//         const icon = getProviderIcon(model)
//         return icon ? <Icon type={icon} className="shrink-0" size="xs" /> : null
//       })()}
//       {model}
//     </div>
//   )

  
const ENDPOINT_PLACEHOLDER = 'NO ENDPOINT ADDED'

const Endpoint = () => {
    const {
      isMounted,
      selectedEndpoint,
      isEndpointActive,
      setIsMounted,
      setSelectedEndpoint,
      setAgents,
      setSessionsData,
      setMessages
    } = usePlaygroundStore()
    const { initializePlayground } = useChatActions()
    const [isEditing, setIsEditing] = useState(false)
    // const isEditing = false
    const [endpointValue, setEndpointValue] = useState('')
    // const [isMounted, setIsMounted] = useState(false)
    const [isHovering, setIsHovering] = useState(false)
    const [isRotating, setIsRotating] = useState(false)
    const [, setAgentId] = useQueryState('agent')
    const [, setSessionId] = useQueryState('session')
  
    useEffect(() => {
      setEndpointValue(selectedEndpoint)
      setIsMounted(true)
    }, [selectedEndpoint])
  
    const getStatusColor = (isActive: boolean) =>
      isActive ? 'bg-positive' : 'bg-destructive'
  
    const handleSave = async () => {
      if (!isValidUrl(endpointValue)) {
        toast.error('Please enter a valid URL')
        return
      }
      const cleanEndpoint = endpointValue.replace(/\/$/, '')
      setSelectedEndpoint(cleanEndpoint)
      setAgentId(null)
      setSessionId(null)
      setIsEditing(false)
      setIsHovering(false)
      setAgents([])
      setSessionsData([])
      setMessages([])
    }
  
    const handleCancel = () => {
      setEndpointValue(selectedEndpoint)
      setIsEditing(false)
      setIsHovering(false)
    }
  
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter') {
        handleSave()
      } else if (e.key === 'Escape') {
        handleCancel()
      }
    }
  
    const handleRefresh = async () => {
      setIsRotating(true)
      await initializePlayground()
      setTimeout(() => setIsRotating(false), 500)
    }
  
    return (
      <div className="flex flex-col items-start items-start gap-2">
        <div className="text-xs font-medium uppercase p-2 ">Endpoint</div>
        {isEditing ? (
            // edit enpoint mode
          <div className="flex w-full items-center gap-1">
            <input
              type="text"
              value={endpointValue}
              onChange={(e) => setEndpointValue(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex h-9 w-full items-center text-ellipsis rounded-xl border border-primary/15 bg-accent p-3 text-xs font-medium text-muted"
              autoFocus
            />
            <Button
              variant="ghost"
              size="icon"
              onClick={handleSave}
              className="hover:cursor-pointer hover:bg-transparent"
            >
              <Icon type="save" size="xs" />
            </Button>
          </div>
        ) : (
             // ready enpoint mode
          <div className="flex flex-row w-full items-start gap-1">
            <motion.div
              className="relative flex h-9 w-[200px] cursor-pointer items-center justify-between rounded-xl border border-primary/15 bg-accent p-3 uppercase"
              onMouseEnter={() => setIsHovering(true)}
              onMouseLeave={() => setIsHovering(false)}
              onClick={() => setIsEditing(true)}
              transition={{ type: 'spring', stiffness: 400, damping: 10 }}
            >
              <AnimatePresence mode="wait">
                {isHovering ? (
                  <motion.div
                    key="endpoint-display-hover"
                    className="absolute inset-0 flex items-center justify-center"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <p className="flex items-center gap-2 whitespace-nowrap text-xs font-medium text-primary">
                      <Icon type="edit" size="xxs" /> EDIT ENDPOINT
                    </p>
                  </motion.div>
                ) : (
                  <motion.div
                    key="endpoint-display"
                    className="absolute inset-0 flex items-center justify-between px-3"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <p className="text-xs font-medium text-muted">
                      {isMounted
                        ? truncateText(selectedEndpoint, 21) ||
                          ENDPOINT_PLACEHOLDER
                        : 'http://localhost:7777'}
                    </p>
                    <div
                      className={`size-2 shrink-0 rounded-full ${getStatusColor(isEndpointActive)}`}
                    />
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleRefresh}
              className="hover:cursor-pointer hover:bg-transparent"
            >
              <motion.div
                key={isRotating ? 'rotating' : 'idle'}
                animate={{ rotate: isRotating ? 360 : 0 }}
                transition={{ duration: 0.5, ease: 'easeInOut' }}
              >
                <Icon type="refresh" size="xs" />
              </motion.div>
            </Button>
          </div>
        )}
      </div>
    )
  }
  export default Endpoint

//   {isMounted && (
//     <>
//       {/* <Endpoint /> */}
//       {isEndpointActive && (
//         <>
//           <motion.div
//             className="flex w-full flex-col items-start gap-2"
//             initial={{ opacity: 0 }}
//             animate={{ opacity: 1 }}
//             transition={{ duration: 0.5, ease: 'easeInOut' }}
//           >
//             {isEndpointLoading ? (
//               <div className="flex w-full flex-col gap-2">
//                 {Array.from({ length: 2 }).map((_, index) => (
//                   <Skeleton
//                     key={index}
//                     className="h-9 w-full rounded-xl"
//                   />
//                 ))}
//               </div>
//             ) : (
//               <>
               
//               </>
//             )}
//           </motion.div>
//           {/* <Sessions /> */}
//         </>
//       )}
//     </>
//   )}
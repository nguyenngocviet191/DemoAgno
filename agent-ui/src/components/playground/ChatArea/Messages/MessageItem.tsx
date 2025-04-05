import Icon from '@/components/ui/icon'
import MarkdownRenderer from '@/components/ui/typography/MarkdownRenderer'
import { usePlaygroundStore } from '@/store'
import type { PlaygroundChatMessage } from '@/types/playground'
import Videos from './Multimedia/Videos'
import Images from './Multimedia/Images'
import Audios from './Multimedia/Audios'
import { memo } from 'react'
import AgentThinkingLoader from './AgentThinkingLoader'
import { Reply, Copy } from 'lucide-react'
import { useBotInfo} from '@/store'


interface MessageProps {
  message: PlaygroundChatMessage
}


const AgentMessage = ({ message }: MessageProps) => {
  const { streamingErrorMessage } = usePlaygroundStore()
  const open = useBotInfo((s) =>  s.open);
  let messageContent
  // console.log('message:', message)
  if (message.streamingError) {
    messageContent = (
      <p className="text-destructive">
        Oops! Something went wrong while streaming.{' '}
        {streamingErrorMessage ? (
          <>{streamingErrorMessage}</>
        ) : (
          'Please try refreshing the page or try again later.'
        )}
      </p>
    )
  } else if (message.content) {
    // console.log('Images:', message.images);
    messageContent = (
      <div className="flex w-full flex-col gap-4">
        <MarkdownRenderer>{message.content}</MarkdownRenderer>
        <div className="flex w-full justify-end gap-4">
          <button className="text-gray-100 hover:text-gray-700">
            <Reply className="size-3" />
          </button>
          <button className="text-gray-100 hover:text-gray-700">
            <Copy className="size-3" />
          </button>
        </div>
        {message.videos && message.videos.length > 0 && (
          <Videos videos={message.videos} />
        )}
        {message.images && message.images.length > 0 && (
          <Images images={message.images} />
        )}
        {message.audio && message.audio.length > 0 && (
          <Audios audio={message.audio} />
        )}
      </div>
    )
  } else if (message.response_audio) {
    if (!message.response_audio.transcript) {
      messageContent = (
        <div className="mt-2 flex items-start">
          <AgentThinkingLoader />
        </div>
      )
    } else {
      messageContent = (
        <div className="flex w-full flex-col gap-4">
          <MarkdownRenderer>
            {message.response_audio.transcript}
          </MarkdownRenderer>
          {message.response_audio.content && message.response_audio && (
            <Audios audio={[message.response_audio]} />
          )}
        </div>
      )
    }
  } else {
    messageContent = (
      <div className="mt-2">
        <AgentThinkingLoader />
      </div>
    )
  }

  return (
    <div className="flex flex-row items-start gap-4 font-geist">
      <div className="flex-shrink-0" onClick={ open}>
        <Icon type="agent" size="sm" />
        
      </div>
      {messageContent}
    </div>
  )
}

const UserMessage = memo(({ message }: MessageProps) => {
  console.log('message:', message)
  return (
    <div className="flex items-start flex-col gap-4 pt-4 text-start max-md:break-words">
      <div className="flex flex-row gap-x-3">
        <p className="flex items-center gap-x-2 text-sm font-medium text-muted">
          <Icon type="user" size="sm" />
          
        </p>
        <div className="text-md rounded-lg py-1">
          {message.content}
        </div>
      </div>  
      {/* <div className="flex w-full flex-col gap-4"> */}
      <div className="flex justify-start w-1/3 flex-col gap-4">
        {/* <MarkdownRenderer>{message.content}</MarkdownRenderer> */}

        {/* Hiển thị video nếu có */}
        {message.videos && message.videos.length > 0 && (
            <Videos videos={message.videos} />
        )}

        {/* Hiển thị hình ảnh nếu có */}
        {message.images && message.images.length > 0 && (

            <Images images={message.images} />
  
        )}

        {/* Hiển thị âm thanh nếu có */}
        {message.audio && message.audio.length > 0 && (
        
            <Audios audio={message.audio} />
          
        )}
    
      </div>
    </div>
  )
})

AgentMessage.displayName = 'AgentMessage'
UserMessage.displayName = 'UserMessage'
export { AgentMessage, UserMessage }

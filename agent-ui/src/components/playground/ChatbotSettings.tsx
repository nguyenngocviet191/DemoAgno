import { useBotInfo} from '@/store'
import { X } from 'lucide-react'
const ChatbotSettings = () => {
  const close = useBotInfo((s) => s.close);
  return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
        <div className="bg-white w-[400px] rounded-xl shadow-2xl p-6 relative animate-fade-in">
          
          <div className="absolute top-3 right-3 text-gray-500 hover:text-red-500 text-xl" onClick={close}>
           <X className="size-5" />
          </div>
 


          {/* Nội dung setting */}
          <h2 className="text-xl font-semibold mb-2">Agent Settings</h2>
          <p className="text-sm text-gray-600 mb-4">Modify AI bot settings</p>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Agent</label>
            <select className="w-full border px-3 py-2 rounded">
              <option>Research Agent</option>
              <option>Support Agent</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Tools</label>
            <div className="flex flex-wrap gap-2">
              <span className="bg-gray-200 px-2 py-1 rounded text-sm">SEARCH_EXA</span>
              <span className="bg-gray-200 px-2 py-1 rounded text-sm">GET_CONTENTS</span>
              <span className="bg-gray-200 px-2 py-1 rounded text-sm">FIND_SIMILAR</span>
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium">Storage</label>
            <p className="text-sm text-gray-500">PostgresStorage</p>
          </div>

          <div>
            <label className="block text-sm font-medium">Memory</label>
            <p className="text-sm text-gray-500">Empty</p>
          </div>
        </div>
      </div>
    )
 
}

export default ChatbotSettings
'use client'

import Avatar from '@/components/Avartar'
import Endpoint from '@/components/playground/Sidebar/Endpoint'

import { usePlaygroundStore } from '@/store'
import Icon from '@/components/ui/icon'

const AppLogo = () => (
    <div className="flex items-center gap-2">
      <Icon type="agno" size="xs" />
      <span className="text-xs font-medium uppercase text-[var(--color-text)] ">Agent UI</span>
    </div>
  )

const Header = () => {


return (
     <div className="flex flex-row border-b border-border px-3 py-2 gap-5">
                <AppLogo />

                
                <div className="ml-auto flex items-center">
                  <Avatar src="/a6.JPG" size={30} isOnline />
                </div>
              </div>
)
}
export default Header
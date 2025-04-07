'use client'
import type { Metadata } from 'next'
import { DM_Mono, Geist } from 'next/font/google'
import { NuqsAdapter } from 'nuqs/adapters/next/app'
import { Toaster } from '@/components/ui/sonner'
import './globals.css'
import { useThemeStore } from '@/store/themeStore';
import Sidebar from '@/components/playground/Sidebar/Sidebar'
import Header from './Header'
const geistSans = Geist({
  variable: '--font-geist-sans',
  weight: '400',
  subsets: ['latin']
})

const dmMono = DM_Mono({
  subsets: ['latin'],
  variable: '--font-dm-mono',
  weight: '400'
})

// export const metadata: Metadata = {
//   title: 'Agent UI',
//   description:
//     'A modern chat interface for AI agents built with Next.js, Tailwind CSS, and TypeScript. This template provides a ready-to-use UI for interacting with Agno agents.'
// }

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode
}>) {
  const { theme } = useThemeStore();

  return (
    <html lang="en" data-theme={theme}>
    <body className={`${geistSans.variable} ${dmMono.variable} antialiased`}>
      <NuqsAdapter>
        {/* Cố định header */}
        <div className="fixed top-0 left-0 w-full z-10">
          <Header />
        </div>

        <div className="flex flex-row pt-16 h-screen w-full">
          {/* Cố định sidebar */}
          <div className="fixed left-0 top-16 h-full w-64 z-10">
            <Sidebar />
          </div>

          {/* Nội dung chính có thể cuộn */}
          <div className="fixed flex-1 ml-64 p-4">
            {children}
          </div>

          <Toaster />
        </div>
      </NuqsAdapter>
    </body>
  </html>
  )
}

import Image from 'next/image'

interface AvatarProps {
  src: string
  alt?: string
  size?: number
  isOnline?: boolean
}

export default function Avatar({
  src,
  alt = 'Avatar',
  size = 64,
  isOnline = true,
}: AvatarProps) {
  return (
    <div className="relative inline-block">
      <Image
        src={src}
        alt={alt}
        width={size}
        height={size}
        className="rounded-full object-cover border border-gray-300 shadow-sm"
      />
      {isOnline && (
        <span className="absolute bottom-0 right-0 block h-2 w-2 rounded-full bg-green-500" />
      )}
    </div>
  )
}
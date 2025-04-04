import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.push('/chat'); // Chuyển hướng đến trang chat
  }, []);

  return <p>Đang chuyển hướng...</p>;
}
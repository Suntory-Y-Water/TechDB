import { config } from '@/lib/config';
import { BlogResponse } from '../types';

export default async function Home() {
  const response = await fetch(`${config.CONTAINER_API_URL}/blog`, { cache: 'no-store' });
  const data: BlogResponse[] = (await response.json()) as BlogResponse[];

  return (
    <div className='flex min-h-screen flex-col items-center p-24'>
      <h1 className='text-5xl font-bold mb-8'>Blog</h1>
      <div className='grid grid-cols-3 gap-4'>
        {data.map((blog) => (
          <div key={blog.id} className='bg-white p-4 rounded-lg shadow-md'>
            <h2 className='text-xl font-bold'>{blog.title}</h2>
            <p className='text-gray-600'>{blog.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

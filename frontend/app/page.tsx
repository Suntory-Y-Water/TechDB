import * as Counter from '@/features/count';
import Link from 'next/link';
import { Button } from './components/ui/button';

export default function Home() {
  return (
    <div className='flex min-h-screen flex-col items-center  p-24'>
      <h1 className='text-3xl py-4'>Hello Tech DB!</h1>
      <Counter.CountUp />
      <h2 className='text-2xl py-4'>下のボタンを押すとAPI疎通画面に移動します。</h2>
      <Link href='/check'>
        <Button>疎通チェック</Button>
      </Link>
    </div>
  );
}

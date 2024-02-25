'use client';
import { Button } from '@/app/components/ui/button';
import React, { useState } from 'react';

const CountUp = () => {
  const [count, setCount] = useState<number>(0);

  const hendleClick = () => {
    setCount(count + 1);
  };
  return (
    <div>
      <Button onClick={hendleClick}>hey! shadcn!</Button>
      <p className='py-2'>現在のカウント: {count}</p>
    </div>
  );
};

export default CountUp;

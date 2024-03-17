import React from 'react';
import Image from 'next/image';
import HashTag from '@/public/images/hash.svg';
import Link from 'next/link';
import { TagProps } from '@/app/types';

const TagCard = ({ tag }: { tag: TagProps }) => {
  return (
    <div className='rounded-md bg-white p-4 shadow-md'>
      <Link href={`/category/${tag.name}`} key={tag.name} className='flex items-center gap-2'>
        <Image
          src={tag.image ? tag.image : HashTag}
          alt='tags'
          width='40'
          height='40'
          className='rounded-full'
        />
        <p className='text-sm font-semibold'>{tag.name}</p>
      </Link>
    </div>
  );
};

export default TagCard;

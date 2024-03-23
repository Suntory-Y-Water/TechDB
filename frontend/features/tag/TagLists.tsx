import React from 'react';
import Image from 'next/image';
import HashTag from '@/public/images/hash.svg';
import Link from 'next/link';
import { TagProps } from '@/app/types';
import { Button } from '@/app/components/ui/button';
import { tagSearchUrl } from '@/app/constants';

const TagLists = ({ tags }: { tags: TagProps[] }) => {
  return (
    <div className='rounded-md border bg-white p-4 shadow-md'>
      {tags.map((tag) => (
        <Link
          href={`/category/${tag.name}`}
          key={tag.name}
          className='flex items-center gap-2 py-2'
        >
          <Image
            src={tag.image ? tag.image : HashTag}
            alt='tags'
            width='40'
            height='40'
            className='rounded-full'
          />
          <p className='text-sm font-semibold'>{tag.name}</p>
        </Link>
      ))}
      <Link href={tagSearchUrl}>
        <Button variant='secondary' className='w-full'>
          タグを探す
        </Button>
      </Link>
    </div>
  );
};

export default TagLists;

import React from 'react';
import Link from 'next/link';
import SearchIcon from '@/public/icons/search.svg';

const Header = () => {
  return (
    <header className='flex justify-between py-10 bg-white px-24'>
      <Link href='/'>
        <h1 className='text-5xl font-bold'>Tech DB</h1>
      </Link>
      <Link href='/search' className='flex items-center gap-1 hover:text-primary/70'>
        <SearchIcon />
        <p className='font-semibold text-2xl'>タグ検索</p>
      </Link>
    </header>
  );
};

export default Header;

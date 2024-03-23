import Link from 'next/link';
import React from 'react';
import ClockIcon from '@/public/icons/clock.svg';
import GoodIcon from '@/public/icons/heart.svg';
import CalendarIcon from '@/public/icons/calendar-days.svg';
import { formatDistanceToNow, parseISO } from 'date-fns';
import { ja } from 'date-fns/locale';
import Image from 'next/image';
import NoImage from '@/public/images/no-image.png';
import { badgeVariants } from '@/app/components/ui/badge';
import { categoryUrl } from '@/app/constants';
import { ArticleCardProps } from '@/app/types';

const ArticleCard = ({ article }: { article: ArticleCardProps }) => {
  /**
   * @description 日付の差分を計算し、表示形式を決定する
   * @param {string} dateString
   * @return {*}
   */
  const formatDate = (dateString: string) => {
    const date = parseISO(dateString);
    const difference = formatDistanceToNow(date, { addSuffix: true, locale: ja });
    const daysDifference = (new Date().getTime() - date.getTime()) / (1000 * 3600 * 24);
    if (daysDifference < 7) {
      // "◯日前" の形式で返す
      return difference;
    }
    // "yyyy-mm-dd" 形式で返す
    return dateString.split('T')[0];
  };

  return (
    <article className='rounded-md bg-white p-6 shadow-md sm:max-w-[370px]'>
      <div className='flex flex-col justify-between space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0'>
        <div className='space-y-1'>
          <Link href={article.url} target='_blank' rel='noopener'>
            <Image
              src={article.ogpImageUrl ? article.ogpImageUrl : NoImage}
              alt='posts'
              width='320'
              height='168'
              className='rounded-md'
              style={{ width: '100%', height: 'auto' }}
            />
          </Link>
          <h2 className='line-clamp-2 text-base font-semibold'>
            {article.title.length > 40 ? `${article.title.substring(0, 39)}...` : article.title}
          </h2>
          <div className='flex flex-wrap items-center gap-1 py-2 text-sm'>
            {article.tags &&
              article.tags.length > 0 &&
              article.tags.map((tag, index) => (
                <Link
                  key={index}
                  href={`${categoryUrl}/${tag.name}`}
                  className={badgeVariants({ variant: 'outline' })}
                >
                  {tag.name}
                </Link>
              ))}
          </div>
          <div className='flex items-center gap-1 py-1 text-sm text-slate-500'>
            <ClockIcon />
            <p>
              {article.readTime >= 15
                ? 'この記事は15分以上かかります'
                : `この記事は${article.readTime}分で読めます`}
            </p>
          </div>
          <div className='flex flex-wrap gap-4 py-1 text-slate-500'>
            <div className='flex items-center gap-1'>
              <GoodIcon />
              <p>{article.likesCount}</p>
            </div>
            <div className='flex items-center gap-1'>
              <CalendarIcon />
              <p>{formatDate(article.createdAt)}</p>
            </div>
          </div>
        </div>
      </div>
    </article>
  );
};

export default ArticleCard;

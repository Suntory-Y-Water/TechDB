import React from 'react';
import { ArticleCardProps } from '@/app/types';
import ArticleCard from './ArticleCard';

const ArticleList = ({ articles }: { articles: ArticleCardProps[] }) => {
  return (
    <>
      {articles.map((article) => (
        <ArticleCard article={article} key={article.articleId} />
      ))}
    </>
  );
};

export default ArticleList;

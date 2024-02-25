import CountUp from './CountUp';
import { render } from '@testing-library/react';

describe('CountUp コンポーネントのテスト', () => {
  test('初期値が0であること', () => {
    const { getByText } = render(<CountUp />);
    expect(getByText('現在のカウント: 0')).toBeInTheDocument();
  });
});

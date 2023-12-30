import { getMatch } from '../src/utils/stringUtils';

describe('getMatch function', () => {
  it('returns the correct match', () => {
    const input = 'Hello, world!';
    const regex = /Hello, (\w+)/;
    const expected = 'world';

    expect(getMatch(input, regex)).toBe(expected);
  });

  it('returns null when no match is found', () => {
    const input = 'Hello, world!';
    const regex = /Goodbye, (\w+)/;

    expect(getMatch(input, regex)).toBeNull();
  });
});

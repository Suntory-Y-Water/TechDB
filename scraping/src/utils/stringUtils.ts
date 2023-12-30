/**
 *  正規表現にマッチした文字列を取得する
 *
 * @param {string} input
 * @param {RegExp} regex
 * @return {*}  string | null
 */
export function getMatch(input: string, regex: RegExp): string | null {
  const match = input.match(regex);
  return match ? match[1] : null;
}

export function extractField(
  itemHtml: string,
  regex: RegExp,
  fieldTitle: string,
): { title: string; value: string; short: boolean } {
  const value = getMatch(itemHtml, regex) || '';
  return { title: fieldTitle, value: value, short: true };
}

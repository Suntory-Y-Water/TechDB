import { Attachment, writeToSpreadsheet } from './services/spreadsheetUtils';
import { extractField, getMatch } from './utils/stringUtils';

const REGION = '関東';
const REGIONS: { [key: string]: string } = {
  北海道: 'hokkaido',
  東北: 'tohoku',
  関東: 'kanto',
  '甲信越・北陸': 'koshinetsu',
  東海: 'tokai',
  近畿: 'kinki',
  '中国・四国': 'chugoku',
  九州: 'kyushu',
};
const ORIGIN = 'http://www.sej.co.jp';
const NEW_ITEM_DIR = '/products/a/thisweek/area/';
const NEW_ITEM_URL = ORIGIN + NEW_ITEM_DIR;
const QUERY = '/1/l100/';

const SEVEN_COLOR = [
  '#f58220', // セブンオレンジ
  '#00a54f', // セブングリーン
  '#ee1c23', // セブンレッド
];

/**
 * 商品の詳細を抽出する
 * @param {string} itemHtml
 * @return {*}  {Attachment}
 */
function extractItemDetails(itemHtml: string): Attachment {
  const link = getMatch(itemHtml, /<a href="([^"]+)"/) || '';
  const image = getMatch(itemHtml, /data-original="([^"]+)"/) || '';
  const name =
    getMatch(itemHtml, /<div class="item_ttl"><p><a href="[^"]+">([^<]+)<\/a><\/p><\/div>/) || '';

  return {
    title_link: ORIGIN + link,
    thumb_url: image,
    title: name,
    fields: [
      extractField(itemHtml, /<div class="item_price"><p>([^<]+)<\/p><\/div>/, '値段'),
      extractField(itemHtml, /<div class="item_launch"><p>([^<]+)<\/p><\/div>/, '販売時期'),
      extractField(
        itemHtml,
        /<div class="item_region"><p><span>販売地域：<\/span>([^<]+)<\/p><\/div>/,
        '販売地域',
      ),
    ],
  };
}

/**
 * メイン処理
 * @return {*}  {void}
 */
function main(): void {
  const attachments: Attachment[] = [];

  const html = UrlFetchApp.fetch(NEW_ITEM_URL + REGIONS[REGION] + QUERY).getContentText();
  const items = html.match(/<div class="list_inner[^>]*>[\s\S]*?<\/div>\s*<\/div>/g) || [];

  if (!items) {
    return;
  }

  for (let i = 0; i < items.length; ++i) {
    const itemDetails = extractItemDetails(items[i]);
    if (itemDetails) {
      attachments.push({
        color: SEVEN_COLOR[i % SEVEN_COLOR.length],
        ...itemDetails,
      });
    }
  }

  // スプレッドシートに書き込み
  writeToSpreadsheet(attachments);
}

main();

/**
 * LINE連携するリストのデータ
 * @interface Attachment
 */
export interface Attachment {
  color?: string;
  title: string;
  title_link: string;
  thumb_url: string;
  fields: Array<{ title: string; value: string; short: boolean }>;
}

/**
 * スプレッドシートに書き込む
 * @param {Attachment[]} data
 */
export function writeToSpreadsheet(data: Attachment[]): void {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName('シート1'); // スプレッドシートのシート名を適宜設定

  if (!sheet) {
    throw new Error('シートがありません.');
  }

  // 既存のデータをクリア
  sheet.clear();

  // ヘッダーの追加
  sheet.appendRow(['商品名', '値段', '販売時期', '販売地域', 'リンク', '画像URL']);

  // 新しいデータを書き込み
  data.forEach((item) => {
    const row = [
      item.title,
      item.fields.find((f) => f.title === '値段')?.value || '',
      item.fields.find((f) => f.title === '販売時期')?.value || '',
      item.fields.find((f) => f.title === '販売地域')?.value || '',
      item.title_link,
      item.thumb_url,
    ];
    sheet.appendRow(row);
  });
}

import { writeToSpreadsheet, Attachment } from '../src/services/spreadsheetUtils';

const sheetMock = {
  clear: jest.fn(),
  appendRow: jest.fn(),
};

const spreadsheetMock = {
  getSheetByName: jest.fn().mockReturnValue(sheetMock),
};

global.SpreadsheetApp = {
  getActiveSpreadsheet: jest.fn().mockReturnValue(spreadsheetMock),
} as any;

describe('writeToSpreadsheet の確認', () => {
  it('データをスプレッドシートに正しく書き込めること', () => {
    const testData: Attachment[] = [
      {
        title: '商品A',
        title_link: 'http://example.com/productA',
        thumb_url: 'http://example.com/imageA.jpg',
        fields: [
          { title: '値段', value: '1000円', short: true },
          { title: '販売時期', value: '2023年4月', short: true },
          { title: '販売地域', value: '関東', short: true },
        ],
      },
    ];

    // 関数の実行
    writeToSpreadsheet(testData);

    // モック関数が期待通りに呼び出されたことを検証
    expect(sheetMock.clear).toHaveBeenCalled();
    expect(sheetMock.appendRow).toHaveBeenCalledTimes(testData.length + 1);
    expect(sheetMock.appendRow).toHaveBeenCalledWith([
      '商品名',
      '値段',
      '販売時期',
      '販売地域',
      'リンク',
      '画像URL',
    ]);
  });
});

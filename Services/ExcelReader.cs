// reads sheet → List<string[]> using ClosedXML GetFormattedString()

using System.IO;
using ClosedXML.Excel;

namespace Xemplate.Services;

public class ExcelReader
{
    public List<string[]> ReadSheet(string path, string sheetName)
    {
        using var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
        using var workbook = new XLWorkbook(stream);

        if (!workbook.TryGetWorksheet(sheetName, out var sheet))
        {
            throw new InvalidOperationException($"Sheet '{sheetName}' was not found.");
        }

        int lastColumn = sheet.LastColumnUsed()?.ColumnNumber() ?? 0;
        var rows = new List<string[]>();

        foreach (var row in sheet.RowsUsed())
        {
            var values = new string[lastColumn];
            for (int c = 1; c <= lastColumn; c++)
            {
                values[c - 1] = row.Cell(c).GetFormattedString();
            }
            rows.Add(values);
        }

        return rows;
    }
}

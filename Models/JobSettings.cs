namespace Xemplate.Models;

public record PlaceholderMapping(string Placeholder, int ColumnIndex);

public record JobSettings(
    string ExcelPath,
    string SheetName,
    string TemplatePath,
    string DocumentName,
    IReadOnlyList<int> NamingColumns,
    IReadOnlyList<PlaceholderMapping> Mappings,
    bool SaveAsPdf,
    string OutputFolder
);

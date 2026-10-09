using System.Collections.Concurrent;
using System.IO;
using Xemplate.Models;

namespace Xemplate.Services;

public class TemplateJobRunner
{
    private readonly ExcelReader _excel = new();
    private readonly DocumentFiller _filler = new();
    private readonly WordInteropPdfConverter _pdf;

    public TemplateJobRunner(WordInteropPdfConverter pdf)
    {
        _pdf = pdf;
    }

    public async Task RunAsync(JobSettings s, CancellationToken token = default)
{
    var rows = _excel.ReadSheet(s.ExcelPath, s.SheetName);
    Directory.CreateDirectory(s.OutputFolder);

    string work = Path.Combine(Path.GetTempPath(), "Xemplate", Guid.NewGuid().ToString("N"));
    Directory.CreateDirectory(work);

    try
    {
        string date = DateTime.Today.ToString("dd MMMM yyyy");
        int year = DateTime.Today.Year;

        var used = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var jobs = new List<(string[] Row, string FileName)>();

        foreach (var row in rows)
        {
            string name = string.Join(" ", s.NamingColumns.Select(i => Cell(row, i)));
            name = string.Concat(name.Split(Path.GetInvalidFileNameChars()));

            string baseName = $"{name}_{s.DocumentName}_{year}";
            string fileName = baseName + ".docx";
            int n = 2;
            while (!used.Add(fileName))
                fileName = $"{baseName} ({n++}).docx";

            jobs.Add((row, fileName));
        }

        var created = new System.Collections.Concurrent.ConcurrentBag<string>();

        await Parallel.ForEachAsync(jobs,
            new ParallelOptions
            {
                MaxDegreeOfParallelism = Math.Max(1, Environment.ProcessorCount - 1),
                CancellationToken = token
            },
            (job, ct) =>
            {
                var replacements = new List<(string, string)> { ("[DATE]", date) };
                replacements.AddRange(s.Mappings.Select(m => (m.Placeholder, Cell(job.Row, m.ColumnIndex))));

                string workPath = Path.Combine(work, job.FileName);
                _filler.Fill(s.TemplatePath, workPath, replacements);
                created.Add(workPath);
                return ValueTask.CompletedTask;
            });

        var workFiles = created.ToList();
        if (s.SaveAsPdf)
            _pdf.ConvertAndDelete(workFiles, token);

        // Move the finished files into the real output folder
        foreach (string workPath in workFiles)
        {
            string finished = s.SaveAsPdf ? Path.ChangeExtension(workPath, ".pdf") : workPath;
            File.Move(finished, Path.Combine(s.OutputFolder, Path.GetFileName(finished)), overwrite: true);
        }
    }
    finally
    {
        try { Directory.Delete(work, recursive: true); } catch { }
    }
}

    private static string Cell(string[] row, int index) =>
        index < row.Length && !string.IsNullOrWhiteSpace(row[index]) ? row[index] : "N/A";
}

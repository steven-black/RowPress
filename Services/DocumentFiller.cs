// opens template, replaces placeholders (body, tables, headers, footers)

using System.IO;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

namespace Xemplate.Services;

public class DocumentFiller
{
    public void Fill(string templatePath, string outputPath, IEnumerable<(string Placeholder, string Value)> replacements)
    {
        File.Copy(templatePath, outputPath, overwrite: true);

        using var doc = WordprocessingDocument.Open(outputPath, true);
        var main = doc.MainDocumentPart!;

        var paragraphs = main.Document!.Body!.Descendants<Paragraph>().ToList();
        foreach (var header in main.HeaderParts)
            paragraphs.AddRange(header.RootElement!.Descendants<Paragraph>());
        foreach (var footer in main.FooterParts)
            paragraphs.AddRange(footer.RootElement!.Descendants<Paragraph>());

        foreach (var paragraph in paragraphs)
            foreach (var (placeholder, value) in replacements)
                ReplaceInParagraph(paragraph, placeholder, value);
    }

    private static void ReplaceInParagraph(Paragraph paragraph, string placeholder, string replacement)
    {
        int searchFrom = 0;
        while (true)
        {
            var texts = paragraph.Descendants<Text>().ToList();
            string full = string.Concat(texts.Select(t => t.Text));
            int start = full.IndexOf(placeholder, searchFrom, StringComparison.Ordinal);
            if (start < 0) return;

            int end = start + placeholder.Length;
            int pos = 0;
            bool placed = false;

            foreach (var t in texts)
            {
                int tStart = pos;
                int tEnd = pos + t.Text.Length;
                pos = tEnd;
                if (tEnd <= start || tStart >= end) continue;

                int cutFrom = Math.Max(start, tStart) - tStart;
                int cutTo = Math.Min(end, tEnd) - tStart;

                t.Text = t.Text[..cutFrom] + (placed ? "" : replacement) + t.Text[cutTo..];
                t.Space = DocumentFormat.OpenXml.SpaceProcessingModeValues.Preserve;
                placed = true;
            }

            searchFrom = start + replacement.Length;
        }
    }
}
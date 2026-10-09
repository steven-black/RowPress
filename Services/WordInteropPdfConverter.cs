using System.IO;
using System.Runtime.InteropServices;

namespace Xemplate.Services;

public class WordInteropPdfConverter
{
    private const int WdExportFormatPdf = 17;
    private const int WdDoNotSaveChanges = 0;
    private const int WdAlertsNone = 0;

    public void ConvertAndDelete(IReadOnlyList<string> docxPaths, CancellationToken token = default)
    {
        Type? wordType = Type.GetTypeFromProgID("Word.Application");
        if (wordType == null)
            throw new InvalidOperationException("Microsoft Word does not appear to be installed.");

        dynamic? app = null;
        try
        {
            app = Activator.CreateInstance(wordType)!;
            app.Visible = false;
            app.DisplayAlerts = WdAlertsNone;

            foreach (string docxPath in docxPaths)
            {
                token.ThrowIfCancellationRequested();

                dynamic? doc = null;
                try
                {
                    doc = app.Documents.Open(docxPath, false, true);
                    string pdfPath = Path.ChangeExtension(docxPath, ".pdf");
                    doc.ExportAsFixedFormat(pdfPath, WdExportFormatPdf);
                }
                finally
                {
                    if (doc != null)
                    {
                        doc.Close(WdDoNotSaveChanges);
                        Marshal.ReleaseComObject((object)doc);
                    }
                }

                File.Delete(docxPath);
            }
        }
        finally
        {
            if (app != null)
            {
                app.Quit(WdDoNotSaveChanges);
                Marshal.ReleaseComObject((object)app);
            }
        }
    }
}

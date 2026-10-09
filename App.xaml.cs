using System.IO;
using System.Windows;

namespace Xemplate;

public partial class App : Application
{
    public App()
    {
        DispatcherUnhandledException += (s, e) =>
        {
            Report(e.Exception);
            e.Handled = true;
            Shutdown();
        };

        AppDomain.CurrentDomain.UnhandledException += (s, e) =>
            Report(e.ExceptionObject as Exception);
    }

    private static void Report(Exception? ex)
    {
        string text = ex?.ToString() ?? "Unknown error";
        File.WriteAllText(
            Path.Combine(AppContext.BaseDirectory, "crash.log"),
            $"{DateTime.Now}\n{text}");
        MessageBox.Show(text, "Xemplate crashed");
    }
}

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Win32;
using System.Collections.ObjectModel;
using System.IO;
using Xemplate.Helpers;
using Xemplate.Models;
using Xemplate.Services;

namespace Xemplate.ViewModels;

public partial class MainViewModel : ObservableObject
{
    public ObservableCollection<PlaceholderRowViewModel> PlaceholderRows { get; } = new();

    [ObservableProperty]
    private string excelDocumentPath = "";

    [ObservableProperty]
    private string wordDocumentPath = "";

    [ObservableProperty]
    private string outputFolderPath = "";
    

    [ObservableProperty]
    private string outputDocumentName = "";

    [ObservableProperty]
    private string sheetName = "";

    [ObservableProperty]
    private string outputDocumentNamingColumns = "";

    [ObservableProperty]
    private bool saveAsPdf = true;

    [ObservableProperty]
    private string statusText = "";

    [RelayCommand]
    private void BrowseExcel()
    {
        var dialog = new OpenFileDialog
        {
            Title = "Select Excel Workbook",
            Filter = "Excel workbooks (*.xlsx)|*.xlsx"
        };

        if (dialog.ShowDialog() == true)
        {
            ExcelDocumentPath = dialog.FileName;
        }
    }

    [RelayCommand]
    private void BrowseWord()
    {
        var dialog = new OpenFileDialog
        {
            Title = "Select Word Template",
            Filter = "Word documents (*.docx)|*.docx"
        };

        if (dialog.ShowDialog() == true)
        {
            WordDocumentPath = dialog.FileName;
        }
    }

    [RelayCommand]
    private void BrowseFolder()
    {
        var dialog = new OpenFolderDialog
        {
            Title = "Select Output Folder"
        };

        if (dialog.ShowDialog() == true)
        {
            OutputFolderPath = dialog.FolderName;
        }
    }

    [RelayCommand]
    private void AddPlaceholder()
    {
        PlaceholderRows.Add(new PlaceholderRowViewModel(row => PlaceholderRows.Remove(row)));
    }

    [RelayCommand]
    private async Task PropagateAsync()
    {
        if (!File.Exists(ExcelDocumentPath))
        {
            StatusText = "Please select an Excel workbook.";
            return;
        }

        if (!File.Exists(WordDocumentPath))
        {
            StatusText = "Please select a Word template.";
            return;
        }

        if (string.IsNullOrWhiteSpace(OutputFolderPath))
        {
            StatusText = "Please select an output folder.";
            return;
        }
        
        try
        {
            var settings = new JobSettings(
                ExcelDocumentPath,
                SheetName,
                WordDocumentPath,
                OutputDocumentName,
                ColumnLetters.ParseList(OutputDocumentNamingColumns),
                PlaceholderRows
                    .Where(r => r.Placeholder != "" && r.ReplacementColumn != "")
                    .Select(r => new PlaceholderMapping(r.Placeholder, ColumnLetters.ToIndex(r.ReplacementColumn)))
                    .ToList(),
                SaveAsPdf,
                OutputFolderPath
            );

            StatusText = "Working...";
            await Task.Run(() => new TemplateJobRunner(new WordInteropPdfConverter()).RunAsync(settings));
            StatusText = $"Done. Documents saved to {OutputFolderPath}.";
        }
        catch (Exception ex)
        {
            StatusText = $"Error: {ex.Message}";
        }
    }
}

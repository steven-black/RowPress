using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace Xemplate.ViewModels;

public partial class PlaceholderRowViewModel : ObservableObject
{
    private readonly Action<PlaceholderRowViewModel> _remove;

    public PlaceholderRowViewModel(Action<PlaceholderRowViewModel> remove)
    {
        _remove = remove;
    }

    [ObservableProperty]
    private string placeholder = "";

    [ObservableProperty]
    private string replacementColumn = "";

    [RelayCommand]
    private void Remove() => _remove(this);
}

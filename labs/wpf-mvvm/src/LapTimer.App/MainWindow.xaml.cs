using System.Windows;
using LapTimer.Core;

namespace LapTimer.App;

/// <summary>The entire code-behind: hand the window its view model.</summary>
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        DataContext = new LapTimerViewModel(new SystemClock());
    }
}

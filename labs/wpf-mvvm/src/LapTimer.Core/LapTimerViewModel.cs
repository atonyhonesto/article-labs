using System.Collections.ObjectModel;

namespace LapTimer.Core;

public sealed record LapRow(int Lap, TimeSpan Time, bool IsBest)
{
    public string Display => LapTimerViewModel.Format(Time);
}

/// <summary>
/// Everything the window shows and does, with no reference to the window.
/// The view binds to these properties and commands; tests drive them directly.
/// </summary>
public sealed class LapTimerViewModel : ObservableObject
{
    private readonly IClock _clock;
    private TimeSpan _lapStart;
    private bool _isRunning;
    private string _carNumber = "24";
    private TimeSpan? _best;

    public LapTimerViewModel(IClock clock)
    {
        _clock = clock;
        StartCommand = new RelayCommand(Start, () => !IsRunning && IsCarNumberValid);
        LapCommand = new RelayCommand(RecordLap, () => IsRunning);
        StopCommand = new RelayCommand(Stop, () => IsRunning);
    }

    public ObservableCollection<LapRow> Laps { get; } = [];
    public RelayCommand StartCommand { get; }
    public RelayCommand LapCommand { get; }
    public RelayCommand StopCommand { get; }

    public string CarNumber
    {
        get => _carNumber;
        set
        {
            if (Set(ref _carNumber, value))
            {
                OnPropertyChanged(nameof(IsCarNumberValid));
                StartCommand.RaiseCanExecuteChanged();
            }
        }
    }

    public bool IsCarNumberValid => int.TryParse(CarNumber, out var n) && n is >= 1 and <= 99;

    public bool IsRunning
    {
        get => _isRunning;
        private set
        {
            if (Set(ref _isRunning, value))
            {
                StartCommand.RaiseCanExecuteChanged();
                LapCommand.RaiseCanExecuteChanged();
                StopCommand.RaiseCanExecuteChanged();
                OnPropertyChanged(nameof(Status));
            }
        }
    }

    public string BestLap => _best is { } b ? Format(b) : "--:--.---";

    public string Status => IsRunning ? $"Car {CarNumber} on track" : $"Car {CarNumber} in the pits";

    private void Start()
    {
        _lapStart = _clock.Now;
        IsRunning = true;
    }

    private void RecordLap()
    {
        var now = _clock.Now;
        var time = now - _lapStart;
        _lapStart = now;
        var isBest = _best is null || time < _best;
        if (isBest)
        {
            _best = time;
            for (var i = 0; i < Laps.Count; i++) Laps[i] = Laps[i] with { IsBest = false };
            OnPropertyChanged(nameof(BestLap));
        }
        Laps.Add(new LapRow(Laps.Count + 1, time, isBest));
    }

    private void Stop() => IsRunning = false;

    public static string Format(TimeSpan t) => $"{(int)t.TotalMinutes}:{t.Seconds:00}.{t.Milliseconds:000}";
}

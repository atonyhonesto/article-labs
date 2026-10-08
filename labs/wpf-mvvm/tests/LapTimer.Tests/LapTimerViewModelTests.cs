using System.ComponentModel;
using LapTimer.Core;

namespace LapTimer.Tests;

/// <summary>No window, no dispatcher, no sleeps: the view model is just a class.</summary>
public class LapTimerViewModelTests
{
    private sealed class FakeClock : IClock
    {
        public TimeSpan Now { get; set; }
    }

    private readonly FakeClock _clock = new();
    private readonly LapTimerViewModel _vm;

    public LapTimerViewModelTests() => _vm = new LapTimerViewModel(_clock);

    private void Lap(double seconds)
    {
        _clock.Now += TimeSpan.FromSeconds(seconds);
        _vm.LapCommand.Execute(null);
    }

    [Fact]
    public void Commands_follow_running_state()
    {
        Assert.True(_vm.StartCommand.CanExecute(null));
        Assert.False(_vm.LapCommand.CanExecute(null));
        _vm.StartCommand.Execute(null);
        Assert.False(_vm.StartCommand.CanExecute(null));
        Assert.True(_vm.LapCommand.CanExecute(null));
        _vm.StopCommand.Execute(null);
        Assert.False(_vm.LapCommand.CanExecute(null));
    }

    [Fact]
    public void Records_laps_and_tracks_best()
    {
        _vm.StartCommand.Execute(null);
        Lap(41.250);
        Lap(40.875);
        Lap(41.900);
        Assert.Equal(3, _vm.Laps.Count);
        Assert.Equal("0:40.875", _vm.BestLap);
        Assert.Equal(new[] { false, true, false }, _vm.Laps.Select(l => l.IsBest).ToArray());
    }

    [Fact]
    public void Invalid_car_number_disables_start_and_notifies()
    {
        var changed = new List<string?>();
        var startChanged = 0;
        ((INotifyPropertyChanged)_vm).PropertyChanged += (_, e) => changed.Add(e.PropertyName);
        _vm.StartCommand.CanExecuteChanged += (_, _) => startChanged++;

        _vm.CarNumber = "150";

        Assert.False(_vm.StartCommand.CanExecute(null));
        Assert.Contains(nameof(LapTimerViewModel.CarNumber), changed);
        Assert.Contains(nameof(LapTimerViewModel.IsCarNumberValid), changed);
        Assert.Equal(1, startChanged);
    }

    [Fact]
    public void Status_text_follows_state()
    {
        Assert.Equal("Car 24 in the pits", _vm.Status);
        _vm.StartCommand.Execute(null);
        Assert.Equal("Car 24 on track", _vm.Status);
    }

    [Theory]
    [InlineData(83.456, "1:23.456")]
    [InlineData(9.005, "0:09.005")]
    public void Formats_lap_times(double seconds, string expected) =>
        Assert.Equal(expected, LapTimerViewModel.Format(TimeSpan.FromMilliseconds(Math.Round(seconds * 1000))));
}

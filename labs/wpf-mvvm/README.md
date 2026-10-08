<sub>[← all labs](../../README.md)</sub>

# WPF the MVVM way

> If the logic lives in the view model, you can test the app without opening a window.

`C#` · `.NET 10` · `WPF` · `MVVM` · `xUnit`

**Companion to:**
- [Windows Desktop Applications with WPF](https://www.linkedin.com/pulse/windows-desktop-applications-wpf-tony-honesto-h0kmc/)

## What it shows

- A view model with `INotifyPropertyChanged` properties and `ICommand` commands, in a plain `net10.0` library.
- A WPF window with zero event handlers: every button and field is a binding.
- Command availability that follows state (`CanExecute`), and an injected clock so tests never sleep.
- Built on a Windows runner (WPF needs Windows); the view-model tests would run anywhere.

## Run it

```bash
bash labs/wpf-mvvm/ci.sh          # on Windows
dotnet run --project src/LapTimer.App
```

Real output (from this lab's CI run):

```text
Build succeeded.
    0 Warning(s)
    0 Error(s)

Time Elapsed 00:00:15.93
Test run for D:\a\article-labs\article-labs\labs\wpf-mvvm\tests\LapTimer.Tests\bin\Release\net10.0\LapTimer.Tests.dll (.NETCoreApp,Version=v10.0)
A total of 1 test files matched the specified pattern.
[xUnit.net 00:00:00.00] xUnit.net VSTest Adapter v2.8.2+699d445a1a (64-bit .NET 10.0.12)
[xUnit.net 00:00:00.11]   Discovering: LapTimer.Tests
[xUnit.net 00:00:00.20]   Discovered:  LapTimer.Tests
[xUnit.net 00:00:00.20]   Starting:    LapTimer.Tests
[xUnit.net 00:00:00.28]   Finished:    LapTimer.Tests
  Passed LapTimer.Tests.LapTimerViewModelTests.Formats_lap_times(seconds: 83.456000000000003, expected: "1:23.456") [4 ms]
  Passed LapTimer.Tests.LapTimerViewModelTests.Formats_lap_times(seconds: 9.0050000000000008, expected: "0:09.005") [< 1 ms]
  Passed LapTimer.Tests.LapTimerViewModelTests.Status_text_follows_state [1 ms]
  Passed LapTimer.Tests.LapTimerViewModelTests.Records_laps_and_tracks_best [7 ms]
  Passed LapTimer.Tests.LapTimerViewModelTests.Commands_follow_running_state [< 1 ms]
  Passed LapTimer.Tests.LapTimerViewModelTests.Invalid_car_number_disables_start_and_notifies [3 ms]

Test Run Successful.
Total tests: 6
     Passed: 6
 Total time: 0.9942 Seconds
```

## What's in here

| File | Purpose |
|---|---|
| `src/LapTimer.Core/` | View model, ObservableObject, RelayCommand, IClock |
| `src/LapTimer.App/` | WPF window, bindings and the real clock |
| `tests/LapTimer.Tests/` | xUnit tests for the view model |
| `WpfMvvm.slnx` | Solution file |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Hand-written base classes | CommunityToolkit.Mvvm source generators (`[ObservableProperty]`, `[RelayCommand]`) |
| `new` in code-behind | Dependency injection with Microsoft.Extensions.Hosting |
| One window | Navigation, dialogs and services behind interfaces |

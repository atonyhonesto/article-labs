using System.Diagnostics;
using LapTimer.Core;

namespace LapTimer.App;

/// <summary>The real clock; tests use a fake one.</summary>
public sealed class SystemClock : IClock
{
    private readonly Stopwatch _watch = Stopwatch.StartNew();
    public TimeSpan Now => _watch.Elapsed;
}

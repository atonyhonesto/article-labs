namespace LapTimer.Core;

/// <summary>Injected so tests control time instead of sleeping.</summary>
public interface IClock
{
    TimeSpan Now { get; }
}

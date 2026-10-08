package dev.honesto.standards;

import java.time.Duration;
import java.util.List;
import java.util.Objects;
import java.util.OptionalDouble;

/** Lap-time helpers written to pass the quality gate. */
public final class LapTimes {

    private static final long MILLIS_PER_MINUTE = 60_000L;
    private static final long MILLIS_PER_SECOND = 1_000L;
    private static final double PIT_LOSS_SECONDS = 22.5;

    private LapTimes() {
    }

    /**
     * Formats a lap as m:ss.SSS.
     *
     * @param lap lap duration, not negative
     * @return formatted lap time
     */
    public static String format(Duration lap) {
        Objects.requireNonNull(lap, "lap");
        if (lap.isNegative()) {
            throw new IllegalArgumentException("lap time cannot be negative: " + lap);
        }
        long ms = lap.toMillis();
        return String.format("%d:%02d.%03d", ms / MILLIS_PER_MINUTE,
                (ms % MILLIS_PER_MINUTE) / MILLIS_PER_SECOND, ms % MILLIS_PER_SECOND);
    }

    /**
     * Mean of the laps that are not outliers (in/out laps, yellows).
     *
     * @param lapsSeconds lap times in seconds
     * @param tolerance   fraction above the best lap still counted as representative
     * @return representative pace, empty if there are no laps
     */
    public static OptionalDouble representativePace(List<Double> lapsSeconds, double tolerance) {
        if (lapsSeconds.isEmpty()) {
            return OptionalDouble.empty();
        }
        double best = lapsSeconds.stream().mapToDouble(Double::doubleValue).min().orElseThrow();
        return lapsSeconds.stream()
                .mapToDouble(Double::doubleValue)
                .filter(t -> t <= best * (1 + tolerance))
                .average();
    }

    /**
     * Laps a stop pays back on fresher tyres.
     *
     * @param gainPerLapSeconds pace advantage of new tyres
     * @return laps needed to recover the time lost in the pit lane
     */
    public static int lapsToRecoverStop(double gainPerLapSeconds) {
        if (gainPerLapSeconds <= 0) {
            throw new IllegalArgumentException("a stop with no pace gain never pays back");
        }
        return (int) Math.ceil(PIT_LOSS_SECONDS / gainPerLapSeconds);
    }
}

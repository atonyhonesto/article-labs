package dev.honesto.standards;

import java.time.Duration;
import java.util.List;
import java.util.logging.Logger;

/** Entry point for the lab demo: uses a logger, as the rules require. */
public final class Demo {

    private static final Logger LOG = Logger.getLogger(Demo.class.getName());
    private static final long SAMPLE_LAP_MS = 83_456L;
    private static final double TOLERANCE = 0.03;
    private static final double TYRE_GAIN = 0.9;
    private static final List<Double> STINT = List.of(83.9, 83.5, 84.1, 97.2, 83.7, 110.4);

    private Demo() {
    }

    /**
     * Runs the demo.
     *
     * @param args unused
     */
    public static void main(String[] args) {
        System.setProperty("java.util.logging.SimpleFormatter.format", "%5$s%n");
        LOG.info(() -> "Best lap formatted: " + LapTimes.format(Duration.ofMillis(SAMPLE_LAP_MS)));
        LOG.info(() -> String.format("Representative pace (in/out laps dropped): %.3f s",
                LapTimes.representativePace(STINT, TOLERANCE).orElseThrow()));
        LOG.info(() -> "Laps to pay back a stop at 0.9 s/lap: " + LapTimes.lapsToRecoverStop(TYRE_GAIN));
    }
}

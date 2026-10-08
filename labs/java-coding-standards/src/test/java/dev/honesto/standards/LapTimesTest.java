package dev.honesto.standards;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.List;
import org.junit.jupiter.api.Test;

class LapTimesTest {

    @Test
    void formatsMinutesSecondsMillis() {
        assertEquals("1:23.456", LapTimes.format(Duration.ofMillis(83_456)));
        assertEquals("0:09.005", LapTimes.format(Duration.ofMillis(9_005)));
    }

    @Test
    void rejectsNegativeLap() {
        assertThrows(IllegalArgumentException.class, () -> LapTimes.format(Duration.ofMillis(-1)));
    }

    @Test
    void representativePaceDropsOutliers() {
        double pace = LapTimes.representativePace(List.of(80.0, 81.0, 95.0), 0.03).orElseThrow();
        assertEquals(80.5, pace, 1e-9);
        assertTrue(LapTimes.representativePace(List.of(), 0.03).isEmpty());
    }

    @Test
    void pitStopPayback() {
        assertEquals(25, LapTimes.lapsToRecoverStop(0.9));
        assertThrows(IllegalArgumentException.class, () -> LapTimes.lapsToRecoverStop(0));
    }
}

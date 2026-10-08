package dev.honesto.standards;

import java.util.*;

// Deliberately breaks the rules. ci.sh drops it into a copy of the project to prove the gate fails.
public class BadExample {
    public int count;

    public static String status(String flag, int laps) {
        if (flag == "GREEN") return "racing";
        try {
            Thread.sleep(250);
        } catch (InterruptedException e) {
        }
        switch (laps) {
            case 0:
                System.out.println("not started");
            case 1:
                return "first lap";
        }
        List<String> unused = new ArrayList<>();
        return laps > 57 ? "finished" : "running";
    }
}

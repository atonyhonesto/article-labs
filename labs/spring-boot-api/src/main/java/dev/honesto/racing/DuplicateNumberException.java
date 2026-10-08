package dev.honesto.racing;

public class DuplicateNumberException extends RuntimeException {

    public DuplicateNumberException(int number) {
        super("Car number " + number + " is already entered");
    }
}

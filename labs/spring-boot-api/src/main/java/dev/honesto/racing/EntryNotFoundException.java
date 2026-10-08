package dev.honesto.racing;

public class EntryNotFoundException extends RuntimeException {

    public EntryNotFoundException(long id) {
        super("No entry with id " + id);
    }
}

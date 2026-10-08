package dev.honesto.racing;

/** A car entered in the race. Records give immutable DTOs with no boilerplate. */
public record Entry(long id, int number, String driver, String team) {
}

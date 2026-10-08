package dev.honesto.racing;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** What a client sends. Validation runs before the controller method is called. */
public record EntryRequest(
        @Min(value = 1, message = "car number must be 1-99") @Max(value = 99, message = "car number must be 1-99") int number,
        @NotBlank(message = "driver is required") @Size(max = 60) String driver,
        @NotBlank(message = "team is required") String team) {
}

package dev.honesto.racing;

import jakarta.validation.Valid;
import java.net.URI;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/entries")
public class EntryController {

    private final EntryService service;

    public EntryController(EntryService service) {     // constructor injection: no @Autowired needed
        this.service = service;
    }

    @GetMapping
    public List<Entry> all() {
        return service.all();
    }

    @GetMapping("/{id}")
    public Entry one(@PathVariable long id) {
        return service.get(id);
    }

    @PostMapping
    public ResponseEntity<Entry> create(@Valid @RequestBody EntryRequest request) {
        Entry e = service.create(request);
        return ResponseEntity.created(URI.create("/api/entries/" + e.id())).body(e);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}

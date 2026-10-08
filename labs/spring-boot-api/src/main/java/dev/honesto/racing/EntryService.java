package dev.honesto.racing;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Service;

/** Business rules live here, not in the controller. Swap the map for a Spring Data repository later. */
@Service
public class EntryService {

    private final Map<Long, Entry> entries = new ConcurrentHashMap<>();
    private final AtomicLong ids = new AtomicLong();

    public List<Entry> all() {
        return entries.values().stream().sorted(Comparator.comparingInt(Entry::number)).toList();
    }

    public Entry get(long id) {
        Entry e = entries.get(id);
        if (e == null) {
            throw new EntryNotFoundException(id);
        }
        return e;
    }

    public synchronized Entry create(EntryRequest req) {
        if (entries.values().stream().anyMatch(e -> e.number() == req.number())) {
            throw new DuplicateNumberException(req.number());
        }
        Entry e = new Entry(ids.incrementAndGet(), req.number(), req.driver().trim(), req.team().trim());
        entries.put(e.id(), e);
        return e;
    }

    public void delete(long id) {
        if (entries.remove(id) == null) {
            throw new EntryNotFoundException(id);
        }
    }
}

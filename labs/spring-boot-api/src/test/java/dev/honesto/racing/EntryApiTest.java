package dev.honesto.racing;

import static org.hamcrest.Matchers.endsWith;
import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class EntryApiTest {

    @Autowired
    MockMvc mvc;

    ResultActions postEntry(String json) throws Exception {
        return mvc.perform(post("/api/entries").contentType(MediaType.APPLICATION_JSON).content(json));
    }

    @Test
    void createThenRead() throws Exception {
        postEntry("{\"number\":24,\"driver\":\"A. Driver\",\"team\":\"Team Green\"}")
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", endsWith("/api/entries/1")))
                .andExpect(jsonPath("$.number").value(24));
        mvc.perform(get("/api/entries/1")).andExpect(status().isOk()).andExpect(jsonPath("$.team").value("Team Green"));
        mvc.perform(get("/api/entries")).andExpect(jsonPath("$", hasSize(1)));
    }

    @Test
    void validationErrorsAreProblemDetails() throws Exception {
        postEntry("{\"number\":150,\"driver\":\"\",\"team\":\"X\"}")
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errors.number").value("car number must be 1-99"))
                .andExpect(jsonPath("$.errors.driver").value("driver is required"));
    }

    @Test
    void duplicateNumberIsConflict() throws Exception {
        postEntry("{\"number\":5,\"driver\":\"One\",\"team\":\"T\"}").andExpect(status().isCreated());
        postEntry("{\"number\":5,\"driver\":\"Two\",\"team\":\"T\"}").andExpect(status().isConflict());
    }

    @Test
    void missingEntryIs404() throws Exception {
        mvc.perform(get("/api/entries/99"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.detail").value("No entry with id 99"));
        mvc.perform(delete("/api/entries/99")).andExpect(status().isNotFound());
    }

    @Test
    void healthEndpoint() throws Exception {
        mvc.perform(get("/actuator/health")).andExpect(status().isOk()).andExpect(jsonPath("$.status").value("UP"));
    }
}

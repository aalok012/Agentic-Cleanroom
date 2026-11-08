package com.cleanroom.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;

@SpringBootTest
@AutoConfigureMockMvc
public class Feature3_1Test {
    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testEditEventDetailsAndRegistrationWithValidInputs() throws Exception {
        String json = "{\"event_id\":\"evt-123\",\"details\":{\"title\":\"Updated Title\",\"date\":\"2023-10-15\"},\"registration_requirements\":{\"max_participants\":50,\"fee\":25}}";
        mockMvc.perform(post("/edit-event-details-and-registration")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json))
                .andExpect(status().isOk());
    }

    @Test
    public void testEditEventDetailsWithEmptyRegistrationRequirements() throws Exception {
        String json = "{\"event_id\":\"evt-123\",\"details\":{\"title\":\"Updated Title\",\"date\":\"2023-10-15\"},\"registration_requirements\":{}}";
        mockMvc.perform(post("/edit-event-details-and-registration")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json))
                .andExpect(status().isOk());
    }

    @Test
    public void testEditEventDetailsWithMinimalRegistrationRequirements() throws Exception {
        String json = "{\"event_id\":\"evt-123\",\"details\":{\"title\":\"Updated Title\",\"date\":\"2023-10-15\"},\"registration_requirements\":{\"max_participants\":1}}";
        mockMvc.perform(post("/edit-event-details-and-registration")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json))
                .andExpect(status().isOk());
    }

    @Test
    public void testEditNonExistentEvent() throws Exception {
        String json = "{\"event_id\":\"evt-nonexistent\",\"details\":{\"title\":\"Title\",\"date\":\"2023-10-15\"},\"registration_requirements\":{\"max_participants\":50,\"fee\":25}}";
        mockMvc.perform(post("/edit-event-details-and-registration")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json))
                .andExpect(status().isBadRequest());
    }
}

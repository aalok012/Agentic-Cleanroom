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
public class Feature3_2Test {
    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testRegisterForEventNotLoggedIn() throws Exception {
        mockMvc.perform(post("/events/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{}"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    public void testRegisterForEventLoggedIn() throws Exception {
        mockMvc.perform(post("/events/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"user_id\": 123}"))
                .andExpect(status().isOk());
    }

    @Test
    public void testRegisterForNonExistentEvent() throws Exception {
        mockMvc.perform(post("/events/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"user_id\": 123, \"event_id\": 999}"))
                .andExpect(status().isNotFound());
    }

    @Test
    public void testRegisterForPassedEvent() throws Exception {
        mockMvc.perform(post("/events/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"user_id\": 123, \"event_id\": 456}"))
                .andExpect(status().isBadRequest());
    }
}

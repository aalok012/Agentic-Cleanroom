package com.cleanroom.app.gen.g3_2_REQ_1;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.server.ResponseStatusException;

public class PromptUserToLogInController {
    private static final Map<String, Object> loggedInUsers = new ConcurrentHashMap<>();

    @PostMapping("/controllers/prompt_user_to_log_in")
    public ResponseEntity<?> promptUserToLogIn(@RequestBody Map<String, Object> body) {
        // Check if user is logged in
        if (loggedInUsers.containsKey("current_user")) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "User is already logged in");
        }
        
        // Return null as per specification
        return ResponseEntity.ok().build();
    }
}

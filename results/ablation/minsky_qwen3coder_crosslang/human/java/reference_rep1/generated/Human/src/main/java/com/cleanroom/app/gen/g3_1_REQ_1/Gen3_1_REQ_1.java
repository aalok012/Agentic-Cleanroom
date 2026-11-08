package com.cleanroom.app.gen.g3_1_REQ_1;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.math.BigInteger;
import java.util.HashMap;
import java.util.Map;

class F3_1Adapter {
    private static Object model = F3__1Domain.__default.Init();

    @PostMapping("/controllers/edit_event_details_and_registration")
    public Map<String, Object> edit_event_details_and_registration(@RequestBody Map<String, Object> body) {
        // Extract event_id, details, and registration_requirements from the request body
        String eventId = (String) body.get("event_id");
        Map<String, String> details = (Map<String, String>) body.get("details");
        Map<String, String> registrationRequirements = (Map<String, String>) body.get("registration_requirements");

        // Convert Java Maps to Dafny Maps
        dafny.DafnyMap<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>> dafnyDetails = convertToDafnyMap(details);
        dafny.DafnyMap<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>> dafnyRegistrationRequirements = convertToDafnyMap(registrationRequirements);

        // Create the Action
        F3__1Domain.Action action = F3__1Domain.Action.create_EditEventDetails(dafnyDetails, dafnyRegistrationRequirements);

        // Apply the action to the model
        Object newState = F3__1Domain.__default.Apply((F3__1Domain.Model) model, action);
        model = F3__1Domain.__default.Normalize((F3__1Domain.Model) newState);

        // Marshal the result back to a JSON-serializable map
        F3__1Domain.Model normalizedModel = (F3__1Domain.Model) model;
        Map<String, Object> response = new HashMap<>();
        response.put("event_id", normalizedModel.dtor_0().verbatimString());
        response.put("details", convertFromDafnyMap(normalizedModel.dtor_1()));
        response.put("registration_requirements", convertFromDafnyMap(normalizedModel.dtor_2()));

        return response;
    }

    private dafny.DafnyMap<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>> convertToDafnyMap(Map<String, String> javaMap) {
        dafny.DafnyMap<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>> dafnyMap = dafny.DafnyMap.of();
        for (Map.Entry<String, String> entry : javaMap.entrySet()) {
            dafny.DafnySequence<? extends dafny.CodePoint> key = dafny.DafnySequence.asUnicodeString(entry.getKey());
            dafny.DafnySequence<? extends dafny.CodePoint> value = dafny.DafnySequence.asUnicodeString(entry.getValue());
            dafnyMap = dafnyMap.put(key, value);
        }
        return dafnyMap;
    }

    private Map<String, String> convertFromDafnyMap(dafny.DafnyMap<dafny.DafnySequence<? extends dafny.CodePoint>, dafny.DafnySequence<? extends dafny.CodePoint>> dafnyMap) {
        Map<String, String> javaMap = new HashMap<>();
        for (dafny.DafnySequence<? extends dafny.CodePoint> key : dafnyMap.keySet().Elements()) {
            dafny.DafnySequence<? extends dafny.CodePoint> value = dafnyMap.get(key);
            javaMap.put(key.verbatimString(), value.verbatimString());
        }
        return javaMap;
    }
}

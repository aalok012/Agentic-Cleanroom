package com.cleanroom.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Application entry point — generated mechanically by the pipeline's Spring packager.
 * {@code @SpringBootApplication} component-scans com.cleanroom.app, so every generated
 * {@code @RestController} under com.cleanroom.app.gen is auto-registered. No business logic lives here.
 *
 * Run with:  mvn spring-boot:run
 */
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

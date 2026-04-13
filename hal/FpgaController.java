package com.kryptur.hal;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

@SpringBootApplication
@RestController
@RequestMapping("/fpga")
public class FpgaController {

    @GetMapping("/status")
    public String getStatus() {
        return "{\"fpga\":\"online\",\"temperature\":45.2}";
    }

    public static void main(String[] args) {
        SpringApplication.run(FpgaController.class, args);
    }
}

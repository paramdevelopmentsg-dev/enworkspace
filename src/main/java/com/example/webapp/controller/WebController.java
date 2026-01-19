package com.example.webapp.controller;

import com.example.webapp.service.BackendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class WebController {

    @Autowired
    private BackendService backendService;

    @GetMapping("/")
    public String index(Model model) {
        // Add data to model for initial page load
        model.addAttribute("title", "Spring Boot Web Application");
        model.addAttribute("message", "Welcome to the Spring Boot Web Application with REST API Backend");
        return "index";
    }

    @GetMapping("/dashboard")
    public String dashboard() {
        return "dashboard";
    }
}

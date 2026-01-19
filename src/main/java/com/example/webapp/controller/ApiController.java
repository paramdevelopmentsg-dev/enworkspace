package com.example.webapp.controller;

import com.example.webapp.model.DataModel;
import com.example.webapp.service.BackendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class ApiController {

    @Autowired
    private BackendService backendService;

    @GetMapping("/data")
    public ResponseEntity<List<DataModel>> getAllData() {
        try {
            List<DataModel> data = backendService.getAllData();
            return ResponseEntity.ok(data);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/data/{id}")
    public ResponseEntity<DataModel> getDataById(@PathVariable Long id) {
        DataModel data = backendService.getDataById(id);
        return data != null ? ResponseEntity.ok(data) : ResponseEntity.notFound().build();
    }

}

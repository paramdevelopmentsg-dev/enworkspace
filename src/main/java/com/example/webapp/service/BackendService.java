package com.example.webapp.service;

import com.example.webapp.model.DataModel;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.Arrays;
import java.util.List;

@Service
public class BackendService {

    private final WebClient webClient;
    
    @Value("${backend.api.base-url:https://jsonplaceholder.typicode.com}")
    private String baseUrl;

    public BackendService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }

    /**
     * Fetch all data from backend REST API
     */
    public List<DataModel> getAllData() {
        try {
            return webClient.get()
                    .uri(baseUrl + "/posts")
                    .retrieve()
                    .bodyToFlux(DataModel.class)
                    .collectList()
                    .timeout(Duration.ofSeconds(10))
                    .block();
        } catch (Exception e) {
            // Return mock data if external API is not available
            return getMockData();
        }
    }

    /**
     * Fetch single data item by ID from backend REST API
     */
    public DataModel getDataById(Long id) {
        try {
            return webClient.get()
                    .uri(baseUrl + "/posts/" + id)
                    .retrieve()
                    .bodyToMono(DataModel.class)
                    .timeout(Duration.ofSeconds(5))
                    .block();
        } catch (Exception e) {
            // Return mock data if external API is not available
            return new DataModel(id, "Sample Item " + id, "Sample description for item " + id, "active");
        }
    }

    private List<DataModel> getMockData() {
        return Arrays.asList(
                new DataModel(1L, "Sample Item 1", "This is a sample data item from mock backend", "active"),
                new DataModel(2L, "Sample Item 2", "Another sample data item for demonstration", "inactive"),
                new DataModel(3L, "Sample Item 3", "Third sample item with different status", "pending")
        );
    }
}

// JavaScript for Spring Boot Web Application frontend

document.addEventListener('DOMContentLoaded', function() {
    setupEventHandlers();
});

function setupEventHandlers() {
    const loadButton = document.getElementById('loadDataBtn');
    const itemButton = document.getElementById('loadItemBtn');
    
    if (loadButton) {
        loadButton.addEventListener('click', fetchAllData);
    }
    
    if (itemButton) {
        itemButton.addEventListener('click', fetchSingleItem);
    }
}

async function fetchAllData() {
    const spinner = document.getElementById('loading');
    const container = document.getElementById('dataContainer');
    const button = document.getElementById('loadDataBtn');
    
    showLoading(spinner, button);
    container.innerHTML = '';
    
    try {
        const response = await fetch('/api/data');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const items = await response.json();
        renderDataItems(items, container);
        
    } catch (error) {
        console.error('Fetch error:', error);
        container.innerHTML = createErrorMessage('Unable to load data from backend');
    } finally {
        hideLoading(spinner, button);
    }
}

async function fetchSingleItem() {
    const idInput = document.getElementById('itemId');
    const container = document.getElementById('itemContainer');
    const itemId = idInput.value;
    
    if (!itemId) {
        alert('Please enter a valid item ID');
        return;
    }
    
    try {
        const response = await fetch('/api/data/' + itemId);
        if (!response.ok) {
            throw new Error('Item not found');
        }
        
        const item = await response.json();
        renderDataItems([item], container);
        
    } catch (error) {
        console.error('Fetch error:', error);
        container.innerHTML = createErrorMessage('Item with ID ' + itemId + ' not found');
    }
}

function renderDataItems(items, container) {
    if (!items || items.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No items found</div>';
        return;
    }
    
    const itemsHtml = items.slice(0, 10).map(item => 
        '<div class="data-item">' +
        '<h6>ID: ' + (item.id || 'Unknown') + '</h6>' +
        '<p><strong>Title:</strong> ' + (item.title || item.name || 'No title available') + '</p>' +
        '<p><strong>Description:</strong> ' + (item.body || item.description || 'No description available') + '</p>' +
        '<span class="badge bg-success status-badge">' + (item.status || 'active') + '</span>' +
        '</div>'
    ).join('');
    
    container.innerHTML = itemsHtml;
    
    if (items.length > 10) {
        container.innerHTML += '<div class="alert alert-info mt-2">Displaying first 10 of ' + items.length + ' total items</div>';
    }
}

function showLoading(spinner, button) {
    spinner.style.display = 'block';
    button.disabled = true;
}

function hideLoading(spinner, button) {
    spinner.style.display = 'none';
    button.disabled = false;
}

function createErrorMessage(message) {
    return '<div class="alert alert-danger"><strong>Error:</strong> ' + message + '</div>';
}

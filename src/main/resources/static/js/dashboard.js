// Dashboard specific JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    setupDashboard();
    loadDashboardData();
});

function setupDashboard() {
    const refreshButton = document.getElementById('refreshBtn');
    if (refreshButton) {
        refreshButton.addEventListener('click', loadDashboardData);
    }
}

async function loadDashboardData() {
    const loadingDiv = document.getElementById('dashboardLoading');
    const dataDiv = document.getElementById('dashboardData');
    const refreshBtn = document.getElementById('refreshBtn');
    
    loadingDiv.style.display = 'block';
    refreshBtn.disabled = true;
    dataDiv.innerHTML = '';
    
    try {
        const response = await fetch('/api/data');
        if (!response.ok) {
            throw new Error('Failed to fetch dashboard data');
        }
        
        const data = await response.json();
        renderDashboardTable(data, dataDiv);
        
    } catch (error) {
        console.error('Dashboard error:', error);
        dataDiv.innerHTML = '<div class="alert alert-danger">Failed to load dashboard data</div>';
    } finally {
        loadingDiv.style.display = 'none';
        refreshBtn.disabled = false;
    }
}

function renderDashboardTable(items, container) {
    const tableHtml = '<div class="table-responsive"><table class="table table-striped"><thead><tr><th>ID</th><th>Title</th><th>Status</th></tr></thead><tbody>' +
        items.slice(0, 20).map(item => '<tr><td>' + (item.id || 'N/A') + '</td><td>' + (item.title || item.name || 'No title') + '</td><td><span class="badge bg-primary">' + (item.status || 'active') + '</span></td></tr>').join('') +
        '</tbody></table></div>';
    
    container.innerHTML = tableHtml;
}

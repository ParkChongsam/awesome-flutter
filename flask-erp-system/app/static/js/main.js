/**
 * Main JavaScript for Flask ERP System
 * 참좋은복사기 (Very Good Copy Machine) Company
 */

// Initialize when document is ready
$(document).ready(function() {
    console.log('Flask ERP System initialized');

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Confirm delete actions
    $('.btn-delete, .delete-btn').on('click', function(e) {
        if (!confirm('정말 삭제하시겠습니까? (Are you sure you want to delete this?)')) {
            e.preventDefault();
            return false;
        }
    });

    // Format currency inputs
    $('input[type="currency"]').on('blur', function() {
        var value = parseFloat($(this).val());
        if (!isNaN(value)) {
            $(this).val(value.toFixed(2));
        }
    });

    // Format number inputs with thousand separators
    $('.format-number').each(function() {
        var value = $(this).text();
        var formatted = Number(value).toLocaleString('ko-KR');
        $(this).text(formatted);
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Data table search filter
    $('#searchInput').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $('#dataTable tbody tr').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Print functionality
    $('.btn-print').on('click', function() {
        window.print();
    });

    // Export to CSV
    $('.btn-export-csv').on('click', function() {
        var table = $(this).closest('.card').find('table');
        var csv = [];

        // Get headers
        var headers = [];
        table.find('thead th').each(function() {
            headers.push($(this).text().trim());
        });
        csv.push(headers.join(','));

        // Get rows
        table.find('tbody tr').each(function() {
            var row = [];
            $(this).find('td').each(function() {
                row.push('"' + $(this).text().trim().replace(/"/g, '""') + '"');
            });
            csv.push(row.join(','));
        });

        // Download
        var csvContent = csv.join('\n');
        var blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
        var link = document.createElement('a');
        var url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', 'export_' + Date.now() + '.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    // Form validation
    $('form').on('submit', function(e) {
        var form = $(this);

        // Check required fields
        var isValid = true;
        form.find('[required]').each(function() {
            if ($(this).val() === '') {
                isValid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });

        if (!isValid) {
            e.preventDefault();
            alert('필수 항목을 입력해주세요. (Please fill in all required fields)');
            return false;
        }
    });

    // Remove validation error on input
    $('input, select, textarea').on('input change', function() {
        $(this).removeClass('is-invalid');
    });

    // Datepicker (if using)
    if (typeof $.fn.datepicker !== 'undefined') {
        $('.datepicker').datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true,
            todayHighlight: true
        });
    }

    // Select2 initialization (if using)
    if (typeof $.fn.select2 !== 'undefined') {
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%'
        });
    }
});

/**
 * Format number as currency
 */
function formatCurrency(amount, currency = '₩') {
    return currency + Number(amount).toLocaleString('ko-KR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });
}

/**
 * Format date
 */
function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('ko-KR');
}

/**
 * Show loading overlay
 */
function showLoading() {
    if ($('#loadingOverlay').length === 0) {
        $('body').append('<div id="loadingOverlay" style="position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:9999;display:flex;align-items:center;justify-content:center;"><div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div></div>');
    }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    $('#loadingOverlay').remove();
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    var bgClass = 'bg-' + type;
    var toast = $('<div class="toast align-items-center text-white ' + bgClass + ' border-0" role="alert"><div class="d-flex"><div class="toast-body">' + message + '</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div></div>');

    if ($('.toast-container').length === 0) {
        $('body').append('<div class="toast-container position-fixed top-0 end-0 p-3"></div>');
    }

    $('.toast-container').append(toast);
    var bsToast = new bootstrap.Toast(toast[0]);
    bsToast.show();

    setTimeout(function() {
        toast.remove();
    }, 5000);
}

/**
 * AJAX helper for API calls
 */
function apiCall(url, method, data, successCallback, errorCallback) {
    showLoading();

    $.ajax({
        url: url,
        method: method,
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(response) {
            hideLoading();
            if (successCallback) {
                successCallback(response);
            }
        },
        error: function(xhr, status, error) {
            hideLoading();
            console.error('API Error:', error);
            if (errorCallback) {
                errorCallback(xhr, status, error);
            } else {
                showToast('오류가 발생했습니다. (An error occurred)', 'danger');
            }
        }
    });
}

/**
 * Calculate line total for order items
 */
function calculateLineTotal(quantity, unitPrice, discountPercent = 0) {
    var subtotal = quantity * unitPrice;
    var discount = subtotal * (discountPercent / 100);
    return subtotal - discount;
}

/**
 * Calculate order total
 */
function calculateOrderTotal(subtotal, discountPercent = 0, taxRate = 10, shippingCost = 0) {
    var discount = subtotal * (discountPercent / 100);
    var taxableAmount = subtotal - discount;
    var tax = taxableAmount * (taxRate / 100);
    return taxableAmount + tax + shippingCost;
}

document.getElementById('voucherForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var form = event.target;
    var formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(data => {
        var newWindow = window.open();
        newWindow.document.write(data);
        newWindow.document.close();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
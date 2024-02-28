function printDiv() {
    var invoiceElement = document.getElementById("invoice-POS");

    if (invoiceElement) {
        var printWindow = window.open('', '', 'width=700,height=700');
        printWindow.document.open();
        printWindow.document.write('<html><head><title>Print Invoice</title></head><body>');
        printWindow.document.write(invoiceElement.innerHTML);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
        printWindow.close();
    } else {
        alert("Div with ID 'invoice-POS' not found.");
    }
}

// Add a click event listener to the button
document.getElementById("printButton").addEventListener("click", printDiv);
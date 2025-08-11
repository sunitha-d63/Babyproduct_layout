
document.querySelector('input[name="phone"]').addEventListener('keydown', function(e) {
   
    if ([46, 8, 9, 27, 13].includes(e.keyCode) || 
        (e.keyCode >= 48 && e.keyCode <= 57) || 
        (e.keyCode >= 96 && e.keyCode <= 105)) {
        return;
    }
    e.preventDefault();
});

document.querySelector('input[name="email"]').addEventListener('input', function(e) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(e.target.value) && e.target.value.length > 0) {
        e.target.setCustomValidity('Please enter a valid email (e.g., example@domain.com)');
    } else {
        e.target.setCustomValidity('');
    }
});

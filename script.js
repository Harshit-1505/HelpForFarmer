const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});
loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});
document.addEventListener("DOMContentLoaded", function() {
    
    const sendOtpBtn = document.getElementById("sendOtp");
    const verifyOtpBtn = document.getElementById("verifyOtp"); 
    const emailInput = document.getElementById("email"); 
    const otpInput = document.getElementById("otp"); 


    sendOtpBtn.addEventListener("click", async () => {
        const email = emailInput.value.trim(); 
        if (!email) {
            alert("Please enter your email");
            return;
        }
        // console.log("Sending OTP to:", email);

        try {
            const response = await fetch("http://127.0.0.1:5000/send-otp", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email })
            });

            const result = await response.json();
            console.log("Server response:", result); 

            if (response.ok) {
                alert(result.message); 
            } else {
                alert(result.error); 
            }
        } catch (error) {
            console.error("Error sending OTP:", error);
            alert("Error sending OTP. Please try again later.");
        }
    });

    verifyOtpBtn.addEventListener("click", async () => {
        const email = emailInput.value.trim(); 
        const otp = otpInput.value.trim(); 

        if (!email || !otp) {
            alert("Please enter both email and OTP");
            return;
        }
        console.log("Verifying OTP for email:", email, "OTP:", otp);
        try {
            
            const response = await fetch("http://127.0.0.1:5000/verify-otp", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email, otp: otp })
            });
            const result = await response.json();
            console.log("Server response:", result);
            if (response.ok) {
                alert(result.message); 
                alert("You are now logged in!");
            } else {
                alert(result.error); 
            }
        } catch (error) {
            console.error("Error verifying OTP:", error);
            alert("Error verifying OTP. Please try again later.");
        }
    });
});

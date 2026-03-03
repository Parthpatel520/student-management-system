from email.message import EmailMessage
import smtplib #Used to connect to Gmail SMTP server.
from app.config import settings

def send_otp_email(to_email: str, otp: str):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Verify Your Account -OTP"
        msg["From"] = settings.EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Reply-To"] = settings.EMAIL_ADDRESS
        
        # msg.set_content(
        #     f"""
        #     Hello,
            
        #     Your One Time Password (OTP) is: {otp}
            
        #     This OTP will expire in 5 minutes.

        #     If you did not request this, please ignore this email.

        #     Regards,
        #     Student Management System
        #     """)
        
        msg.add_alternative(
            f"""
           <html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f6f9;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            padding: 25px;
            border-radius: 8px;
            max-width: 500px;
            margin: auto;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .otp {{
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            letter-spacing: 4px;
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 25px;
            font-size: 12px;
            color: #888888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2 style="color:#2c3e50;">Student Management System</h2>
        <p>Hello,</p>

        <p>Thank you for registering with <strong>Student Management System</strong>.</p>

        <p>Please use the following One-Time Password (OTP) to verify your email address:</p>

        <div class="otp">{otp}</div>

        <p>This OTP will expire in <strong>5 minutes</strong>.</p>

        <p>If you did not request this verification, please ignore this email.</p>

        <div class="footer">
            © 2026 Student Management System <br>
            All rights reserved.
        </div>
    </div>
</body>
</html>
            """, subtype="html")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
                server.send_message(msg)
                
        print("Email sent successfully:")
        
    except Exception as e:
        print("Email sending failed:", e)

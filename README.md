# Coffee Bar

A simple web app for ordering coffee. Each order is sent as text message (via [Twilio](https://www.twilio.com/)) to the barista.

## Environment Variables

    TO_PHONE_NUMBER="+1234567890"     # barista's phone number
    FROM_PHONE_NUMBER="+15555555555"  # Twilio "from" number
    TWILIO_AUTH_TOKEN="..."           # Twilio authentication token
    TWILIO_ACCOUNT_SID="..."          # Twilio session ID

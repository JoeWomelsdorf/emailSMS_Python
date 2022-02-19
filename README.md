# EmailSMS_Python
Gateway between email and SMS/MMS for Python3.  Allows for two way communication between a server and mobile device.  

## Installation

Install requirements with [pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```

## Usage

```python
from EmailSMS import emailSMS

# Initialize CommManager Object
manager = CommManager(phone_num='XXXXXXXXXX', carrier="XXXX",
                          email_address="EMAIL",
                          email_password="PASSWORD")

# Sends an SMS to the configured phone with a subject line "Hello, World!"
manager.send_sms("Hello, World!")

# Sends an MMS to the configured phone with a subject line "Hello, World!"
manager.send_mms("Hello, World!")

#Returns an array of new (unread) messages from the configured phone.
manager.check_incoming()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
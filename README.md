# Python-Email-Sender
This is a python-email-sender

# How to use
## Basic usage (Text)
* You have to fill out the below arguments:
```
--sender: The email of sender
--smtp: The email server. (default is smtp.gmail.com)
--receiver: The email of receiver
--password: The email server password
--title: The title of the email
--content: The contents of the email
```

* Usage: (Python)
```
import python_email_sender as email

email_args = email.parse_args()
email.sendmail(email_args)
```

* Usage: (Shell)
```
python ~~ --sender <Sender Email> --smtp <Sender SMTP Server Address> --receiver <Receiver Email> --password <Sender SMTP Password> --title <The title of the email> --content <Contents>
```

## Send text file
* You have to fill out the below arguments:
```
--sender: The email of sender
--smtp: The email server. (default is smtp.gmail.com)
--receiver: The email of receiver
--password: The email server password
--title: The title of the email
--content_file: The path of the contents file
```

* Usage:
```
import python_email_sender as email

email_args = email.parse_args()
email.sendmail(email_args)
```

* Usage: (Shell)
```
python ~~ --sender <Sender Email> --smtp <Sender SMTP Server Address> --receiver <Receiver Email> --password <Sender SMTP Password> --title <The title of the email> --content_file <Contents file path>
```

# Other options
```
--save_config: save configs such as sender, smtp, receiver, password at ~/.python-email-sender/config
```
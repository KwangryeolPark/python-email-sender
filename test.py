import python_email_sender as email

email_args = email.parse_args()
email.sendmail(email_args)
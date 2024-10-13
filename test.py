from core.email_spammer import EmailSpammner


if __name__ == '__main__':
    message = input("Input the message : ")
    # Pass the object
    spammer = EmailSpammner(message)
    spammer.run()



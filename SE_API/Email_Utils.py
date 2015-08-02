__author__ = 'sagi'


from google.appengine.api import mail


def send_validation_email(token, email, name):
    emailSuffix = str(email).split('@')[1]
    message = mail.EmailMessage(sender="SE-Hub Support <se-hub@appspot.gserviceaccount.com>",
                                subject="SE-Hub Activate Account")

    message.to = email

    message.body = """
    Dear """+name+""":

    To Activate your SE-Hub Account please click on the link below:<br>
    http://se-hub.appspot.com/api/validation/confirm/"""+token+"""|"""+emailSuffix+"""
    to get access to your Campus :)

    Please let us know if you have any questions.

    SE-Hub (c) 2015 niptop Team.
    """

    message.html = """
    <html><head></head><body>
        <div>
        <center>
            <img src='https://cloud.githubusercontent.com/assets/2984053/6825467/7c9d0402-d303-11e4-9827-62a6d66f937a.png'>
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" type="text/css" rel="stylesheet" />
        </center>
        </div>
        <div style='width:70%'>
            <h1>Hey """+name+"""- Just one More Step...</h1>
            <h3>Dear """+name+""":</h3>

            To Activate your SE-Hub Account please click on the link below:<br>
            http://se-hub.appspot.com/api/validation/confirm/"""+token+"""|"""+emailSuffix+"""

            to access you virtual class.
        </div>
        <br><br>
        Please let us know if you have any questions.
        <br>
        SE-Hub (c) 2015 niptop Team.
    </body>
    </html>
    """

    message.send()

def send_create_campus_request(email, name, campus_name):
    message = mail.EmailMessage(sender="SE-Hub Support <se-hub@appspot.gserviceaccount.com>",
                                subject="SE-Hub: "+campus_name+" Is Being Evaluated")

    message.to = email

    message.body = """
    Dear """+name+""":

    Thank You For Choosing SE-Hub!
    Your Request for creating a new Campus named """+campus_name + """
    is Being Evaluated.
    You Will Receive an e-mail When We finish the process<br>

    Please let us know if you have any questions.

    SE-Hub (c) 2015 niptop Team.
    """

    message.html = """
    <html><head>
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" type="text/css" rel="stylesheet" />
    </head><body>
        <div>
        <center>
            <img src='https://cloud.githubusercontent.com/assets/2984053/6825467/7c9d0402-d303-11e4-9827-62a6d66f937a.png'>

        </center>
        </div>
        <div style='width:70%'>
            <h1>Thank You For Choosing SE-Hub!</h1>
            <h3>Dear """+name+""":</h3>

           Your Request for creating a new Campus named """+campus_name + """
            is Being Evaluated.
            You Will Receive an e-mail When We finish the process<br>

            to access you virtual class.
        </div>
        <br><br>
        Please let us know if you have any questions.
        <br>
        SE-Hub (c) 2015 niptop Team.
    </body>
    </html>
    """
    message.send()


def notify_se_hub_campus_request(campus, campus_name):
    message = mail.EmailMessage(sender="SE-Hub Support <se-hub@appspot.gserviceaccount.com>",
                                subject="SE-Hub: "+campus_name+" Is Being Evaluated")

    message.to = 'se-hub@appspot.gserviceaccount.com'

    message.body = """
    a new Campus request
    """ + str(campus.to_JSON())

    message.html = """
    <html><head>
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" type="text/css" rel="stylesheet" />
    </head><body>
        <div>
        <center>
            <img src='https://cloud.githubusercontent.com/assets/2984053/6825467/7c9d0402-d303-11e4-9827-62a6d66f937a.png'>

        </center>
        </div>
        <div style='width:70%'>
            <h1>New Campus!</h1>
            <br>
            """ + str(campus.to_JSON()) + """
        <br>
        SE-Hub (c) 2015 niptop Team.
    </body>
    </html>
    """
    message.send()


def send_task_reminder( email, name, task_name, course_name):
    message = mail.EmailMessage(sender="SE-Hub Support <se-hub@appspot.gserviceaccount.com>",
                                subject="Hey! Due Date for task " + task_name + " is TOMORROW!")

    message.to = email

    message.body = """
    Dear """+name+""":

    You Have A Task that Due tomorrow! don't forget to submit the task.

            Task name: """ + task_name + """ \n
            In Course: """ + course_name + """ \n\n


    http://se-hub.appspot.com


    Please let us know if you have any questions.

    SE-Hub (c) 2015 niptop Team.
    """

    message.html = """
    <html><head>
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" type="text/css" rel="stylesheet" />
    </head><body>
        <div>
        <center>
            <img src='https://cloud.githubusercontent.com/assets/2984053/6825467/7c9d0402-d303-11e4-9827-62a6d66f937a.png'>
        </center>
        </div>
        <div style='width:70%'>
            <h3>Dear """+name+""":</h3>

            <center>
                <img src='https://pixabay.com/static/uploads/photo/2014/03/05/07/54/reminder-279903_640.png'>
            </center>
            <br>

            You Have A Task that Due tomorrow! don't forget to submit the task.<br>

            Task name: """ + task_name + """ <br>
            In Course: """ + course_name + """ <br>
            <br>
            <a href='http://se-hub.appspot.com/'>SE - Hub</a>

        </div>
        <br><br>
        Please let us know if you have any questions.
        <br>
        SE-Hub (c) 2015 niptop Team.
    </body>
    </html>
    """

    message.send()

from datetime import datetime

def log(msg):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_msg = now + " : " + msg.strip() + "\n"
    prefix = datetime.now().strftime("%Y-%m-%d-")
    open(prefix+"log.txt", "a").write(log_msg)

def log_points(fom,to,amount,why):
    log(str(fom) + " added " + str(amount) + " credits to " + str(to) + " for " + str(why) + "\n")

def log_use(user,command):
    log(str(user) + " requested use of " + str(command)+ "\n")
working_dir = "/home/maciek/Desktop/Studia/ochrona danych/var/log/"
files = ["auth.log", "auth.log.1", "auth.log.2", "auth.log.3", "auth.log.4"]
usernames = {}

for fname in files:
    current = open(working_dir + fname, "r")
    for line in current.readlines():
        if 'Failed password for' in line:
            user = line[line.find("for") + 3: line.find("from")]
            if user in usernames:
                usernames[user] += 1
            else:
                usernames[user] = 1
    current.close()
print(usernames)
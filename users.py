customers = (   
                ("passport id", "site id", (2100, 1, 1), "firstname - lastname"),# 
            )

def get_user(whichUser):
    if whichUser == "T":
        customer = ('t id', 't id', (1, 1, 1), "t")
        print (customer[3])
        return customer
    else:
        whichUser = int(whichUser)
        global customers
        print (customers[whichUser][3])
        return customers[whichUser]
    
def find_user(APN, already_user):
    if already_user == "T":
       return 'Test-user', None
    else:
        global customers
        for customer in customers:
            if APN in customer:
                if customers.index(customer) == int(already_user):
                    return customer[3], True
                else:
                    return customer[3], False

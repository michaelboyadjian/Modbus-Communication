import minimalmodbus

def askport():
    port = input('Which port are you using?\n')
    return port

def askdefaults():
    print("The current library defaults are:\n")
    print("     minimalmodbus.BAUDRATE = 19200")
    print("     minimalmodbus.PARITY = 'N'")
    print("     minimalmodbus.BYTESIZE = 8")
    print("     minimalmodbus.STOPBITS = 1")
    print("     minimalmodbus.TIMEOUT = 0.05")
    print("     minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = False\n")

    DEFAULTS = input('Would you like to change any of the default settings? (Yes/No)\n')

    if DEFAULTS == 'Yes':
        return defaults()
    elif DEFAULTS == "No":
        return True
    else:
        print("ERROR: Incorrect Input")

def defaults():
    baudrate()
    parity()
    bytesize()
    stopbits()
    timeout()
    closeport()
    return True

def baudrate():
    x = input("Change BAUDRATE? (Yes/No)\n")
    if x == "Yes":
        value = int(input("What value?\n"))
        exec("minimalmodbus.BAUDRATE = %d" % (value))
    elif x == "No":
        return True
    else:
        print("ERROR: Incorrect Input")
        return baudrate()

def parity():
    x = input("Change PARITY? (Yes/No)\n")

    if x == "Yes":
        value = input("What value?\n")
        exec("minimalmodbus.PARITY = %s" % (value))
    elif x == "No":
        return True
    else:
        print("ERROR: Incorrect Input")
        return parity()

def bytesize():
    x = input("Change BYTESIZE? (Yes/No)\n")

    if x == "Yes":
        value = input("What value?\n")
        exec("minimalmodbus.BYTESIZE = %d" % (value))
    elif x == "No":
        return True
    else:
        print("ERROR: Incorrect Input")
        return bytesize()

def stopbits():
    x = input("Change STOPBITS? (Yes/No)\n")

    if x == "Yes":
        value = input("What value?\n")
        exec("minimalmodbus.STOPBITS = %d" % (value))
    elif x == "No":
        return True
    else:
        print("ERROR: Incorrect Input")
        return stopbits()

def timeout():
    x = input("Change TIMEOUT? (Yes/No)\n")

    if x == "Yes":
        value = input("What value?\n")
        exec("minimalmodbus.TIMEOUT = %d" % (value))
    elif x == "No":
        return True
    else:
        print("ERROR: Incorrect Input")
        return timeout()

def closeport():
    x = input("Change CLOSE_PORT_AFTER_EACH_CALL? (Yes/No)\n")

    if x == "Yes":
        value = input("What value?")
        exec("minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = %s" % (value))
    elif x == "No":
        return True
    else:
        print("ERROR: Incorrect Input")
        return closeport()

def print_current_slave(port):
    instrument = minimalmodbus.Instrument(port, 0, 'rtu')
    slaveaddress = instrument.read_register(6, 0, 3, False)
    print('The CURRENT slave address is %d' % (slaveaddress))
    return True

def current_slave(port):
    instrument = minimalmodbus.Instrument(port, 0, 'rtu')
    slaveaddress = instrument.read_register(6, 0, 3, False)
    return slaveaddress

def change_slave_question(slaveaddress, port):
    SLAVE = input('Would you like to change the slave address? (Yes/No) \n')
    if SLAVE == "Yes":
        return change_slave(slaveaddress, port)
    elif SLAVE == "No":
        return read_registers(slaveaddress, port)
    else:
        print("ERROR: Incorrect Input")
        return change_slave_question(slaveaddress, port)

def change_slave(slaveaddress, port):
    x = input('What do you want to set your new slave address to?\n')

    try:
        r = int(x)
        instrument = minimalmodbus.Instrument(port=port, slaveaddress=0, mode='rtu')
        instrument.write_register(registeraddress=6, value=r, functioncode=6, signed=False)
        instrument9 = minimalmodbus.Instrument(port=port, slaveaddress=r, mode='rtu')
        newslave = instrument9.read_register(registeraddress=6, functioncode=3, signed=False)
        print("The NEW slave address is %d" % (newslave))
        return read_registers(newslave, port)
    except Exception as E:
        print(E)
        print('ERROR: Please Try Again')
        return change_slave(slaveaddress, port)

def read_registers(slave, port):
    REGISTER = input("Would you like to read any registers? (Yes/No)\n")

    if REGISTER == "Yes":
        return how_many_registers(slave, port)
    elif REGISTER == "No":
        print("END PROGRAM")
    else:
        print("ERROR: Incorrect Input")
        return read_registers(slave, port)

def how_many_registers(slave, port):
    HOWMANY = input("One (0), Multiple (1), All Meters (2)? (0/1/2)\n")

    if HOWMANY == "0":
        return read_single(slave, port)

    elif HOWMANY == "1":
        return read_multiple(slave, port)

    elif HOWMANY == "2":
        return read_meters(slave, port)

    else:
        print("ERROR: Incorrect Input")
        return how_many_registers(slave, port)

def read_single(slave, port):
    instrument3 = minimalmodbus.Instrument(port=port, slaveaddress=slave, mode='rtu')

    WHICHREG = input("Which register?\n")

    try:
        reg = int(WHICHREG)

        try:
            print('Register ' + str(reg) + ' = ' + str(
                instrument3.read_register(reg, 0, 3,
                                          False)))
        except:
            print('DEVICE ERROR')
    except:
        print("ERROR: Incorrect Input")
        return read_single(slave, port)

    return read_more(slave, port)

def read_multiple(slave, port):
    instrument4 = minimalmodbus.Instrument(port=port, slaveaddress=slave, mode='rtu')

    try:
        STARTREG = int(input("Start address:\n"))
    except:
        print("ERROR: Incorrect Input")
        return read_multiple(slave, port)

    try:
        ENDREG = int(input("End address:\n"))

        for address in range(STARTREG, ENDREG + 1):
            try:
                print('Register ' + str(address) + ' = ' + str(
                    instrument4.read_register(address, 0, 3,
                                              False)))
            except:
                print('DEVICE ERROR')
    except:
        print("ERROR: Incorrect Input")
        return (read_multiple(slave, port))

    return read_more(slave, port)

def read_meters(slave, port):
    instrument5 = minimalmodbus.Instrument(port=port, slaveaddress=slave, mode='rtu')

    count = 1
    for address in range(110, 157, 2):
        try:
            value = instrument5.read_register(address, 0, 3,
                                              False)
            output = "Meter %d (REG # %d) = %d" % (count, address, value)
            print(output)
        except Exception as E:
            print(E)
        count += 1

    return read_more(slave, port)

def read_more(slave, port):
    Q = input("Would you like to read more registers? (Yes/No)\n")
    if Q == "Yes":
        return how_many_registers(slave, port)
    elif Q == "No":
        print("END PROGRAM")
    else:
        print("ERROR: Incorrect Input")
        return read_more(slave, port)

def main():
    askdefaults()
    port = askport()
    print_current_slave(port)
    change_slave_question(current_slave(port), port)
    return True

main()
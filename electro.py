import serial

portname = '/dev/ttyUSB0'
request_string = '/?!\x0D\x0A'

def get_data_simple(portname):
    ''' simple function fetching data from tarif device
    the disadvantage of this function is, it take almost 30s and it can't
    be seen that it goes well .. but its simple

    it opens the port specified with 'portname' parameter,
    sends the data request, reads the response and return it
    as the functions return value'''
    
    with serial.Serial(port='/dev/ttyUSB0',baudrate=300,bytesize=7,parity=serial.PARITY_EVEN,stopbits=1,timeout=5) as port:
        port.write(request_string.encode('ascii'))
        answ = port.readlines()
        return answ

def get_data(portname):
    ''' this function is doing the same as get_data_simple but it tests
    the data structure a bit, prints lines already read and returns imediately
    after data tranmition ends

    the function returns all read data as the return value'''
    
    with serial.Serial(port='/dev/ttyUSB0',baudrate=300,bytesize=7,parity=serial.PARITY_EVEN,stopbits=1,timeout=5) as port:
        port.write(request_string.encode('ascii'))
        answ = []

        #read tarif device information
        line = port.readline()
        answ += [line]
        if len(line)==0:
            #something's wrong (b'/...\r\n' expected)
            return answ
        print(line.decode('ascii').strip())

        #read data
        while True:
              line = port.readline()
              answ += [line]
              if len(line)==0:
                  #no answer .. wrong
                  return answ
              if line[0]==ord('!'):
                  #end of data block
                  break
              print(line.decode('ascii').strip()pline)

        #read crc
        line = port.read(2)
        answ += [line]
              
        return answ

if __name__ == "__main__":

    #test 'get_data' function
    answ = get_data(portname)

    '''#test 'get_data_simple' function
    answ = get_data_simple(portname)
    for l in answ:
        print(l.decode('ascii').strip())'''

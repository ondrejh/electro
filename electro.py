import serial

#portname = '/dev/ttyUSB0'
#portname = '/dev/ttyS0'
portname = '/dev/ttyAMA0'
request_string = '/?!\x0D\x0A'


#tariff device entry symbols

STX = b'\x02'
ETX = b'\x03'

kwh_total_value_start_str = '1.8.0('
kwh_value_end_str = '*kWh'


def get_total_kwh(data_str):

    ''' return total kwh value from input data '''

    kwh = data_str[(data_str.find(kwh_total_value_start_str)+len(kwh_total_value_start_str)):]
    kwh = kwh[:kwh.find(kwh_value_end_str)]

    return(float(kwh))


def join_listofbytes(listof_bytes):

    ''' Join list of bytes returned by get_data function
    into one bytes block (return) '''
    
    retval = []
    for item in listof_bytes:
        retval+=item
    return bytes(retval)


def split_data_block(bytes_answer):

    ''' Split bytes (one block) into ident and data block,
    and checks checksum.
    
    returns [string(ident), string(data), string(checksum)] '''
    
    st = 0
    ident = []
    data = []
    checksum = 0
    checksum_result = 'None'
    for i in range(len(bytes_answer)):
        b=bytes_answer[i]
        if (st==0) and (b==ord(b'/')):
            st = 1
        elif b==ord(STX):
            st = 2
        elif b==ord(b'!'):
            st = 3
        elif b==ord(ETX):
            st = 4
        else: #other than service symbol
            if st == 1:
                ident += [b]
            if st == 2:
                data += [b]
            if (st == 2) or (st == 3):
                checksum ^= b
            if st == 4:
                checksum ^= ord(b'!')
                checksum ^= ord(ETX)
                if (checksum==b):
                    checksum_result = 'OK'
                else:
                    checksum_result = 'Error'
                st += 1
                
    return [bytes(ident).decode('ascii'),bytes(data).decode('ascii'),checksum_result]


def set_rtsdtr_power(port):

    port.setDTR(False) # -V
    port.setRTS(True)  # +V

def get_data_silent(portname):

    ''' simple function fetching data from tarif device
    the disadvantage of this function is, it take almost 30s and it can't
    be seen that it goes well .. but its simple

    it opens the port specified with 'portname' parameter,
    sends the data request, reads the response and return it
    as the functions return value'''
    
    with serial.Serial(portname,baudrate=300,bytesize=7,parity=serial.PARITY_EVEN,stopbits=1,timeout=5) as port:

        set_rtsdtr_power(port)
        
        port.write(request_string.encode('ascii'))
        answ = port.readlines()
        return answ


def get_data(portname):

    ''' this function is doing the same as get_data_simple but it tests
    the data structure a bit, prints lines already read and returns imediately
    after data tranmition ends

    the function returns all read data as the return value'''
    
    with serial.Serial(portname,baudrate=300,bytesize=7,parity=serial.PARITY_EVEN,stopbits=1,timeout=5) as port:

        set_rtsdtr_power(port)
        
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
              if (line[0]==ord('/')) or (line[0]==b'\x02'):
                  #print line without first char
                  print(line[1:].decode('ascii').strip())
              else:
                  print(line.decode('ascii').strip())

        #read crc
        line = port.read(2)
        answ += [line]
              
        return answ

if __name__ == "__main__":

    #test 'get_data' function
    answ = get_data(portname)

    '''#test 'get_data_simple' function
    answ = get_data_silent(portname)
    for l in answ:
        print(l.decode('ascii').strip())'''

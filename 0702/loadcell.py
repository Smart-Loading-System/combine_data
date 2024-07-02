import time
import sys
import RPi.GPIO as GPIO
from hx711v0_5_1 import HX711
import socket
import threading

HOST = '0.0.0.0' #모든 연결을 허락하기 위해 0.0.0.0으로 설정한다
PORT = 65432

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    if request.decode('utf-8') == "REQUEST":
        client_socket.sendall(str(wieght + ', ' + wieght2 + ', ' + weight3 + ', ' + weight4).encode('utf-8'))
    client_socket.close()

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Server listening on port', PORT)
        while True:
            client_socket, addr = s.accept()
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_socket,)
            )
            client_handler.start()

'''
About READ_MODE
----------------

If set to "interrupt based" (--interrupt_based), sets the class to use the "GPIO.add_event_detect"
to know when to poll and execute the passed callback.

If set to "polling based" (--polling_based), sets the example polls a new value from the HX711 using
the readRawBytes() method, which will wait until the HX711 is ready.
'''
READ_MODE_INTERRUPT_BASED = "--interrupt-based"
READ_MODE_POLLING_BASED = "--polling-based"
READ_MODE = READ_MODE_POLLING_BASED

if len(sys.argv) > 1 and sys.argv[1] == READ_MODE_INTERRUPT_BASED:
    READ_MODE = READ_MODE_INTERRUPT_BASED
    print("[INFO] Read mode is 'interrupt based'.")
else:
    print("[INFO] Read mode is 'polling based'.")
    
count = 0
hx = HX711(5, 6)
hx2 = HX711(16,20)
hx3 = HX711(17,27)
hx4 = HX711(23,24)

def printRawBytes(rawBytes):
    print(f"[RAW BYTES] {rawBytes}")

def printLong(rawBytes):
    print(f"[LONG] {hx.rawBytesToLong(rawBytes)} {hx2.rawBytesToLong(rawBytes)} {hx3.rawBytesToLong(rawBytes)} {hx4.rawBytesToLong(rawBytes)}")

def printLongWithOffset(rawBytes):
    print(f"[LONG WITH OFFSET] {hx.rawBytesToLongWithOffset(rawBytes)} {hx2.rawBytesToLongWithOffset(rawBytes)} {hx3.rawBytesToLongWithOffset(rawBytes)} {hx4.rawBytesToLongWithOffset(rawBytes)}")

def printWeight(rawBytes):
    print(f"[WEIGHT] {hx.rawBytesToWeight(rawBytes)} {hx2.rawBytesToWeight(rawBytes)} {hx3.rawBytesToWeight(rawBytes)} {hx4.rawBytesToWeight(rawBytes)} gr")

def printAll(rawBytes):
    longValue = hx.rawBytesToLong(rawBytes)
    longWithOffsetValue = hx.rawBytesToLongWithOffset(rawBytes)
    weightValue = hx.rawBytesToWeight(rawBytes)
    
    longValue2 = hx2.rawBytesToLong(rawBytes)
    longWithOffsetValue2 = hx2.rawBytesToLongWithOffset(rawBytes)
    weightValue2 = hx2.rawBytesToWeight(rawBytes)
    
    longValue3 = hx3.rawBytesToLong(rawBytes)
    longWithOffsetValue3 = hx3.rawBytesToLongWithOffset(rawBytes)
    weightValue3 = hx3.rawBytesToWeight(rawBytes)
    
    longValue4 = hx4.rawBytesToLong(rawBytes)
    longWithOffsetValue4 = hx4.rawBytesToLongWithOffset(rawBytes)
    weightValue4 = hx4.rawBytesToWeight(rawBytes)
    print(f"[INFO] INTERRUPT_BASED | weight5-6 (grams): {weightValue} weight16-20 (grams): {weightValue2} weight17-27 (grams): {weightValue3} weight23-24 (grams): {weightValue4}")
    time.sleep(3)

    return weightValue, weightValue2, weightValue3, weightValue4

def getRawBytesAndPrintAll():
    global count
    rawBytes = hx.getRawBytes()
    longValue = hx.rawBytesToLong(rawBytes)
    longWithOffsetValue = hx.rawBytesToLongWithOffset(rawBytes)
    weightValue = hx.rawBytesToWeight(rawBytes)
    
    rawBytes2 = hx2.getRawBytes()
    longValue2 = hx2.rawBytesToLong(rawBytes2)
    longWithOffsetValue2 = hx2.rawBytesToLongWithOffset(rawBytes2)
    weightValue2 = hx2.rawBytesToWeight(rawBytes2)
    
    rawBytes3 = hx3.getRawBytes()
    longValue3 = hx3.rawBytesToLong(rawBytes3)
    longWithOffsetValue3 = hx3.rawBytesToLongWithOffset(rawBytes3)
    weightValue3 = hx3.rawBytesToWeight(rawBytes3)
    
    rawBytes4 = hx4.getRawBytes()
    longValue4 = hx4.rawBytesToLong(rawBytes4)
    longWithOffsetValue4 = hx4.rawBytesToLongWithOffset(rawBytes4)
    weightValue4 = hx4.rawBytesToWeight(rawBytes4)
    
    weightValue /= 1.02929377511007
    weightValue3 /= 1.00909339076352
    weightValue4 /= 1.03247620427766
    
    sum = weightValue + weightValue2 + weightValue3 + weightValue4
    print(f" weight111 (grams): {weightValue} \t weight222 (grams): {weightValue2} \n weight333 (grams): {weightValue3} \t weight444 (grams): {weightValue4}") #\t weight444 (grams): {weightValue4}
    print(" ")
    print(" ")
    print(sum)
    #count += 1
    #print(count)
    time.sleep(3)

'''
About the reading format.
----------------
I've found out that, for some reason, the order of the bytes is not always the same between versions of python,
and the hx711 itself. I still need to figure out why.

If you're experiencing super random values, switch these values between `MSB` and `LSB` until you get more stable values.
There is some code below to debug and log the order of the bits and the bytes.

The first parameter is the order in which the bytes are used to build the "long" value. The second paramter is
the order of the bits inside each byte. According to the HX711 Datasheet, the second parameter is MSB so you
shouldn't need to modify it.
'''
hx.setReadingFormat("MSB", "MSB")
hx2.setReadingFormat("MSB", "MSB")
hx3.setReadingFormat("MSB", "MSB")
hx4.setReadingFormat("MSB", "MSB")

print("[INFO] Automatically setting the offset.")
hx.autosetOffset()
hx2.autosetOffset()
hx3.autosetOffset()
hx4.autosetOffset()

offsetValue = hx.getOffset()
offsetValue2 = hx2.getOffset()
offsetValue3 = hx3.getOffset()
offsetValue4 = hx4.getOffset()

print(f"[INFO] Finished automatically setting the offset. The new value is '{offsetValue}'.")

print("[INFO] You can add weight now!")

'''
# HOW TO CALCULATE THE REFFERENCE UNIT
1. Set the reference unit to 1 and make sure the offset value is set.
2. Load you sensor with 1kg or with anything you know exactly how much it weights.
3. Write down the 'long' value you're getting. Make sure you're getting somewhat consistent values.
    - This values might be in the order of millions, varying by hundreds or thousands and it's ok.
4. To get the wright in grams, calculate the reference unit using the following formula:
        
    referenceUnit = longValueWithOffset / 1000
        
In my case, the longValueWithOffset was around 114000 so my reference unit is 114,
because if I used the 114000, I'd be getting milligrams instead of grams.
'''

referenceUnit = 114

print(f"[INFO] Setting the 'referenceUnit' at {referenceUnit}.")
hx.setReferenceUnit(referenceUnit)
hx2.setReferenceUnit(referenceUnit)
hx3.setReferenceUnit(referenceUnit)
hx4.setReferenceUnit(referenceUnit)
print(f"[INFO] Finished setting the 'referenceUnit' at {referenceUnit}.")

if READ_MODE == READ_MODE_INTERRUPT_BASED:
    print("[INFO] Enabling the callback.")
    hx.enableReadyCallback(printAll)
    hx2.enableReadyCallback(printAll)
    hx3.enableReadyCallback(printAll)
    hx4.enableReadyCallback(printAll)
    print("[INFO] Finished enabling the callback.")


while True:
    try:
        if READ_MODE == READ_MODE_POLLING_BASED:
            wieght, wieght2, weight3, weight4 = getRawBytesAndPrintAll()

        
            
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        print("[INFO] 'KeyboardInterrupt Exception' detected. Cleaning and exiting...")
        sys.exit()

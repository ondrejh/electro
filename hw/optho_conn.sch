EESchema Schematic File Version 2  date So 17. květen 2014, 12:57:22 CEST
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
EELAYER 43  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title ""
Date "17 may 2014"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 1000 1000 0    60   ~ 0
TTL version:
Text Label 1700 2400 0    60   ~ 0
GND
Text Label 1700 1900 0    60   ~ 0
RXI
Text Label 1700 1700 0    60   ~ 0
TXO
Text Label 1700 1200 0    60   ~ 0
+5V
Connection ~ 1600 1500
Wire Wire Line
	1900 1500 1600 1500
Wire Wire Line
	1600 1600 1600 1500
Wire Wire Line
	1600 1500 1600 1100
Wire Wire Line
	1600 1600 1500 1600
Wire Wire Line
	1500 1800 2600 1800
Wire Wire Line
	2600 1800 2800 1800
Wire Wire Line
	2800 2300 2800 2400
Wire Wire Line
	2400 1700 2800 1700
Wire Wire Line
	2800 1700 2800 1600
Wire Wire Line
	2800 2400 1600 2400
Wire Wire Line
	2800 1800 2800 1900
Wire Wire Line
	2800 1200 2800 1100
Wire Wire Line
	2800 1100 2600 1100
Wire Wire Line
	2600 1100 1600 1100
Connection ~ 2600 1800
Wire Wire Line
	1500 1900 1600 1900
Wire Wire Line
	1600 1900 1600 2400
Wire Wire Line
	1500 1700 1900 1700
Wire Wire Line
	2400 1500 2600 1500
Wire Wire Line
	2600 1500 2600 1800
$Comp
L CONN_4 X1
U 1 1 53773A11
P 1150 1750
F 0 "X1" V 1100 1750 50  0000 C CNN
F 1 "CONN_4" V 1200 1750 50  0000 C CNN
	1    1150 1750
	-1   0    0    1   
$EndComp
$Comp
L R R2
U 1 1 5377393D
P 2150 1500
F 0 "R2" V 2230 1500 50  0000 C CNN
F 1 "4k7" V 2150 1500 50  0000 C CNN
	1    2150 1500
	0    1    -1   0   
$EndComp
$Comp
L R R1
U 1 1 537738B2
P 2150 1700
F 0 "R1" V 2230 1700 50  0000 C CNN
F 1 "390R" V 2150 1700 50  0000 C CNN
	1    2150 1700
	0    -1   -1   0   
$EndComp
$Comp
L LED D1
U 1 1 537737E5
P 2800 1400
F 0 "D1" V 2650 1550 50  0000 C CNN
F 1 "SFH409-2" V 2750 1700 50  0000 C CNN
	1    2800 1400
	0    -1   1    0   
$EndComp
$Comp
L OPTO_NPN Q1
U 1 1 537737B5
P 2900 2100
F 0 "Q1" H 3050 2150 50  0000 L CNN
F 1 "SFH309FA" H 3050 2050 50  0000 L CNN
	1    2900 2100
	-1   0    0    -1  
$EndComp
$EndSCHEMATC

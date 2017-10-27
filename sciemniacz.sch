EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
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
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L LINE #PWR?
U 1 1 59F353DF
P 1950 1550
F 0 "#PWR?" H 1950 1400 50  0001 C CNN
F 1 "LINE" H 1950 1700 50  0000 C CNN
F 2 "" H 1950 1550 50  0001 C CNN
F 3 "" H 1950 1550 50  0001 C CNN
	1    1950 1550
	1    0    0    -1  
$EndComp
$Comp
L NEUT #PWR?
U 1 1 59F353F3
P 1950 2500
F 0 "#PWR?" H 1950 2350 50  0001 C CNN
F 1 "NEUT" H 1950 2650 50  0000 C CNN
F 2 "" H 1950 2500 50  0001 C CNN
F 3 "" H 1950 2500 50  0001 C CNN
	1    1950 2500
	-1   0    0    1   
$EndComp
$Comp
L D_Bridge_+-AA D?
U 1 1 59F3547E
P 1950 2000
F 0 "D?" H 2000 2275 50  0000 L CNN
F 1 "D_Bridge_+-AA" H 2000 2200 50  0000 L CNN
F 2 "" H 1950 2000 50  0001 C CNN
F 3 "" H 1950 2000 50  0001 C CNN
	1    1950 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	1950 2500 1950 2300
Wire Wire Line
	1950 1700 1950 1550
$Comp
L GND #PWR?
U 1 1 59F354D1
P 1400 2500
F 0 "#PWR?" H 1400 2250 50  0001 C CNN
F 1 "GND" H 1400 2350 50  0000 C CNN
F 2 "" H 1400 2500 50  0001 C CNN
F 3 "" H 1400 2500 50  0001 C CNN
	1    1400 2500
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR?
U 1 1 59F354E7
P 2750 1550
F 0 "#PWR?" H 2750 1400 50  0001 C CNN
F 1 "VCC" H 2750 1700 50  0000 C CNN
F 2 "" H 2750 1550 50  0001 C CNN
F 3 "" H 2750 1550 50  0001 C CNN
	1    2750 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	2250 2000 2750 2000
Wire Wire Line
	2750 2000 2750 1550
Wire Wire Line
	1650 2000 1400 2000
Wire Wire Line
	1400 2000 1400 2500
$Comp
L +5V #PWR?
U 1 1 59F35533
P 3850 1550
F 0 "#PWR?" H 3850 1400 50  0001 C CNN
F 1 "+5V" H 3850 1690 50  0000 C CNN
F 2 "" H 3850 1550 50  0001 C CNN
F 3 "" H 3850 1550 50  0001 C CNN
	1    3850 1550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59F3554A
P 3800 2500
F 0 "#PWR?" H 3800 2250 50  0001 C CNN
F 1 "GND" H 3800 2350 50  0000 C CNN
F 2 "" H 3800 2500 50  0001 C CNN
F 3 "" H 3800 2500 50  0001 C CNN
	1    3800 2500
	1    0    0    -1  
$EndComp
$EndSCHEMATC

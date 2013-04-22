import time
MASK = [            ## O = AO, T = BOOT
	0xF0000000, ## PREG_PAD_0  .... AAAA AAAA AAAA AAAA AAAA AAAA AAAA
	0xFF000000, ## PREG_PAD_1  .... .... BBBB BBBB BBBB BBBB BBBB BBBB
	0xFC000000, ## PREG_PAD_2  .... ..DD DDDD DDDD CCCC CCCC CCCC CCCC 
	0xFF0C0000, ## PREG_PAD_3  .... .... XXXX ..TT TTTT TTTT TTTT TTTT 
	0x00000000, ## PREG_PAD_4  XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX
	0xFF800003, ## PREG_PAD_5  .... .... .YYY YYYY YYYY YYYY YYYY YYYY 
	0xF800F000, ## PREG_PAD_6  .... .ZZZ ZZZZ ZZZZ .... EEEE EEEE EEEE
	0xFFFFF003  ## PREG_PAD_AO .... .... .... .... .... OOOO OOOO OOOO 
]

def CharToHex(Char):
	s = '0123456789ABCDEF '
	for i in range(0, 17):
		if s[i] == Char: 
			return { 
				0: "0000",
				1: "0001",
				2: "0010",
				3: "0011",
				4: "0100",
				5: "0101",
				6: "0110",
				7: "0111",
				8: "1000",
				9: "1001",
				10: "1010",
				11: "1011",
				12: "1100",
				13: "1111",
				14: "1110",
				15: "1111",
				16: "0000"
			}.get(i)
	return "----"
		
def StrToHex(Str):
	"Converts String to Hex"
	l = len(Str)
	s = Str.upper()
	retstr = ""
	for i in range(len(s)):
		retstr = retstr + CharToHex(s[i])
	return retstr
old_data = [
	"00000000000000000000000000000000",
	"00000000000000000000000000000000",
	"00000000000000000000000000000000",
	"00000000000000000000000000000000",
	"00000000000000000000000000000000",
	"00000000000000000000000000000000",
	"00000000000000000000000000000000",
	"00000000000000000000000000000000"
]
 

while(1):
	gpio = open('/sys/class/gpio/cmd', 'r')
	## gpio = open('c:\python27\gpio.sysfs', 'r')
	bank = 0
	data = {}
	gpio.readline()
	for line in gpio:
		data[bank] = line.rstrip('\n')
		# print data[bank]
		bank = bank + 1
	gpio.close()

	cOutput = '0'
	print "BANK: 1098-7654-3210-9876-5432-1098-7654-3210"
	bank_data = {}
	for bank in range(len(data)):
		bank_data["NAME"] = data[bank][:5].strip()
		bank_data["EN"]   = StrToHex(data[bank][7:15])
		bank_data["OUT"]  = StrToHex(data[bank][17:25])
		bank_data["IN"]   = StrToHex(data[bank][27:35])
		# print  bank_data["EN"]
		# print  bank_data["OUT"]
		# print  bank_data["IN"] 
		bank_data["STATUS"]  = ""
		txt = ""
		bit = 0x80000000
		for i in range (0, 32):
			if (i != 0) & ((i & 3) == 0):
				bank_data["STATUS"] = bank_data["STATUS"] + "-"
			if (MASK[bank] & bit):
				txt = "."
			else:

				if (bank_data["EN"][i] == cOutput):
					txt = "_"
				else:
					if (bank_data["IN"][i] == old_data[bank][i]):
						txt = bank_data["IN"][i]
					else:
						txt = "\x1b[1;31m"+ bank_data["IN"][i] + "\x1b[0m"
			bank_data["STATUS"] = bank_data["STATUS"] + txt
			bit = bit >> 1

		print bank_data["NAME"] + "  : " + bank_data["STATUS"]
		old_data[bank] = bank_data["IN"]
	#time.sleep(1)
	raw_input("a")
        print "read:"	


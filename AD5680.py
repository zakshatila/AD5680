import spidev				#Using spidev to interact with spi interface

class AD5680():
    def initialize(self):
            #Setup SPI communication SoC
            self.spi=spidev.SpiDev()
            self.spi.open(1,2) 			  	#Spi port 1 , CS 2 
            self.spi.mode = 1
            self.spi.max_speed_hz = SPI_SPEED 		#AD5680 supports up to 30 Mhz
            self.bits_per_word = SPI_BITS_PER_WORD			#Based on DAC specifications
    
    def setOutput(self,val):
            # Outputs from 0 to 5 v (Vref = 5v)
            # According to AD5680 Datasheet, Vout= Vref*(D/262144) 
            # Where D is the data input and 262144 represents 2^18 
            Voltage = (float(val)/5.0)*262144.0
            To_Out_int = int(Voltage)
            To_Out_Bin = '{0:018b}'.format(0)
            if To_Out_int > 0 : #AD5680 Cannot Send negative voltage
                To_Out_Bin = '{0:018b}'.format(To_Out_int)
            # Last 4 bits (LSB) would have a 00 in the LSB because those are dont care and do not affect SPI communication
            Out_Hex1 = int('0000' + To_Out_Bin [0:4],2) # To_Out_Bin[0:4] goes from 0 to the third number (4 ignored)
            Out_Hex2 = int(To_Out_Bin [4:12],2) #To_Out_Bin[4:12] goes from 4 to the 11th....
            Out_Hex3 = int(To_Out_Bin [12:18] + '00',2)#12 to 18
            
            To_Out_Complete = [Out_Hex1,Out_Hex2,Out_Hex3]
        
            #Output
            
            self.spi.xfer2(To_Out_Complete) 
	

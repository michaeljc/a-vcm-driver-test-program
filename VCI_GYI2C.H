//#include "VCI_GYI2C.H"

#define DEV_GY7501A		1//1ch-I2C
#define DEV_GY7512		2//2ch-I2C
#define DEV_GY7514		3//4ch-I2C
#define DEV_GY7518		4//8ch-I2C
#define DEV_GY7503		5//1ch-I2C
#define DEV_GY7506		6//1ch-I2C,module/
#define DEV_GY7601		7//1ch-I2C
#define DEV_GY7602		8//2ch-I2C
#define DEV_GY7604		9//4ch-I2C
#define DEV_GY7608		10//8ch-I2C

typedef struct GYI2C_DATA_INFO{
						BYTE SlaveAddr;//设备物理地址，bit7-1有效
						BYTE Databuffer[520];//Data 报文的数据；
						UINT WriteNum;//地址和数据的总个数
						UINT ReadNum;//需要读的数据的个数
						BYTE IoSel;//1 表示被选择，将被读/写
						BYTE IoData;//IO口状态，bit3－0分别表示4个IO口
									//只有与IoSel中为1的位相同的位值有效
						UINT DlyMsRead;//I2C读操作时，PC发出读命令后，延时多少ms请求读到的数据。
						BYTE Reserved[4];//Reserved 系统保留。
						}GYI2C_DATA_INFO,*pGYI2C_DATA_INFO;





extern "C" 
{ 
	DWORD	__stdcall  GYI2C_Open(DWORD DeviceType,DWORD DeviceInd,DWORD Reserved);
	DWORD	__stdcall  GYI2C_Close(DWORD DeviceType,DWORD DeviceInd);
	DWORD	__stdcall GYI2C_SetMode(DWORD DeviceType,DWORD DeviceInd,BYTE ModeValue);
	DWORD	__stdcall GYI2C_GetMode(DWORD DeviceType,DWORD DeviceInd);
	DWORD	__stdcall  GYI2C_SetClk(DWORD DeviceType,DWORD DeviceInd,DWORD ClkValue);
	DWORD	__stdcall  GYI2C_GetClk(DWORD DeviceType,DWORD DeviceInd);
	DWORD	__stdcall  GYI2C_SetChannel(DWORD DeviceType,DWORD DeviceInd,BYTE ChannelValue);
	DWORD	__stdcall  GYI2C_GetChannel(DWORD DeviceType,DWORD DeviceInd);

	DWORD	__stdcall  GYI2C_Read(DWORD DeviceType,DWORD DeviceInd,pGYI2C_DATA_INFO  pDataInfo);
	DWORD	__stdcall  GYI2C_Write(DWORD DeviceType,DWORD DeviceInd,pGYI2C_DATA_INFO pDataInfo);
	DWORD	__stdcall  GYI2C_Connect(DWORD DeviceType,DWORD DeviceInd,DWORD Reserved);//查询USB-I2C设备是否从系统中掉线或者被拔出。

	DWORD	__stdcall  GYI2C_SetIO(DWORD DeviceType,DWORD DeviceInd,pGYI2C_DATA_INFO pDataInfo);
	DWORD	__stdcall  GYI2C_GetIO(DWORD DeviceType,DWORD DeviceInd,pGYI2C_DATA_INFO pDataInfo);

	DWORD	__stdcall  GYI2C_Start(DWORD DeviceType,DWORD DeviceInd);
	DWORD	__stdcall  GYI2C_WriteByte(DWORD DeviceType,DWORD DeviceInd,BYTE DataValue);
	DWORD	__stdcall  GYI2C_ReadByte(DWORD DeviceType,DWORD DeviceInd,BYTE AckValue);
	DWORD	__stdcall  GYI2C_Stop(DWORD DeviceType,DWORD DeviceInd);
//GYI2C_Write2,GYI2C_Read2函数与GYI2C_Read, GYI2C_Write函数功能一样，仅是入口参数类型差别
	DWORD	__stdcall  GYI2C_Write2(DWORD DeviceType,DWORD DeviceInd,BYTE *buf,int buflen);
					//WRITE buf[]=	A0,00,11,22,33,44	
	DWORD	__stdcall GYI2C_Read2(DWORD DeviceType,DWORD DeviceInd,BYTE *buf,DWORD buflen);
/*
buf[0]=slaveaddr;	//I2C从设备地址
buf[1]=WriteData0;	//如果是当前地址读，则不需要
					//指定地址读的时候，需要在I2C读之前先写入的内部地址或其他命令。比如读AT24C02,则为24c02的内部地址
buf[2]=WriteData1;	//如果是单字节内部地址，或是对当前地址读，则不需要WriteData1。
...
buf[buflen-2]=ReadNum>>8;//高8位，需要读的数据字节个数
buf[buflen-1]=ReadNum;
数组的最后2个字节表示需要读取的字节个数。
举例：AT24C02指定地址读 : A1,00,01,00	//读数据长度0100＝256
	         当前地址读 : A1,01,00 //直接读，不指定内部地址。
	  AT24C256指定地址读：A1,00,00,01,00
*/
}
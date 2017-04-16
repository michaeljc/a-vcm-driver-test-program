#ifndef	LKIF_INCLUDED
#define	LKIF_INCLUDED

#ifdef I_AM_LKIF
#define EXP __declspec(dllexport)
#else
#define EXP __declspec(dllimport)
#endif

extern	"C"
{
// Measurement value structures
typedef enum {
	LKIF_FLOATRESULT_VALID,								// valid data
	LKIF_FLOATRESULT_RANGEOVER_P,						// over range at positive (+) side
	LKIF_FLOATRESULT_RANGEOVER_N,						// over range at negative (-) side
	LKIF_FLOATRESULT_WAITING,							// comparator result
} LKIF_FLOATRESULT;

typedef struct {
	LKIF_FLOATRESULT	FloatResult;					// valid or invalid data
	float				Value;							// measurement value during LKIF_FLOATRESULT_VALID.
														// Any other times will return an invalid value
} LKIF_FLOATVALUE;
///////////////////////////////////////////////
// Measurement Control Command
//
// Measurement Value Output
EXP BOOL		WINAPI	LKIF_GetCalcData(OUT LKIF_FLOATVALUE *CalcData1,OUT LKIF_FLOATVALUE *CalcData2);
// Timing ON/OFF
EXP	BOOL		WINAPI	LKIF_SetTiming(IN int OutNo,IN BOOL IsOn);
// Auto-zero ON/OFF
EXP	BOOL		WINAPI	LKIF_SetZero(IN int OutNo,IN BOOL IsOn);
// Reset
EXP	BOOL		WINAPI	LKIF_SetReset(IN int OutNo);
// Panel Lock
EXP	BOOL		WINAPI	LKIF_SetPanelLock(IN BOOL IsLock);
// Program Change
EXP	BOOL		WINAPI	LKIF_SetProgramNo(IN int ProgramNo);
// Program Check
EXP	BOOL		WINAPI	LKIF_GetProgramNo(OUT int *ProgramNo);
// Statistical Results Output
typedef struct {
	LKIF_FLOATVALUE		ToleUpper;						// tolerance upper limit
	LKIF_FLOATVALUE		ToleLower;						// tolerance lower limit
	LKIF_FLOATVALUE		AverageValue;					// average value
	LKIF_FLOATVALUE		MaxValue;						// maximum value
	LKIF_FLOATVALUE		MinValue;						// minimum value
	LKIF_FLOATVALUE		DifValue;						// maximum value - minimum value
	LKIF_FLOATVALUE		SdValue;						// standard deviation
	LONG				DataCnt;						// number of all data
	LONG				HighDataCnt;					// number of tolerance High data
	LONG				GoDataCnt;						// number of tolerance Go data
	LONG				LowDataCnt;						// number of tolerance Low data
} LKIF_FIGUREDATA;
EXP	BOOL		WINAPI	LKIF_GetFigureData(IN int OutNo,OUT LKIF_FIGUREDATA *FigureData);
// Clearing Statistics
EXP	BOOL		WINAPI	LKIF_ClearFigureData(void);
// Starting the Data Storage
EXP BOOL		WINAPI	LKIF_DataStorageStart(void);
// Stopping the Data Storage
EXP BOOL		WINAPI	LKIF_DataStorageStop(void);
// Initializing the Data Storage
EXP BOOL		WINAPI	LKIF_DataStorageInit(void);
// Outputting the Data Storage
EXP BOOL		WINAPI	LKIF_DataStorageGetData(IN int OutNo,IN int NumOutBuffer,OUT LKIF_FLOATVALUE *OutBuffer,OUT int *NumReceived);
// Data Storage Accumulation Status Output
EXP BOOL		WINAPI	LKIF_DataStorageGetStatus(IN int OutNo,OUT BOOL *IsStorage,OUT int *NumStorageData);
// Receive Light Waveform
EXP BOOL		WINAPI	LKIF_GetLight(IN int HeadNo,IN int PeekNo,OUT int *MeasurePosition,OUT int *NumReaded,OUT BYTE *Value);

///////////////////////////////////////////////
// Change Parameter Command
//
// Display Panel Switch
EXP BOOL		WINAPI	LKIF_SetPanel(IN int OutNo);
// Set Tolerance
EXP	BOOL		WINAPI	LKIF_SetTolerance(IN int OutNo,IN int UpperLimit,IN int LowerLimit,IN int Hysteresis);
// Set ABLE
typedef enum {
	LKIF_ABLEMODE_AUTO,									// automatic
	LKIF_ABLEMODE_MANUAL,								// manual
} LKIF_ABLEMODE;
EXP	BOOL		WINAPI	LKIF_SetAbleMode(IN int HeadNo,IN LKIF_ABLEMODE AbleMode);
// Set ABLE Control Range
EXP	BOOL		WINAPI	LKIF_SetAbleMinMax(IN int HeadNo,IN int Min,IN int Max);
// Set Measurement Mode
typedef enum {
	LKIF_MEASUREMODE_NORMAL,							// normal
	LKIF_MEASUREMODE_HALF_T,							// translucent object
	LKIF_MEASUREMDOE_TRAN_1,							// transparent object
	LKIF_MEASUREMODE_TRAN_2,							// transparent object 2
	LKIF_MEASUREMODE_MRS,								// multireflective object
} LKIF_MEASUREMODE;
EXP BOOL		WINAPI	LKIF_SetMeasureMode(IN int HeadNo,IN LKIF_MEASUREMODE MeasureMode);
// Set Number of Times of Alarm Processing
EXP	BOOL		WINAPI	LKIF_SetNumAlarm(IN int HeadNo,IN int NumAlarm);
// Set Alarm Level
EXP BOOL		WINAPI	LKIF_SetAlarmLevel(IN int HeadNo,IN int AlarmLevel);
// Starting the ABLE Calibration
EXP	BOOL		WINAPI	LKIF_AbleStart(IN int HeadNo);
// Finishing the ABLE Calibration
EXP	BOOL		WINAPI	LKIF_AbleStop(void);
// Stopping the ABLE Calibration
EXP	BOOL		WINAPI	LKIF_AbleCancel(void);
// Set Mounting Mode
typedef enum {
	LKIF_REFLECTIONMODE_DIFFUSION,						// diffuse reflection
	LKIF_REFLECTIONMODE_MIRROR,							// specular reflection
} LKIF_REFLECTIONMODE;
EXP BOOL		WINAPI	LKIF_SetReflectionMode(IN int HeadNo,IN LKIF_REFLECTIONMODE ReflectionMode);
// Set Calculation Method
typedef enum {
	LKIF_CALCMETHOD_HEADA,								// head A
	LKIF_CALCMETHOD_HEADB,								// head B
	LKIF_CALCMETHOD_HEAD_HEADA_PLUS_HEADB,				// head A+head B
	LKIF_CALCMETHOD_HEAD_HEADA_MINUS_HEADB,				// head A-head B
	LKIF_CALCMETHOD_HEAD_HEADA_TRANSPARENT,				// head A transparent object
	LKIF_CALCMETHOD_HEAD_HEADB_TRANSPARENT,				// head B transparent object
} LKIF_CALCMETHOD;
// Measurement target
typedef enum {
	LKIF_CALCTARGET_PEAK_1,								// peak 1
	LKIF_CALCTARGET_PEAK_2,								// peak 2
	LKIF_CALCTARGET_PEAK_3,								// peak 3
	LKIF_CALCTARGET_PEAK_4,								// peak 4
	LKIF_CALCTARGET_PEAK_1_2,							// peak 1-peak 2
	LKIF_CALCTARGET_PEAK_1_3,							// peak 1-peak 3
	LKIF_CALCTARGET_PEAK_1_4,							// peak 1-peak 4
	LKIF_CALCTARGET_PEAK_2_3,							// peak 2-peak 3
	LKIF_CALCTARGET_PEAK_2_4,							// peak 2-peak 4
	LKIF_CALCTARGET_PEAK_3_4,							// peak 3-peak 4
} LKIF_CALCTARGET;
EXP	BOOL		WINAPI	LKIF_SetCalcMethod(IN int OutNo,IN LKIF_CALCMETHOD CalcMethod,LKIF_CALCTARGET CalcTarget);
// Set Scaling
EXP	BOOL		WINAPI	LKIF_SetScaling(IN int OutNo,IN int HeadNo,IN int InputValue1,IN int OutputValue1,IN int InputValue2,IN int OutputValue2);
// Set Filter Mode
typedef enum {
	LKIF_FILTERMODE_MOVING_AVERAGE,						// moving average
	LKIF_FILTERMODE_LOWPASS,							// low pass filter
	LKIF_FILTERMODE_HIGHPASS,							// high pass filter
} LKIF_FILTERMODE;
EXP	BOOL		WINAPI	LKIF_SetFilterMode(IN int OutNo,OUT LKIF_FILTERMODE FilterMode);
// Set Number of Times for Averaging
typedef enum {
	LKIF_AVERAGE_1,										// 1 time
	LKIF_AVERAGE_4,										//
	LKIF_AVERAGE_16,									// 
	LKIF_AVERAGE_64,									//
	LKIF_AVERAGE_256,									//
	LKIF_AVERAGE_1024,									//
	LKIF_AVERAGE_4096,									//
	LKIF_AVERAGE_16384,									//
	LKIF_AVERAGE_65536,									//
	LKIF_AVERAGE_262144,								// 262144 times
} LKIF_AVERAGE;
EXP BOOL		WINAPI	LKIF_SetAverage(IN int OutNo,IN LKIF_AVERAGE Average);
// Set Cutoff Frequency
typedef enum {
	LKIF_CUTOFFFREQUENCY_1000,							// 1000Hz
	LKIF_CUTOFFFREQUENCY_300,							// 300Hz
	LKIF_CUTOFFFREQUENCY_100,							// 100Hz
	LKIF_CUTOFFFREQUENCY_30,							// 30Hz
	LKIF_CUTOFFFREQUENCY_10,							// 10Hz
	LKIF_CUTOFFFREQUENCY_3,								// 3Hz
	LKIF_CUTOFFFREQUENCY_1,								// 1Hz
	LKIF_CUTOFFFREQUENCY_0_3,							// 0.3Hz
	LKIF_CUTOFFFREQUENCY_0_1,							// 0.1Hz
} LKIF_CUTOFFFREQUENCY;
EXP	BOOL		WINAPI	LKIF_SetCutOffFrequency(IN int OutNo,IN LKIF_CUTOFFFREQUENCY CutOffFrequency);
// Set Trigger Mode
typedef enum {
	LKIF_TRIGGERMODE_EXT1,								// external trigger 1
	LKIF_TRIGGERMODE_EXT2,								// external trigger 2
} LKIF_TRIGGERMODE;
EXP	BOOL		WINAPI	LKIF_SetTriggerMode(IN int OutNo,IN LKIF_TRIGGERMODE TriggerMode);
// Set Offset
EXP BOOL		WINAPI	LKIF_SetOffset(IN int OutNo,IN int Offset);
// Set Analog Output Scaling
EXP	BOOL		WINAPI	LKIF_SetAnalogScaling(IN int OutNo,IN int InputValue1,IN int OutputVoltage1,IN int InputValue2,IN int OutputVoltage2);
// Set Calculation Mode
typedef enum {
	LKIF_CALCMODE_NORMAL,								// normal
	LKIF_CALCMODE_PEAKHOLD,								// peak hold
	LKIF_CALCMODE_BOTTOMHOLD,							// bottom hold
	LKIF_CALCMODE_PEAKTOPEAKHOLD,						// peak-to-peak hold
	LKIF_CALCMODE_SAMPLEHOLD,							// sample hold
	LKIF_CALCMODE_AVERAGEHOLD,							// average hold
} LKIF_CALCMODE;
EXP	BOOL		WINAPI	LKIF_SetCalcMode(IN int OutNo,IN LKIF_CALCMODE CalcMode);
// Set Minimum Display Unit
typedef enum {
	LKIF_DISPLAYUNIT_0000_01MM,							// 0.01mm
	LKIF_DISPLAYUNIT_000_001MM,							// 0.001mm
	LKIF_DISPLAYUNIT_00_0001MM,							// 0.0001mm
	LKIF_DISPLAYUNIT_0_00001MM,							// 0.00001mm
	LKIF_DISPLAYUNIT_00000_1UM,							// 0.1um
	LKIF_DISPLAYUNIT_0000_01UM,							// 0.01um
} LKIF_DISPLAYUNIT;
EXP	BOOL		WINAPI	LKIF_SetDisplayUnit(IN int OutNo,IN LKIF_DISPLAYUNIT DisplayUnit);
// Set Analog-Through
EXP	BOOL		WINAPI	LKIF_SetAnalogThrough(IN int OutNo,IN BOOL IsOn);
// Set Data Storage
typedef enum {
	LKIF_TARGETOUT_NONE,								// no target OUT
	LKIF_TARGETOUT_OUT1,								// OUT1
	LKIF_TARGETOUT_OUT2,								// OUT2
	LKIF_TARGETOUT_BOTH,								// OUT1 and OUT2
} LKIF_TARGETOUT;
typedef enum {
	LKIF_STORAGECYCLE_1,								// sampling rate x 1
	LKIF_STORAGECYCLE_2,								// sampling rate x 2 
	LKIF_STORAGECYCLE_5,								// sampling rate x 5
	LKIF_STORAGECYCLE_10,								// sampling rate x 10
	LKIF_STORAGECYCLE_20,								// sampling rate x 20
	LKIF_STORAGECYCLE_50,								// sampling rate x 50
	LKIF_STORAGECYCLE_100,								// sampling rate x 100
	LKIF_STORAGECYCLE_200,								// sampling rate x 200
	LKIF_STORAGECYCLE_500,								// sampling rate x 500
	LKIF_STORAGECYCLE_1000,								// sampling rate x 1000
} LKIF_STORAGECYCLE;
EXP	BOOL		WINAPI	LKIF_SetDataStorage(IN LKIF_TARGETOUT TargetOut,IN int NumStorage,IN LKIF_STORAGECYCLE StorageCycle);
// Set Sampling Rate
typedef enum {
	LKIF_SAMPLINGCYCLE_20USEC,							// 20us
	LKIF_SAMPLINGCYCLE_50USEC,							// 50us
	LKIF_SAMPLINGCYCLE_100USEC,							// 100us
	LKIF_SAMPLINGCYCLE_200USEC,							// 200us
	LKIF_SAMPLINGCYCLE_500USEC,							// 500us
	LKIF_SAMPLINGCYCLE_1MSEC,							// 1ms
} LKIF_SAMPLINGCYCLE;
EXP BOOL		WINAPI	LKIF_SetSamplingCycle(IN LKIF_SAMPLINGCYCLE SamplingCycle);
// Set Mutual Interference Prevention
EXP	BOOL		WINAPI	LKIF_SetMutualInterferencePrevention(IN BOOL IsOn);
// Set Timing Synchronization
typedef enum {
	LKIF_SYNCHRONIZATION_ASYNCHRONOUS,					// asynchronous
	LKIF_SYNCHRONIZATION_SYNCHRONIZED,					// synchronous
} LKIF_SYNCHRONIZATION;
EXP	BOOL		WINAPI	LKIF_SetTimingSynchronization(IN LKIF_SYNCHRONIZATION Synchronization);
// Set Comparator Output Format
typedef enum {
	LKIF_TOLERANCE_COMPARATOR_OUTPUT_FORMAT_NORMAL,		// normal
	LKIF_TOLERANCE_COMPARATOR_OUTPUT_FORMAT_HOLD,		// hold
	LKIF_TOLERANCE_COMPARATOR_OUTPUT_FORMAT_OFF_DELAY,	// off-delay
} LKIF_TOLERANCE_COMPARATOR_OUTPUT_FORMAT;
EXP	BOOL		WINAPI	LKIF_SetToleranceComparatorOutputFormat(IN LKIF_TOLERANCE_COMPARATOR_OUTPUT_FORMAT ToleranceComparatorOutputFormat);
// Set Strobe Time
typedef enum {
	LKIF_STOROBETIME_2MS,								// 2ms
	LKIF_STOROBETIME_5MS,								// 5ms
	LKIF_STOROBETIME_10MS,								// 10ms
	LKIF_STOROBETIME_20MS,								// 20ms
} LKIF_STOROBETIME;
EXP	BOOL		WINAPI	LKIF_SetStorobeTime(IN LKIF_STOROBETIME StorobeTime);
///////////////////////////////////////////////
// Check Parameter Command
//
// Display Panel Check
EXP BOOL		WINAPI	LKIF_GetPanel(OUT int *OutNo);
// Get Tolerance
EXP	BOOL		WINAPI	LKIF_GetTolerance(IN int OutNo,OUT int *UpperLimit,OUT int *LowerLimit,OUT int *Hysteresis);
// Get ABLE
EXP	BOOL		WINAPI	LKIF_GetAbleMode(IN int HeadNo,OUT LKIF_ABLEMODE *AbleMode);
// ABLE Control Range
EXP	BOOL		WINAPI	LKIF_GetAbleMinMax(IN int HeadNo,OUT int *Min,OUT int *Max);
// Get Measurement Mode
EXP BOOL		WINAPI	LKIF_GetMeasureMode(IN int HeadNo,OUT LKIF_MEASUREMODE *MeasureMode);
// Get Number of Times of Alarm Processing
EXP	BOOL		WINAPI	LKIF_GetNumAlarm(IN int HeadNo,OUT int *NumAlarm);
// Get Alarm Level
EXP	BOOL		WINAPI	LKIF_GetAlarmLevel(IN int HeadNo,OUT int *AlarmLevel);
// Get Mounting Mode
EXP BOOL		WINAPI	LKIF_GetReflectionMode(IN int HeadNo,OUT LKIF_REFLECTIONMODE *ReflectionMode);
// Get Calculation Method
EXP	BOOL		WINAPI	LKIF_GetCalcMethod(IN int OutNo,OUT LKIF_CALCMETHOD *CalcMethod,LKIF_CALCTARGET *CalcTarget);
// Get Scaling
EXP	BOOL		WINAPI	LKIF_GetScaling(IN int OutNo,IN int HeadNo,OUT int *InputValue1,OUT int *OutputValue1,OUT int *InputValue2,OUT int *OutputValue2);
// Get Filter Mode
EXP	BOOL		WINAPI	LKIF_GetFilterMode(IN int OutNo,OUT LKIF_FILTERMODE *FilterMode);
// Get Number of Times for Averaging
EXP	BOOL		WINAPI	LKIF_GetAverage(IN int OutNo,OUT LKIF_AVERAGE *Average);
// Get Cutoff Frequency
EXP	BOOL		WINAPI	LKIF_GetCutOffFrequency(IN int OutNo,OUT LKIF_CUTOFFFREQUENCY *CutOffFrequency);
// Get Trigger Mode
EXP	BOOL		WINAPI	LKIF_GetTriggerMode(IN int OutNo,OUT LKIF_TRIGGERMODE *TriggerMode);
// Get Offset
EXP BOOL		WINAPI	LKIF_GetOffset(IN int OutNo,IN int *Offset);
// Get Analog Output Scaling
EXP	BOOL		WINAPI	LKIF_GetAnalogScaling(IN int OutNo,OUT int *InputValue1,OUT int *OutputVoltage1,OUT int *InputValue2,OUT int *OutputVoltage2);
// Get Calculation Mode
EXP	BOOL		WINAPI	LKIF_GetCalcMode(IN int OutNo,OUT LKIF_CALCMODE *CalcMode);
// Get Minimum Display Unit
EXP	BOOL		WINAPI	LKIF_GetDisplayUnit(IN int OutNo,OUT LKIF_DISPLAYUNIT *DisplayUnit);
// Analog-Through
EXP	BOOL		WINAPI	LKIF_GetAnalogThrough(IN int OutNo,OUT BOOL *IsOn);
// Get Data Storage
EXP	BOOL		WINAPI	LKIF_GetDataStorage(IN LKIF_TARGETOUT *TargetOut,OUT int *NumStorage,OUT LKIF_STORAGECYCLE *StorageCycle);
// Get Sampling Rate
EXP BOOL		WINAPI	LKIF_GetSamplingCycle(OUT LKIF_SAMPLINGCYCLE *SamplingCycle);
// Get Mutual Interference Prevention
EXP	BOOL		WINAPI	LKIF_GetMutualInterferencePrevention(OUT BOOL *IsOn);
// Get Timing Synchronization
EXP	BOOL		WINAPI	LKIF_GetTimingSynchronization(OUT LKIF_SYNCHRONIZATION *Synchronization);
// Get Comparator Output Format
EXP	BOOL		WINAPI	LKIF_GetToleranceComparatorOutputFormat(OUT LKIF_TOLERANCE_COMPARATOR_OUTPUT_FORMAT *ToleranceComparatorOutputFormat);
// Get Strobe Time
EXP	BOOL		WINAPI	LKIF_GetStorobeTime(OUT LKIF_STOROBETIME *StorobeTime);
///////////////////////////////////////////////
// Mode Change Command
//
// Mode Switch
typedef enum {
	LKIF_MODE_NORMAL,									// normal mode
	LKIF_MODE_COMMUNICATION,							// setting mode
} LKIF_MODE;
EXP BOOL		WINAPI	LKIF_SetMode(IN LKIF_MODE Mode);
} // extern "C"

#endif	// LKIF_INCLUDED
/*
 * outputapi.h
 *
 *  Created on: Jun 4, 2014
 *      Author: mtryby
 */

#ifndef OUTPUTAPI_H_
#define OUTPUTAPI_H_
#define   MAGICNUMBER        516114521
#define   MAXFNAME  259      /* Max. # characters in file name         */
#define   MAXTITLE  3        /* Max. # title lines                     */
#define   MAXID     31       /* Max. # characters in ID name           */      //(2.00.11 - LR)


/*------------------- Error Messages --------------------*/
#define ERR411 "Input Error 411: no memory allocated for results."
#define ERR412 "Input Error 412: no results; binary file hasn't been opened."
#define ERR421 "Input Error 421: invalid parameter code."
#define ERR434 "File Error  434: unable to open binary output file."
#define ERR435 "File Error  435: run terminated; no results in binary file."
#define ERR436 "File Error  436: run terminated; wrong binary file type."


/* Epanet Results binary file API */
typedef struct ENResultsAPI ENResultsAPI; // opaque struct object

typedef enum {
	ENR_node = 1,
    ENR_link = 2
} ENR_ElementType;

typedef enum {
    ENR_getSeries    = 1,
    ENR_getAttribute = 2,
    ENR_getResult    = 3
} ENR_ApiFunction;

typedef enum {
    ENR_nodeCount  = 1,
    ENR_tankCount  = 2,
    ENR_linkCount  = 3,
    ENR_pumpCount  = 4,
    ENR_valveCount = 5
} ENR_ElementCount;

typedef enum {
    ENR_flowUnits   = 1,
    ENR_pressUnits  = 2
} ENR_Unit;

typedef enum {
	ENR_reportStart = 1,
	ENR_reportStep  = 2,
	ENR_simDuration = 3,
	ENR_numPeriods  = 4
}ENR_Time;

typedef enum {
    ENR_demand   = 0,
    ENR_head     = 1,
    ENR_pressure = 2,
    ENR_quality  = 3
} ENR_NodeAttribute;

typedef enum {
    ENR_flow         = 0,
    ENR_velocity     = 1,
    ENR_headloss     = 2,
    ENR_avgQuality   = 3,
    ENR_status       = 4,
    ENR_setting      = 5,
    ENR_rxRate       = 6,
    ENR_frctnFctr    = 7
} ENR_LinkAttribute;


#ifdef WINDOWS
  #ifdef __cplusplus
  #define DLLEXPORT extern "C" __declspec(dllexport) __stdcall
  #else
  #define DLLEXPORT __declspec(dllexport) __stdcall
  #endif
#else
  #ifdef __cplusplus
  #define DLLEXPORT extern "C"
  #else
  #define DLLEXPORT
  #endif
#endif



int DLLEXPORT ENR_open(ENResultsAPI* *enrapi, char* path);
int DLLEXPORT ENR_getEnVersion(ENResultsAPI* enrapi, int* version);
int DLLEXPORT ENR_getWarningCode(ENResultsAPI* enrapi, int* warncode);

int DLLEXPORT ENR_getNetSize(ENResultsAPI* enrapi, ENR_ElementCount code, int* count);
int DLLEXPORT ENR_getUnits(ENResultsAPI* enrapi, ENR_Unit code, int* unitFlag);
int DLLEXPORT ENR_getTimes(ENResultsAPI* enrapi, ENR_Time code, int* time);


int DLLEXPORT ENR_getNodeValue(ENResultsAPI* enrapi, int timeIndex, int nodeIndex, ENR_NodeAttribute attr, float *value);
int DLLEXPORT ENR_getLinkValue(ENResultsAPI* enrapi, int timeIndex, int linkIndex, ENR_LinkAttribute attr, float *value);

int DLLEXPORT ENR_getNodeID(ENResultsAPI* enrapi, int nodeIndex, char* id);
int DLLEXPORT ENR_getLinkID(ENResultsAPI* enrapi, int linkIndex, char* id);


float* ENR_newOutValueSeries(ENResultsAPI* enrapi, int seriesStart,
        int seriesLength, int* length, int* errcode);
float* ENR_newOutValueArray(ENResultsAPI* enrapi, ENR_ApiFunction func,
        ENR_ElementType type, int* length, int* errcode);

int DLLEXPORT ENR_getNodeSeries(ENResultsAPI* enrapi, int nodeIndex, ENR_NodeAttribute attr,
        int timeIndex, int length, float* outValueSeries, int* len);
int DLLEXPORT ENR_getLinkSeries(ENResultsAPI* enrapi, int linkIndex, ENR_LinkAttribute attr,
        int timeIndex, int length, float* outValueSeries);

int DLLEXPORT ENR_getNodeAttribute(ENResultsAPI* enrapi, int timeIndex,
        ENR_NodeAttribute attr, float* outValueArray);
int DLLEXPORT ENR_getLinkAttribute(ENResultsAPI* enrapi, int timeIndex,
        ENR_LinkAttribute attr, float* outValueArray);

int DLLEXPORT ENR_getNodeResult(ENResultsAPI* enrapi, int timeIndex, int nodeIndex,
        float* outValueArray);
int DLLEXPORT ENR_getLinkResult(ENResultsAPI* enrapi, int timeIndex, int linkIndex,
        float* outValueArray);

int DLLEXPORT ENR_free(float *array);
int DLLEXPORT ENR_close(ENResultsAPI **enrapi);
int DLLEXPORT ENR_errMessage(int errcode, char* errmsg, int n);


#endif /* OUTPUTAPI_H_ */


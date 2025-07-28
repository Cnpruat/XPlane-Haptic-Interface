// Simple widget-based plugin for X-Plane 11/12
// Opens a window with buttons to trigger failures or weather changes.

#include "XPLMDisplay.h"
#include "XPLMGraphics.h"
#include "XPLMDataAccess.h"
#include "XPLMMenus.h"
#include "XPWidgets.h"
#include "XPStandardWidgets.h"

#include <string.h>

static int menuItemFlag = 0;
static XPLMMenuID menuID;

static XPWidgetID mainWidget;
static XPWidgetID labelFailures, labelWeather;

// Failure/weather buttons
static XPWidgetID buttonFailEngines, buttonBirdStrike;
static XPWidgetID buttonFailFlapLeft, buttonFailFlapRight;
static XPWidgetID buttonFailAileronLeft, buttonFailAileronRight;
static XPWidgetID buttonFailRudder;
static XPWidgetID buttonFailElevatorLeft, buttonFailElevatorRight;
static XPWidgetID buttonResetControls;

static XPWidgetID buttonTurbulence, buttonStopTurbulence;
static XPWidgetID buttonClear, buttonOvercast, buttonRain, buttonStorm, buttonWindy;

// Failure-related DataRefs
static XPLMDataRef drEngine1Fail, drEngine2Fail, drBirdStrike;

static XPLMDataRef drFlapFailLeft, drFlapFailRight;
static XPLMDataRef drAileronFailLeft, drAileronFailRight;
static XPLMDataRef drRudderFail;
static XPLMDataRef drElevatorFailLeft, drElevatorFailRight;

// Weather-related DataRefs
static XPLMDataRef drTurbulence, drTurb1, drTurb2, drTurb3;
static XPLMDataRef drRain0, drRain1, drStorm;
static XPLMDataRef drCloudCover0, drCloudCover1, drCloudCover2, drCloudCover3;
static XPLMDataRef drVisibility0, drVisibility1;
static XPLMDataRef drWindSpeed0, drWindSpeed1, drWindSpeed2;

static float MAX_intensity = 10.0f;
static float MIN_intensity = 0.0f;

static float MAX_wind = 80.0f;
static float MID_wind = 40.0f;
static float MIN_wind = 0.0f;

static float MAX_cloud = 1.0f;
static float MID_cloud = 0.5f;
static float MIN_cloud = 0.0f;

void CreateMainWindow(int x, int y, int width, int height) {
    int x2 = x + width;
    int y2 = y - height;

    mainWidget = XPCreateWidget(x, y, x2, y2, 1, "XPlane Control Panel", 1, NULL, xpWidgetClass_MainWindow);
    XPSetWidgetProperty(mainWidget, xpProperty_MainWindowHasCloseBoxes, 1);

    // Labels
    labelFailures = XPCreateWidget(x + 20, y - 30, x + 300, y - 50, 1, "--- Failures ---", 0, mainWidget, xpWidgetClass_Caption);
    labelWeather = XPCreateWidget(x + 20, y - 320, x + 300, y - 340, 1, "--- Weather Conditions ---", 0, mainWidget, xpWidgetClass_Caption);

    // Failure buttons
    buttonFailEngines = XPCreateWidget(x + 20, y - 60, x + 150, y - 100, 1, "Fail Engines", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonFailEngines, xpProperty_ButtonType, xpPushButton);

    buttonBirdStrike = XPCreateWidget(x + 160, y - 60, x + 300, y - 100, 1, "Bird Strike", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonBirdStrike, xpProperty_ButtonType, xpPushButton);

    buttonFailFlapLeft = XPCreateWidget(x + 20, y - 110, x + 150, y - 150, 1, "Fail Flap Left", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonFailFlapLeft, xpProperty_ButtonType, xpPushButton);

    buttonFailFlapRight = XPCreateWidget(x + 160, y - 110, x + 300, y - 150, 1, "Fail Flap Right", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonFailFlapRight, xpProperty_ButtonType, xpPushButton);

    buttonFailAileronLeft = XPCreateWidget(x + 20, y - 160, x + 150, y - 200, 1, "Fail Aileron Left", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonFailAileronLeft, xpProperty_ButtonType, xpPushButton);

    buttonFailAileronRight = XPCreateWidget(x + 160, y - 160, x + 300, y - 200, 1, "Fail Aileron Right", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonFailAileronRight, xpProperty_ButtonType, xpPushButton);

    buttonFailRudder = XPCreateWidget(x + 20, y - 260, x + 150, y - 300, 1, "Fail Rudder", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonFailRudder, xpProperty_ButtonType, xpPushButton);

    buttonFailElevatorLeft = XPCreateWidget(x + 20, y - 210, x + 150, y - 250, 1, "Fail Elevator Left", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonFailElevatorLeft, xpProperty_ButtonType, xpPushButton);

    buttonFailElevatorRight = XPCreateWidget(x + 160, y - 210, x + 300, y - 250, 1, "Fail Elevator Right", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonFailElevatorRight, xpProperty_ButtonType, xpPushButton);

    buttonResetControls = XPCreateWidget(x + 160, y - 260, x + 300, y - 300, 1, "Reset Failures", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonResetControls, xpProperty_ButtonType, xpPushButton);

    // Weather buttons
    buttonTurbulence = XPCreateWidget(x + 20, y - 370, x + 150, y - 380, 1, "Add Turbulence", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonTurbulence, xpProperty_ButtonType, xpPushButton);

    buttonStopTurbulence = XPCreateWidget(x + 160, y - 370, x + 300, y - 380, 1, "Stop Turbulence", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonStopTurbulence, xpProperty_ButtonType, xpPushButton);

    buttonClear = XPCreateWidget(x + 90, y - 520, x + 230, y - 530, 1, "Clear Skies", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonClear, xpProperty_ButtonType, xpPushButton);

    buttonOvercast = XPCreateWidget(x + 160, y - 420, x + 300, y - 430, 1, "Overcast", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonOvercast, xpProperty_ButtonType, xpPushButton);

    buttonRain = XPCreateWidget(x + 20, y - 470, x + 150, y - 480, 1, "Rainy Weather", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonRain, xpProperty_ButtonType, xpPushButton);

    buttonStorm = XPCreateWidget(x + 160, y - 470, x + 300, y - 480, 1, "Stormy Weather", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonStorm, xpProperty_ButtonType, xpPushButton);

    buttonWindy = XPCreateWidget(x + 20, y - 420, x + 150, y - 430, 1, "Windy Weather", 0, mainWidget, xpWidgetClass_Button);
    XPSetWidgetProperty(buttonWindy, xpProperty_ButtonType, xpPushButton);

    XPAddWidgetCallback(mainWidget, [](XPWidgetMessage msg, XPWidgetID widget, intptr_t param1, intptr_t param2) -> int {
        if (msg == xpMessage_CloseButtonPushed) {
            XPHideWidget(mainWidget);
            return 1;
        }

        if (msg == xpMsg_PushButtonPressed) {
            if (param1 == (intptr_t)buttonFailEngines) {
                XPLMSetDatai(drEngine1Fail, 6);
                XPLMSetDatai(drEngine2Fail, 6);
                return 1;
            }
            if (param1 == (intptr_t)buttonBirdStrike) {
                XPLMSetDatai(drBirdStrike, 6);
                return 1;
            }
            if (param1 == (intptr_t)buttonFailFlapLeft) {
                XPLMSetDatai(drFlapFailLeft, 6);
                return 1;
            }
            if (param1 == (intptr_t)buttonFailFlapRight) {
                XPLMSetDatai(drFlapFailRight, 6);
                return 1;
            }
            if (param1 == (intptr_t)buttonFailAileronLeft) {
                XPLMSetDatai(drAileronFailLeft, 6);
                return 1;
            }
            if (param1 == (intptr_t)buttonFailAileronRight) {
                XPLMSetDatai(drAileronFailRight, 6);
                return 1;
            }
            if (param1 == (intptr_t)buttonFailRudder) {
                XPLMSetDatai(drRudderFail, 6);
                return 1;
            }
            if (param1 == (intptr_t)buttonFailElevatorLeft) {
                XPLMSetDatai(drElevatorFailLeft, 6);
                return 1;
            }
            if (param1 == (intptr_t)buttonFailElevatorRight) {
                XPLMSetDatai(drElevatorFailRight, 6);
                return 1;
            }
            if (param1 == (intptr_t)buttonResetControls) {
                // Reset all failures on engines
                XPLMSetDatai(drBirdStrike, 0);
                XPLMSetDatai(drEngine1Fail, 0);
                XPLMSetDatai(drEngine2Fail, 0);

                // Reset all failures on control surfaces
                XPLMSetDatai(drFlapFailLeft, 0);
                XPLMSetDatai(drFlapFailRight, 0);

                XPLMSetDatai(drAileronFailLeft, 0);
                XPLMSetDatai(drAileronFailRight, 0);

                XPLMSetDatai(drRudderFail, 0);

                XPLMSetDatai(drElevatorFailLeft, 0);
                XPLMSetDatai(drElevatorFailRight, 0);
                return 1;
            }
            if (param1 == (intptr_t)buttonTurbulence) {
                XPLMSetDatavf(drTurbulence, &MAX_intensity, 0, 13);
                XPLMSetDataf(drTurb1, 10);
                XPLMSetDataf(drTurb2, 10);
                XPLMSetDataf(drTurb3, 10);
                return 1;
            }
            if (param1 == (intptr_t)buttonStopTurbulence) {
                XPLMSetDatavf(drTurbulence, &MIN_intensity, 0, 13);
                XPLMSetDataf(drTurb1, 0);
                XPLMSetDataf(drTurb2, 0);
                XPLMSetDataf(drTurb3, 0);
                return 1;
            }
            if (param1 == (intptr_t)buttonClear) {
                float zero = 0.0f, fullVis = 50000.0f;
                XPLMSetDataf(drRain0, zero);
                XPLMSetDataf(drRain1, zero);
                XPLMSetDataf(drStorm, zero);

                XPLMSetDataf(drCloudCover0, 0.0f);
                XPLMSetDataf(drCloudCover1, 0.0f);
                XPLMSetDataf(drCloudCover2, 0.0f);
                XPLMSetDatavf(drCloudCover3, &MIN_cloud, 0, 3);

                XPLMSetDataf(drWindSpeed0, 0.0f);
                XPLMSetDataf(drWindSpeed1, 0.0f);
                XPLMSetDatavf(drWindSpeed2, &MIN_wind, 0, 13);

                XPLMSetDataf(drVisibility0, fullVis);
                XPLMSetDataf(drVisibility1, 35.0f);
                return 1;
            }
            if (param1 == (intptr_t)buttonOvercast) {
                XPLMSetDataf(drCloudCover0, 1.0f);
                XPLMSetDataf(drCloudCover1, 1.0f);
                XPLMSetDataf(drCloudCover2, 1.0f);
                XPLMSetDatavf(drCloudCover3, &MID_cloud, 0, 3);
                return 1;
            }
            if (param1 == (intptr_t)buttonRain) {
                XPLMSetDataf(drRain0, 1.0f);
                XPLMSetDataf(drRain1, 1.0f);

                XPLMSetDataf(drCloudCover0, 0.9f);
                XPLMSetDataf(drCloudCover1, 0.9f);
                XPLMSetDatavf(drCloudCover3, &MID_cloud, 0, 3);

                XPLMSetDataf(drVisibility0, 2000.0f);
                XPLMSetDataf(drVisibility1, 1.25f);
                return 1;
            }
            if (param1 == (intptr_t)buttonStorm) {
                XPLMSetDataf(drStorm, 1.0f);
                XPLMSetDataf(drRain0, 1.0f);
                XPLMSetDataf(drRain1, 1.0f);

                XPLMSetDataf(drCloudCover0, 1.0f);
                XPLMSetDatavf(drCloudCover3, &MAX_cloud, 0, 3);

                XPLMSetDataf(drVisibility0, 1500.0f);
                XPLMSetDataf(drVisibility1, 1.0f);

                XPLMSetDataf(drWindSpeed0, 25.0f);
                XPLMSetDataf(drWindSpeed1, 30.0f);
                XPLMSetDatavf(drWindSpeed2, &MID_wind, 0, 13);
                return 1;
            }
            if (param1 == (intptr_t)buttonWindy) {
                XPLMSetDataf(drWindSpeed0, 35.0f);
                XPLMSetDataf(drWindSpeed1, 40.0f);
                XPLMSetDatavf(drWindSpeed2, &MAX_wind, 0, 13);
                return 1;
            }
        }

        return 0;
        });
}

void MenuHandler(void*, void* ref) {
    if (strcmp((char*)ref, "Open") == 0) {
        if (menuItemFlag == 0) {
            CreateMainWindow(10, 1000, 320, 625);
            menuItemFlag = 1;
        }
        else if (!XPIsWidgetVisible(mainWidget)) {
            XPShowWidget(mainWidget);
        }
    }
}

PLUGIN_API int XPluginStart(char* outName, char* outSig, char* outDesc) {
    strcpy(outName, "ControlPanel");
    strcpy(outSig, "IISRI.pBourrandy.controlpanel");
    strcpy(outDesc, "Control panel to trigger failures and weather.");

    int item = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Control Panel", NULL, 0);
    menuID = XPLMCreateMenu("Control Panel", XPLMFindPluginsMenu(), item, MenuHandler, NULL);
    XPLMAppendMenuItem(menuID, "Open", (void*)"Open", 1);

    // Failure DataRefs
    drEngine1Fail = XPLMFindDataRef("sim/operation/failures/rel_engfai0");
    drEngine2Fail = XPLMFindDataRef("sim/operation/failures/rel_engfai1");
    drBirdStrike = XPLMFindDataRef("sim/operation/failures/rel_bird_strike_eng2");

    drFlapFailLeft = XPLMFindDataRef("sim/operation/failures/rel_fcon_flap_1_lft_lock");
    drFlapFailRight = XPLMFindDataRef("sim/operation/failures/rel_fcon_flap_1_rgt_lock");

    drAileronFailLeft = XPLMFindDataRef("sim/operation/failures/rel_fcon_ailn_1_lft_lock");
    drAileronFailRight = XPLMFindDataRef("sim/operation/failures/rel_fcon_ailn_1_rgt_lock");

    drElevatorFailLeft = XPLMFindDataRef("sim/operation/failures/rel_fcon_elev_1_lft_lock");
    drElevatorFailRight = XPLMFindDataRef("sim/operation/failures/rel_fcon_elev_1_rgt_lock");

    drRudderFail = XPLMFindDataRef("sim/operation/failures/rel_fcon_rudd_1_ctr_lock");

    // Weather DataRefs
    drTurbulence = XPLMFindDataRef("sim/weather/region/turbulence");
    drTurb1 = XPLMFindDataRef("sim/weather/turbulence[0]");
    drTurb2 = XPLMFindDataRef("sim/weather/turbulence[1]");
    drTurb3 = XPLMFindDataRef("sim/weather/turbulence[2]");

    drRain0 = XPLMFindDataRef("sim/weather/rain_percent");
    drRain1 = XPLMFindDataRef("sim/weather/region/rain_percent");
    drStorm = XPLMFindDataRef("sim/weather/thunderstorm_percent");

    drCloudCover0 = XPLMFindDataRef("sim/weather/cloud_coverage[0]");
    drCloudCover1 = XPLMFindDataRef("sim/weather/cloud_coverage[1]");
    drCloudCover2 = XPLMFindDataRef("sim/weather/cloud_coverage[2]");
    drCloudCover3 = XPLMFindDataRef("sim/weather/region/cloud_coverage_percent");

    drVisibility0 = XPLMFindDataRef("sim/weather/visibility_reported_m");
    drVisibility1 = XPLMFindDataRef("sim/weather/region/visibility_reported_sm");

    drWindSpeed0 = XPLMFindDataRef("sim/weather/wind_speed_kt[0]");
    drWindSpeed1 = XPLMFindDataRef("sim/weather/wind_speed_kt[1]");
    drWindSpeed2 = XPLMFindDataRef("sim/weather/region/wind_speed_msc");

    CreateMainWindow(10, 1000, 320, 625);
    menuItemFlag = 1;
    return 1;
}

PLUGIN_API void XPluginStop(void) {
    XPLMDestroyMenu(menuID);
    if (menuItemFlag) {
        XPDestroyWidget(mainWidget, 1);
        menuItemFlag = 0;
    }
}

PLUGIN_API void XPluginDisable(void) {}
PLUGIN_API int  XPluginEnable(void) { return 1; }
PLUGIN_API void XPluginReceiveMessage(XPLMPluginID inFrom, int inMsg, void* inParam) {}

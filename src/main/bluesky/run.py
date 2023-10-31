#!/usr/bin/env python
""" Main BlueSky start script """
import sys
from bluesky.__main__ import main


def cmddict():
    stackdict = {
        "ADDNODES": [
            "ADDNODES number",
            "",
        ],
        "AIRWAY": [
            "AIRWAY wp/airway",
        ],
        "ATALT": [
            "acid ATALT alt cmd ",
        ],
        "ATDIST": [
            "acid ATDIST pos dist cmd ",
        ],
        "ATSPD": [
            "acid ATSPD spd cmd ",
        ],
        "BANK": [
            "BANK acid bankangle[deg]",
        ],
        "BATCH": [
            "BATCH filename",
        ],
        "BLUESKY": [
            "BLUESKY",
        ],
        "BENCHMARK": [
            "BENCHMARK [scenfile,time]",
        ],
        "BOX": [
            "BOX name,lat,lon,lat,lon,[top,bottom]",
        ],
        "CALC": [
            "CALC expression",
        ],
        "CASMACHTHR": [
            "CASMACHTHR threshold",
        ],
        "CD": [
            "CD [path]",
        ],
        "CIRCLE": [
            "CIRCLE name,lat,lon,radius,[top,bottom]",
        ],
        "CLRCRECMD": [
            "CLRCRECMD",
        ],
        "COLOR": [
            "COLOR name,color (named color or r,g,b)",
        ],
        "CRE": [
            "CRE acid,type,lat,lon,hdg,alt,spd",
        ],
        "CRECMD": [
            "CRECMD cmdline (to be added after a/c id )",
        ],
        "CRECONFS": [
            "CRECONFS id, type, targetid, dpsi, cpa, tlos_hor, dH, tlos_ver, spd",
        ],
        "DATE": [
            "DATE [day,month,year,HH:MM:SS.hh]",
        ],
        "DEFWPT": [
            "DEFWPT wpname,lat,lon,[FIX/VOR/DME/NDB]",
        ],
        "DEL": [
            "DEL acid/ALL/WIND/shape",
        ],
        "DIST": [
            "DIST lat0, lon0, lat1, lon1",
        ],
        "DOC": [
            "DOC [command]",
        ],
        "DT": [
            "DT [dt] OR [target,dt]",
        ],
        "DTMULT": [
            "DTMULT multiplier",
        ],
        "ECHO": [
            "ECHO txt",
        ],
        "FF": [
            "FF [timeinsec]",
        ],
        "FILTERALT": [
            "FILTERALT ON/OFF,[bottom,top]",
        ],
        "FIXDT": [
            "FIXDT ON/OFF [tend]",
        ],
        "GROUP": [
            "GROUP [grname, (areaname OR acid,...) ]",
        ],
        "HOLD": [
         "HOLD"
        ],
        "IMPLEMENTATION": [
            "IMPLEMENTATION [base, implementation]",
        ],
        "INSEDIT": [
            "INSEDIT txt",
        ],
        "LEGEND": [
            "LEGEND label1, ..., labeln",
        ],
        "LINE": [
            "LINE name,lat,lon,lat,lon",
        ],
        "LSVAR": [
            "LSVAR path.to.variable",
        ],
        "MAGVAR": [
            "MAGVAR lat,lon",
        ],
        "MCRE": [
            "MCRE n, [type/*, alt/*, spd/*, dest/*]",
        ],
        "MOVE": [
            "MOVE acid,lat,lon,[alt,hdg,spd,vspd]",
        ],
        "ND": [
            "ND acid",
        ],
        "NOISE": [
            "NOISE [ON/OFF]",
        ],
        "OP": [
            "OP",
        ],
        "PAN": [
            "PAN latlon/acid/airport/waypoint/LEFT/RIGHT/ABOVE/DOWN",
        ],
        "PLOT": [
            "PLOT [x], y [,dt,color,figure]",
        ],
        "POLY": [
            "POLY name,[lat,lon,lat,lon, ...]",
        ],
        "POLYALT": [
            "POLYALT name,top,bottom,lat,lon,lat,lon, ...",
        ],
        "POLYLINE": [
            "POLYLINE name,lat,lon,lat,lon,...",
        ],
        "POS": [
            "POS acid/waypoint",
        ],
        "QUIT": [
         "QUIT"
        ],
        "REALTIME": [
            "REALTIME [ON/OFF]",
        ],
        "RESET": [
            "RESET"
        ],
        "SEED": [
            "SEED value",
        ],
        "SSD": [
            "SSD ALL/CONFLICTS/OFF or SSD acid0, acid1, ...",
        ],
        "SWRAD": [
            "SWRAD GEO/GRID/APT/VOR/WPT/LABEL/ADSBCOVERAGE/TRAIL/POLY [dt]/[value]",
        ],
        "SYMBOL": ["SYMBOL"],
        "THR": [
            "THR acid, IDLE/0.0/throttlesetting/1.0/AUTO(default)",
        ],
        "TIME": [
            "TIME RUN(default) / HH:MM:SS.hh / REAL / UTC ",
        ],
        "TRAIL": [
            "TRAIL ON/OFF, [dt] OR TRAIL acid color",
        ],
        "UNGROUP": [
            "UNGROUP grname, acid",
        ],
        "ZOOM": [
            "ZOOM IN/OUT or factor",
        ]
    }
    print(stackdict)


# cmddict()
if __name__ == "__main__":
    # Run mainloop if BlueSky is called directly
    sys.exit(main())

# --------------------------------------------------------------------
# Prototype gain control
# Capstone I
# --------------------------------------------------------------------
# NOTES:
"""
  -Volume and Pan can be implemented very easy in the same function.
  -
"""
# --------------------------------------------------------------------


# --------------------------------------------------------------------
# GAIN CONTROL - 
# --------------------------------------------------------------------
# GetTrack(int project number, int track number)
selected_track = RPR_GetTrack(0, 0)# Get track number(0 = 1st track)
vol = RPR_GetTrackUIVolPan(selected_track, 0, 0)[0] # Get volume of track

# Set track volume to half of current volume
RPR_SetMediaTrackInfo_Value(selected_track, "D_VOL", vol*0.5)

# RPR_SetMediaTrackInfo_Value(selected_track, "D_VOL", vol + hand_loc)

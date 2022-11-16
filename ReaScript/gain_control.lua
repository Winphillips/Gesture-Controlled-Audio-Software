-- ------------------------------------------
-- Protoype Gain Control and Track selection
-- Captsone I
-- ------------------------------------------
-- NOTES: 
-- Vol & Pan can be changed in same function
-- 
-- ------------------------------------------
-- GAIN CONTROL
-- ------------------------------------------
-- Select track (0 = first num)
track = reaper.GetTrack(0, 2) --(project, track)
-- reaper.ShowConsoleMsg(tostring(track))

-- Get (retval, vol, pan)
ok, volume, pan = reaper.GetTrackUIVolPan(track, 0, 0)

--Set track 1 volume to half of current volume
reaper.SetMediaTrackInfo_Value(track, "D_VOL", volume*0.5)

if volume < 1 then
  reaper.SetMediaTrackInfo_Value(track, "D_VOL", 4) --12.04 dB
end

-- Possible implementation
-- RPR_SetMediaTrackInfo_Value(track, "D_VOL", volume + file_name.hand_location)

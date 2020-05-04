@echo off
wmic path Win32_PnPEntity where "Service='monitor' and Status='OK'" get DeviceID /VALUE | find /C "="
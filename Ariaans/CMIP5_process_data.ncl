;*************************************************
; CMIP5_process_data.ncl
;
; Regrid to 2x2
; Restrict to dates of interest
; Calculate climo 
; Calculate monmean files if daily
; Check dates are ok
; AFP 25 February 2014, updated 1 July 2014
;************************************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;************************************************
begin

dataLoc = "Data/" 
myScenario = "rcp85"; "hist_rcp85"; "historical";  "piControl"; 
if (myScenario .eq. "historical")
	yrFirst = 1861
	yrLast = 2005
end if 
if ( (myScenario .eq. "rcp45") .or. (myScenario .eq. "rcp85") )
	yrFirst = 2006
	yrLast = 2100
end if  
if (myScenario .eq. "hist_rcp85")
	yrFirst = 1861
	yrLast = 2100
end if  
fileDate = "140805" ; date of file list
modelList = asciiread("Data/CMIP5_OImon/CMIP5_OImon_master_list_" + fileDate + ".txt",-1,"string")
delim = ","

do ivar = 1,1
	if (ivar .eq. 0)
		myVar = "sic"
		varType = "OImon"
	end if
	if (ivar .eq. 1)
		myVar = "so"; "tos"; "sos"; "thetao";
		varType = "Omon"
	end if
	if (ivar .eq. 2)
		myVar = "psl"; "tauu";
		varType = "Amon"
	end if
	if (ivar .eq. 3)
		myVar = "ua"
		varType = "Amon"
	end if
	if (ivar .eq. 4)
		myVar = "pr"
		varType = "Amon"
	end if
	if (ivar .eq. 5)
		myVar = "clt"
		varType = "Amon"
	end if

	print("********** " + myVar + " **********")

	;************************************************
	; Check which files are ready / done
	;************************************************
	checkFilesOnly = 0
	if (checkFilesOnly .eq. 1)
		do imodel = 0, dimsizes(modelList) - 1
			model = str_get_field(modelList(imodel), 1, delim)
			run = str_get_field(modelList(imodel), 2, delim)
			fileStrDates = dataLoc + "CMIP5_" + varType + "/" + myVar + "/" + myScenario + "/formatted/" + myVar + "_" + varType + "_" + model + "_" + myScenario + "_" + run + "_" + yrFirst + "-" + yrLast + "_r180x90.nc"
			if (.not. isfilepresent(fileStrDates))
				print("Missing: " + model + ", " + run)
			end if
			delete([/model, run, fileStrDates/])
		end do ; imodel loop
	end if

	;************************************************
	; Print out native resolution
	;************************************************
	resPrint = 0
	if (resPrint .eq. 1)
		do imodel = 0, dimsizes(modelList) - 1
			model = str_get_field(modelList(imodel), 1, delim)
			run = str_get_field(modelList(imodel), 2, delim)
			fileStrNcrcat = dataLoc + "CMIP5_" + varType + "/" + myVar + "/" + myScenario + "/ncrcat/" + myVar + "_" + varType + "_" + model + "_" + myScenario + "_" + run + "_*.nc"
			fileIn = systemfunc("ls " + fileStrNcrcat)
			in = addfile(fileIn, "r")
			numLat = dimsizes(in->lat)
			numLon = dimsizes(in->lon)
			print(model + ", " + run + ": lat = " + numLat + ", lon = " + numLon)
			delete([/model, run, fileStrNcrcat, fileIn, in, numLat, numLon/])
		end do ; imodel loop
	end if

	;************************************************
	; Process 1 - remap, dates, climo
	;************************************************
	process1 = 0
	if (process1 .eq. 1)
		do imodel = 0, dimsizes(modelList) - 1
			model = str_get_field(modelList(imodel), 1, delim)
			run = str_get_field(modelList(imodel), 2, delim)
			print("")
			print(model + ", " + run)

			if (myScenario .ne. "piControl")
				fileStrNcrcat = dataLoc + "CMIP5_" + varType + "/" + myVar + "/" + myScenario + "/ncrcat/" + myVar + "_" + varType + "_" + model + "_" + myScenario + "_" + run + "_*.nc"
				; tauu and tauv
				if ( (myVar .eq. "tauu") .or. (myVar .eq. "tauv") )
					fileStrNcrcat = "/data/cow083/CMIP5/atmos/" + myScenario + "/mon/" + myVar + "/" + myVar + "_Amon_" + model + "_" + myScenario + "_" + run + "*.nc"
				end if
				fileStrRemap = dataLoc + "CMIP5_" + varType + "/" + myVar + "/" + myScenario + "/remap/" + myVar + "_" + varType + "_" + model + "_" + myScenario + "_" + run + "_r180x90.nc"
				fileStrDates = dataLoc + "CMIP5_" + varType + "/" + myVar + "/" + myScenario + "/formatted/" + myVar + "_" + varType + "_" + model + "_" + myScenario + "_" + run + "_" + yrFirst + "-" + yrLast + "_r180x90.nc"
				fileStrVertInt = dataLoc + "CMIP5_" + varType + "/" + myVar + "/" + myScenario + "/formatted/" + myVar + "_" + varType + "_" + model + "_" + myScenario + "_" + run + "_" + yrFirst + "-" + yrLast + "_r180x90_40lev.nc"

				if (isfilepresent(fileStrRemap))	
					print("Don't need to remap")
				else
					print("Remapping netcdf files...")
					system("cdo remapbil,r180x90 " + fileStrNcrcat + " " + fileStrRemap)
				end if

				if (isfilepresent(fileStrDates))	
					print("Restricted dates file exists")
				else
					print("Calculating restricted dates netcdf files...")
					system("cdo selyear," + yrFirst + "/" + yrLast + " " + fileStrRemap + " " + fileStrDates)
				end if

				;if (isfilepresent(fileStrVertInt))	
				;	print("Vertically interpolated file is present is present")
				;else
				;	print("Vertically interpolating...")
				;	system("cdo intlevel,5.01,15.07,25.28,35.76,46.61,57.98,70.02,82.92,96.92,112.32,129.49,148.96,171.4,197.79,229.48,268.46,317.65,381.39,465.91,579.31,729.35,918.37,1139.15,1378.57,1625.7,1875.11,2125.01,2375,2625,2875,3125,3375,3625,3875,4125,4375,4625,4875,5125,5375 " + fileStrDates + " " + fileStrVertInt)
				;end if

				delete([/model, run, fileStrNcrcat, fileStrRemap, fileStrDates, fileStrVertInt/])
			else
				run = "r1i1p1"
				fileStrNcrcat = dataLoc + "CMIP5_" + varType + "/" + myVar + "/" + myScenario + "/ncrcat/" + myVar + "_" + varType + "_" + model + "_" + myScenario + "_" + run + "_*.nc"
				fileStrRemap = dataLoc + "CMIP5_" + varType + "/" + myVar + "/" + myScenario + "/remap/" + myVar + "_" + varType + "_" + model + "_" + myScenario + "_" + run + "_r180x90.nc"

				if (isfilepresent(fileStrRemap))	
					print("Don't need to remap")
				else
					print("Remapping netcdf files...")
					system("cdo remapbil,r180x90 " + fileStrNcrcat + " " + fileStrRemap)
				end if

				delete([/model, run, fileStrNcrcat, fileStrRemap/])
			end if ; piControl loop

		end do ; imodel loop
	end if ; process1 loop

	;************************************************
	; Process 2 - concat scenarios, seasonal
	;************************************************
	process2 = 1
	if (process2 .eq. 1) 
		do imodel = 0, dimsizes(modelList) - 1
			model = str_get_field(modelList(imodel), 1, delim)
			run = str_get_field(modelList(imodel), 2, delim)
			print("")
			print(model + ", " + run)

			if (varType .eq. "day")
				varType2 = "monmean"
			else
				varType2 = varType
			end if
			fileStrHist = dataLoc + "CMIP5_" + varType + "/" + myVar + "/historical/formatted/" + myVar + "_" + varType2 + "_" + model + "_historical_" + run + "_1861-2005_r180x90.nc"
			;fileStrHist = dataLoc + "CMIP5_" + varType + "/" + myVar + "/historical/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_1861-2100_r180x90_40lev.nc"
			fileStrRcp = dataLoc + "CMIP5_" + varType + "/" + myVar + "/rcp85/formatted/" + myVar + "_" + varType2 + "_" + model + "_rcp85_" + run + "_2006-2100_r180x90.nc"
			;fileStrRcp = dataLoc + "CMIP5_" + varType + "/" + myVar + "/rcp85/formatted/" + myVar + "_" + varType2 + "_" + model + "_rcp85_" + run + "_2006-2100_r180x90_40lev.nc"
			fileStrNcrcat = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_1861-2100_r180x90.nc"
			;fileStrNcrcat = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_1861-2100_r180x90_40lev.nc"
			fileStrVertInt = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_1861-2100_r180x90_40lev.nc"
			fileStrANN = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/seasons/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_ANN_1861-2100_r180x90.nc"
			fileStrMAM = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/seasons/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_MAM_1861-2100_r180x90.nc"
			fileStrJJA = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/seasons/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_JJA_1861-2100_r180x90.nc"
			fileStrSON = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/seasons/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_SON_1861-2100_r180x90.nc"
			fileStrDJF = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/seasons/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_DJF_1861-2100_r180x90.nc"
			fileStrANNZm = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/zonal/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_ANN_1861-2100_r180x90_zm.nc"
			fileStrMAMZm = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/zonal/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_MAM_1861-2100_r180x90_zm.nc"
			fileStrJJAZm = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/zonal/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_JJA_1861-2100_r180x90_zm.nc"
			fileStrSONZm = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/zonal/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_SON_1861-2100_r180x90_zm.nc"
			fileStrDJFZm = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/zonal/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_DJF_1861-2100_r180x90_zm.nc"

			fileStrANNshift = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/seasons/" + myVar + "_" + varType2 + "_" + model + "_hist_rcp85_" + run + "_ANN_shifttime_8mo_1861-2100_r180x90.nc"

		if ( (isfilepresent(fileStrHist)) .and. (isfilepresent(fileStrRcp)) )
		;if (isfilepresent(fileStrNcrcat))

			if (isfilepresent(fileStrNcrcat))	
				print("Don't need to concatenate")
			else
				print("Concatenating netcdf files...")
				system("ncrcat " + fileStrHist + " " + fileStrRcp + " " + fileStrNcrcat)
			end if

			;if (isfilepresent(fileStrVertInt))	
			;	print("Vertically interpolated file is present is present")
			;else
			;	print("Vertically interpolating...")
			;	system("cdo intlevel,5.01,15.07,25.28,35.76,46.61,57.98,70.02,82.92,96.92,112.32,129.49,148.96,171.4,197.79,229.48,268.46,317.65,381.39,465.91,579.31,729.35,918.37,1139.15,1378.57,1625.7,1875.11,2125.01,2375,2625,2875,3125,3375,3625,3875,4125,4375,4625,4875,5125,5375 " + fileStrNcrcat + " " + fileStrVertInt)
			;end if
			fileStrVertInt = fileStrNcrcat

			if (isfilepresent(fileStrANN))	
				print("Annual file is present")
			else
				print("Calculating annual mean...")
				system("cdo yearmean " + fileStrVertInt + " " + fileStrANN)
			end if

			if (isfilepresent(fileStrMAM))	
				print("MAM file is present")
			else
				print("Calculating MAM mean...")
				system("cdo yearmean -selseas,MAM " + fileStrVertInt + " " + fileStrMAM)
			end if

			if (isfilepresent(fileStrJJA))	
				print("JJA file is present")
			else
				print("Calculating JJA mean...")
				system("cdo yearmean -selseas,JJA " + fileStrVertInt + " " + fileStrJJA)
			end if

			if (isfilepresent(fileStrSON))	
				print("SON file is present")
			else
				print("Calculating SON mean...")
				system("cdo yearmean -selseas,SON " + fileStrVertInt + " " + fileStrSON)
			end if

			if (isfilepresent(fileStrDJF))	
				print("DJF file is present")
			else
				print("Calculating DJF mean...")
				fileStrDJFtemp = dataLoc + "CMIP5_" + varType + "/" + myVar + "/hist_rcp85/seasons/" + myVar + "_" + varType + "_" + model + "_hist_rcp85_" + run + "_DJF_1861-2100_r180x90+temp.nc"
				system("cdo selseas,DJF " + fileStrVertInt + " " + fileStrDJFtemp)
				system("cdo yearmean -shifttime,1mo " + fileStrDJFtemp + " " + fileStrDJF)
				system("rm " + fileStrDJFtemp)
				delete(fileStrDJFtemp)
			end if

			if (isfilepresent(fileStrANNZm))	
				print("Zonal mean file is present")
			else
				print("Calculating zonal mean...")
				system("cdo zonmean " + fileStrANN + " " + fileStrANNZm)
			end if

			if (isfilepresent(fileStrMAMZm))	
				print("Zonal mean file is present")
			else
				print("Calculating zonal mean...")
				system("cdo zonmean " + fileStrMAM + " " + fileStrMAMZm)
			end if

			if (isfilepresent(fileStrJJAZm))	
				print("Zonal mean file is present")
			else
				print("Calculating zonal mean...")
				system("cdo zonmean " + fileStrJJA + " " + fileStrJJAZm)
			end if

			if (isfilepresent(fileStrSONZm))	
				print("Zonal mean file is present")
			else
				print("Calculating zonal mean...")
				system("cdo zonmean " + fileStrSON + " " + fileStrSONZm)
			end if

			if (isfilepresent(fileStrDJFZm))	
				print("Zonal mean file is present")
			else
				print("Calculating zonal mean...")
				system("cdo zonmean " + fileStrDJF + " " + fileStrDJFZm)
			end if

			;if (isfilepresent(fileStrANNshift))	
			;	print("Annual shifttime file is present")
			;else
			;	print("Calculating annual mean...")
			;	system("cdo yearmean -shifttime,8mo " + fileStrVertInt + " " + fileStrANNshift)
			;end if

		end if ; isfilepresent loop

			delete([/model, run, varType2, fileStrHist, fileStrRcp, fileStrNcrcat, fileStrVertInt, fileStrDJF, fileStrMAM, fileStrJJA, fileStrSON, fileStrANN, fileStrANNZm, fileStrMAMZm, fileStrJJAZm, fileStrSONZm, fileStrDJFZm, fileStrANNshift/])
		end do ; imodel loop
	end if ; process2 loop 

	;************************************************
	; Check dates are ok
	;************************************************
	checkDates = 0
	if (checkDates .eq. 1)
		do imodel = 0, dimsizes(modelList) - 1
			model = str_get_field(modelList(imodel), 1, delim)
			run = str_get_field(modelList(imodel), 2, delim)
			print(model + ", " + run)
			fileStrDates = dataLoc + "CMIP5_" + varType + "/" + myVar + "/" + myScenario + "/formatted/" + myVar + "_" + varType + "_" + model + "_" + myScenario + "_" + run + "_" + yrFirst + "-" + yrLast + "_r180x90.nc"

			if (isfilepresent(fileStrDates)) ; for RCP8.5 SIC - don't have all models

			if (varType .eq. "day")
				in = addfile(fileStrDates, "r")
				time = in->time
				delete(in)
				YYYYMMDD = cd_calendar(time, 2)
				print("   " + YYYYMMDD(0))
				print("   " + YYYYMMDD(dimsizes(time)-1))
				print("   " + (dimsizes(time) - 365*95))
				print("   " + time@calendar)
				delete([/time, YYYYMMDD/])
			end if

			if ( (varType .eq. "Amon") .or. (varType .eq. "Omon") .or. (varType .eq. "OImon") )
				in = addfile(fileStrDates, "r")
				time = in->time
				delete(in)
				YYYYMMdble = cd_calendar(time, 1)/100.
				YYYYMMdble!0 = "YYYYMMtime"
				YYYYMM = dble2flt(YYYYMMdble)
				print("   " + dimsizes(YYYYMM))
				delete([/time, YYYYMMdble/])


				if (YYYYMM(0) .ne. (yrFirst + 0.01))
					print("   Error in first month: " + YYYYMM(0))
				end if

				if (YYYYMM(dimsizes(YYYYMM)-1) .ne. (yrLast + 0.12))
					print("   Error in last month: " + YYYYMM(dimsizes(YYYYMM)-1))
				end if

				if (dimsizes(YYYYMM) .ne. ((yrLast-yrFirst+1)*12))
					print("   Error in number of months: " + dimsizes(YYYYMM))
				end if

				do i = 1, dimsizes(YYYYMM) - 1
					diff = round((YYYYMM(i) - YYYYMM(i-1))*100., 1)/100.
					if (diff .ne. 0.01) 
						if (diff .ne. 0.89)
							print("   Error in order of months: " + i)
						end if
					end if
					delete(diff)
				end do
				delete(YYYYMM)
			end if

			end if ; isfilepresent loop

			delete([/model, run, fileStrDates/])
		end do ; imodel loop
	end if ; checkDates loop

end do ; ivar
end

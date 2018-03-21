;*************************************************
; CMIP5_allModel_IPO_EOF_pattern.ncl
;
; Read in IPO EOF patterns
; Plot maps in specific order (i.e. based on SIE trends as for other ordered figs)
; AFP 22 October 2015
;************************************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"   
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

;************************************************
begin	

  yrFirst = 1891
  yrLast = 2013
  neof = 0

  myVar1 = "sie1"
  alphaOrder = True

;************************************************
; Plot resources
;************************************************
  res                      = True     					; plot mods desired
  res@gsnDraw              = False               		; do not draw plot
  res@gsnFrame             = False               		; do not advance frome
  res@gsnAddCyclic         = True    					; data already has cyclic point

  res@mpMinLatF            = -90.      					; range to zoom in on
  res@mpMaxLatF            = 70.
  res@mpCenterLonF	       = 270
  res@gsnMajorLatSpacing   = 20              			; change maj lat tm spacing
  res@gsnMinorLatSpacing   = 20  
  res@gsnMajorLonSpacing   = 30              			; change maj lat tm spacing
  res@gsnMinorLonSpacing   = 30  
  res@txFontHeightF   	   = 0.03

  res@tmXBMinorThicknessF  = 0.7 						; change tm thickness to match
  res@tmYLMinorThicknessF  = 0.7 
  res@tmXBLabelsOn	       = False
  res@tmYLLabelsOn	       = False

  res@cnFillOn             = True     					; turn on color fill
  res@cnLinesOn            = False    					; turn of contour lines
  res@gsnSpreadColors      = True     					; use full range of color map
  res@cnLineLabelsOn       = False			        	; turn off line labels
  res@cnLevelSelectionMode = "ManualLevels"      		; set manual contour levels     
  res@cnFillDrawOrder      = "PreDraw"  				; Make sure map fill happens last
  res@mpFillAreaSpecifiers = (/"Land", "Water"/)
  res@lbLabelBarOn 	       = False

  res@tmBorderThicknessF   = 0.7						; change map border thickness
  res@tmXBMajorThicknessF  = 0.7 						; change tm thickness to match
  res@tmYLMajorThicknessF  = 0.7 
  res@mpGeophysicalLineThicknessF = 1.					; change border thickness, default 1

  res2 			           = True
  res2@gsnTickMarksOn      = False
  res2@gsnDraw		       = False
  res2@gsnFrame		       = False
  res2@cnLevelSelectionMode= "ExplicitLevels" 			; set manual contour levels
  res2@cnInfoLabelOn       = False       				; turn off info label
  res2@cnLineLabelsOn      = True       				; do not draw contour labels
  res2@cnMonoLineColor     = True
  res2@cnLevels 	       = 15
  res2@cnLineColor         = "Black" 
  res2@cnLineThicknessF    = 1.   

  res@gsnSpreadColorStart  = 2
  res@gsnSpreadColorEnd	   = 23   
  res@mpSpecifiedFillColors= (/"grey", "transparent"/) 
		
  res@cnMaxLevelValF 	   = 0.3
  res@cnMinLevelValF 	   = -0.3
  res@cnLevelSpacingF 	   = (res@cnMaxLevelValF - res@cnMinLevelValF)/20

  BlueDarkRed22b = (/ (/1,1,1/),\
(/0,0,0/),\
(/0.176470588, 0, 0.784313725/),\
(/0.141176471, 0, 0.847058824/),\
(/0.117647059, 0, 0.901960784/),\
(/0.094117647, 0.109803922, 0.968627451/),\
(/0.156862745, 0.341176471, 1/),\
(/0.239215686, 0.529411765, 1/),\
(/0.337254902, 0.690196078, 1/),\
(/0.458823529, 0.82745098, 1/),\
(/0.6, 0.917647059, 1/),\
(/0.737254902, 0.976470588, 1/),\
(/1, 1, 1/),\
(/1, 1, 1/),\
(/1, 0.945098039, 0.737254902/),\
(/1, 0.839215686, 0.6/),\
(/1, 0.674509804, 0.458823529/),\
(/1, 0.470588235, 0.337254902/),\
(/1, 0.239215686, 0.239215686/),\
(/0.968627451, 0.152941176, 0.207843137/),\
(/0.847058824, 0.082352941, 0.184313725/),\
(/0.784313725, 0, 0.156862745/),\
(/0.647058824, 0, 0.129411765/),\
(/0.588235294, 0, 0.066666667/) /)

  modelList = asciiread("Data/CMIP5_OImon/CMIP5_OImon_master_list_markers_noCESM1-CAM5-1-FV2_150909.txt",-1,"string")
  delim = ","
  in = addfile("$NCARG_ROOT/lib/ncarg/data/cdf/landsea.nc","r")
  lsdata = in->LSMASK 
  delete(in)

;*************************************************
; Determine order to plot panels in 
;*************************************************
var1all = new(dimsizes(modelList), float)
yrFirstOrder = 1979
yrLastOrder = 2013
mySeas = "ANN"
iseas = 4
sector1 = 0
jetVar1 = 0 	
do imodel = 0, dimsizes(modelList) - 1
	model = str_get_field(modelList(imodel), 1, delim)
	run = str_get_field(modelList(imodel), 2, delim)
	in = addfile("Output/201508_metrics/" + model + "_hist_rcp85_" + run + "_1861-2100_r180x90_metrics_150804.nc", "r")
	if ( (myVar1 .eq. "jetU1") .or. (myVar1 .eq. "jetU2") .or. (myVar1 .eq. "jetU3") )
		var1 = in->$myVar1$(iseas, sector1, jetVar1, :)
	else
		var1 = in->$myVar1$(iseas, sector1, :)
	end if
	time = ispan(1861, 2100, 1)
	ind1YYYY = ind(time.ge.yrFirstOrder .and. time.le.yrLastOrder)
	var1YYYY = var1(ind1YYYY)
	time1YYYY = time(ind1YYYY)
	gmt = in->tasAv1(4, 0, :)
	gmtRc = (/ regCoef(time1YYYY, gmt(ind1YYYY)) /)
	if (num(.not.ismissing(var1YYYY)) .gt. 14)
		var1rc = (/ regCoef(time1YYYY, var1YYYY) /)
		var1rc = var1rc / gmtRc
		var1all(imodel) = var1rc
		delete(var1rc)
	end if
	delete([/in, var1, time,ind1YYYY, var1YYYY, time1YYYY, gmt, gmtRc/])
end do ; imodel loop
modelInd = dim_pqsort(var1all, -1) 
delete(var1all)
if (alphaOrder)
	modelInd = ispan(0, dimsizes(modelList)-1, 1)
end if

;*************************************************
; Input data and plot
;*************************************************
do iseas = 4, 4
	if (iseas .eq. 0)
		mySeas = "DJF"
	end if
	if (iseas .eq. 1)
		mySeas = "MAM"
	end if
	if (iseas .eq. 2)
		mySeas = "JJA"
	end if
	if (iseas .eq. 3)
		mySeas = "SON"
	end if
	if (iseas .eq. 4)
		mySeas = "ANN"
	end if
	wks = gsn_open_wks("pdf", "Figures/IPO_EOF" + (neof+1) + "_BW_" + mySeas + "_" + yrFirst + "-" + yrLast + "_151027Dtb")
	gsn_define_colormap(wks, BlueDarkRed22b)
	plot = new(90, graphic)
	plot2 = new(90, graphic)

	;*************************************************
	; Obs
	;*************************************************
	print("HadISST")
	in = addfile("Output/201510_indices/tos_Obs_HadISST_" + mySeas + "_1891-2013_r180x90_IPO_TBV_151027b.nc", "r")
	neof = 0;in->nIpo2
	eof = in->ipoPatt2(neof,:,:)
	eof@long_name = ""
	eof@units = ""
	res@gsnLeftString = "HadISST, " + sprintf("%5.1f", eof@pcvar(neof)) + "%"
	plot(0) = gsn_csm_contour_map_ce(wks, eof, res)

   	rad = 4.*atan(1.)/180.   
  	clat = sqrt( cos(rad*eof&lat) )  
	obsWgt = eof*conform(eof, clat, 0)
	copy_VarMeta(eof, obsWgt)
	delete([/in, eof, rad/])
	
	in = addfile("Data/Obs/seasons/NSIDC_NOAA_SH_r180x90_" + mySeas + ".nc", "r")
	sic = in->sic_goddard_bt 
	yyyy1 = cd_calendar(sic&time, -1)/100
	indYYYY1 = ind(yyyy1.ge.1979 .and. yyyy1.le.2013)
	sic15 = dim_avg_n(sic(indYYYY1,:,:) , 0)
	copy_VarMeta(sic(0,:,:), sic15)
	sic15@long_name = ""
	sic15@units = ""
	plot2(0) = gsn_csm_contour(wks, sic15, res2)
	overlay (plot(0), plot2(0))
	delete([/in, sic, yyyy1, indYYYY1, sic15/])

	;*************************************************
	; Models
	;*************************************************
	eofMMM = new((/dimsizes(modelList), dimsizes(obsWgt&lat(:)), dimsizes(obsWgt&lon)/), float)
	pcvarMMM = new(dimsizes(modelList), float)
	sicMMM = new((/dimsizes(modelList), dimsizes(obsWgt&lat), dimsizes(obsWgt&lon)/), float)
	counter = 2
	do imodel = 0, dimsizes(modelList) - 1
		model = str_get_field(modelList(modelInd(imodel)), 1, delim)
		run = str_get_field(modelList(modelInd(imodel)), 2, delim)
		print(model + ", " + run)

		in = addfile("Output/201510_indices/tos_Omon_" + model + "_hist_rcp85_" + run + "_" + mySeas + "_1861-2100_r180x90_IPO_TBV_151027b.nc", "r")
		neof = 0
		eof1 = in->ipoPatt2(neof,:,:)
		eof1@long_name = ""
		eof1@units = ""
		eofWgt1 = eof1*conform(eof1, clat, 0) 
		copy_VarMeta(eof1, eofWgt1)
		pattCorr1 =  escorc(ndtooned(obsWgt({-40:60}, {100:290})), ndtooned(eofWgt1({-40:60}, {100:290}))) ; Pacific

		neof = 1
		eof2 = in->ipoPatt2(neof,:,:)
		eof2@long_name = ""
		eof2@units = ""
		eofWgt2 = eof2*conform(eof2, clat, 0) 
		copy_VarMeta(eof2, eofWgt2)
		pattCorr2 =  escorc(ndtooned(obsWgt({-40:60}, {100:290})), ndtooned(eofWgt2({-40:60}, {100:290}))) ; Pacific

		tpi = in->tpiFilt3
		ts1 = in->ipoTs2(0,:)
		ts2 = in->ipoTs2(1,:)
		indYYYY = ind(tpi&year.ge.1891 .and. tpi&year.le.2013)
		tsCorr1 = escorc(tpi(indYYYY), ts1(indYYYY))
		tsCorr2 = escorc(tpi(indYYYY), ts2(indYYYY))

		;if ( abs(pattCorr1) .gt. abs(pattCorr2) ) 
		;if ( abs(tsCorr1) .gt. abs(tsCorr2) ) 
			neof = 0
			eof = eof1
			pattCorr = pattCorr1
		;else
		;	neof = 1
		;	eof = eof2
		;	pattCorr = pattCorr2
		;end if
		delete([/tpi, ts1, ts2, indYYYY, tsCorr1, tsCorr2/])

		;if (pattCorr .lt. 0)
		;	eof = -1*eof
		;	pattCorr = -1*pattCorr
		;end if

		res@gsnLeftString = model + ", " + run + ", " + sprintf("%5.1f", eof@pcvar(neof)) + "%"
		res@gsnRightString = "r = " + sprintf("%5.2f", pattCorr)
		eofMMM(counter-2,:,:) = eof
		pcvarMMM(counter-2) = eof@pcvar(neof)
		plot(counter) = gsn_csm_contour_map_ce(wks, eof, res)
		delete([/in, eof1, eofWgt1, pattCorr1, eof2, eofWgt2, pattCorr2, eof, pattCorr/])

		fileStr  = "Data/CMIP5_OImon/sic/hist_rcp85/seasons/sic_OImon_" + model + "_hist_rcp85_" + run + "_" + mySeas + "_1861-2100_r180x90.nc"
		in = addfile(fileStr, "r")
	 	sic = in->sic
		yyyy1 = cd_calendar(sic&time, -1)/100
		indYYYY1 = ind(yyyy1.ge.yrFirst .and. yyyy1.le.yrLast)		 
		sic15 = dim_avg_n(sic(indYYYY1,:,:), 0)
		copy_VarMeta(sic(0,:,:), sic15)
		sic15@long_name = ""
		sic15@units = ""
		sicMMM(counter-2,:,:) = sic15
		plot2(counter) = gsn_csm_contour(wks, sic15, res2)
		overlay (plot(counter), plot2(counter))
		delete([/in, sic, yyyy1, indYYYY1, sic15/])

		counter = counter + 1
	end do ; imodel loop 	

	eof = dim_avg_n_Wrap(eofMMM, 0)
	sic15 = dim_avg_n_Wrap(sicMMM, 0)
	copy_VarMeta(obsWgt({:},:), eof)
	copy_VarMeta(obsWgt, sic15)
	eofWgt = eof*conform(eof, clat, 0) 
	pattCorr =  escorc(ndtooned(obsWgt), ndtooned(eofWgt))
	
	eof@long_name = ""
	eof@units = ""
	sic15@long_name = ""
	sic15@units = ""
	res@gsnLeftString = "Multimodel mean, " + sprintf("%5.1f", avg(pcvarMMM)) + "%"
	res@gsnRightString = "r = " + sprintf("%5.2f", pattCorr)
	plot(1) = gsn_csm_contour_map_ce(wks, eof, res)
	plot2(1) = gsn_csm_contour(wks, sic15, res2)
	overlay (plot(1), plot2(1))
	delete([/obsWgt, eofMMM, pcvarMMM, sicMMM, eof, sic15, eofWgt, pattCorr/])  

	;*************************************************
	; Panel plots
	;*************************************************
	panel_res 		   = True
	panel_res@gsnFrame         = False 
	panel_res@gsnMaximize	   = True              		
	panel_res@gsnPanelRowSpec  = True
	panel_res@gsnPanelCenter   = False				
	panel_res@gsnPanelYWhiteSpacePercent = 5
	panel_res@gsnPanelXWhiteSpacePercent = 2
	panel_res@txFontHeightF    = 0.01
	if (mySeas .eq. "ANN")
	  	mySeasNice = "Annual"		
	else
		mySeasNice = mySeas	
	end if
	panel_res@txString 	   = "Observed and CMIP5 IPO EOF" + (neof+1)
	panel_res@gsnPanelLabelBar = True
	panel_res@lbLabelFontHeightF= 0.006
	panel_res@lbLabelStride    = 1
	panel_res@lbBoxLineThicknessF= 0.7
	panel_res@lbBoxSeparatorLinesOn= False
	gsn_panel(wks, plot, (/9,9,9,9,9,9,9,9,9,9/), panel_res)
	frame(wks)  
	delete([/wks, plot, plot2/])	
end do ; iseas loop		
end
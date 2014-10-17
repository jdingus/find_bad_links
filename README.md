This script will take the export of an access table and search for hyperlinks anywhere within the table
If it finds a hyperlink it will try to get the size of the file tied to the hyperlink
If the size is 0 it will report it as a broken link
Report is output in results.csv which will look like the following:

															
	***** Summary for info.txt Table ***** 											
	99.3% Accuracy Rate												
	598 Links Good													
	4 Links Bad													
	*******************Bad Links Below***************** 									
	30062	3062-0148-OVA	3/24/2000 0:00	LOCATION INDEX - OPERATOR VISUAL AID	A	3062-0148-OVA#..\Data Files\Plant 3 Files\Visual Aids\Machines\3062-0148-OVA.xls#	
															
	30905	5905-0073-ODS	2/4/2013 0:00	IR Oven	A	5905-0073-ODS#..\Data Files\Plant 3 Files\ODS\Machines\5905-0073-ODS.xls#		
															
	30905	5905-0074-ODS	4/16/2013 0:00	PAX Pivot Bushing	B	5905-0074-ODS#P:\ShopFloor\Data Files\Plant 3 Files\ODS\Machines\5905-0074-ODS.xls#	
															
	30905	5905-0075-ODS	4/16/2013 0:00	Rubber Rebound Roller	B	5905-0075-ODS#P:\ShopFloor\Data Files\Plant 3 Files\ODS\Machines\5905-0075-ODS.xls#	
															
															


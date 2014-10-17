This script will take the export of an access table and search for hyperlinks anywhere within the table
If it finds a hyperlink it will try to get the size of the file tied to the hyperlink
If the size is 0 it will report it as a broken link
Report is output in results.csv which will look like the following:

															
	***** Summary for info.txt Table ***** 											
	99.3% Accuracy Rate												
	598 Links Good													
	4 Links Bad													
	*******************Bad Links Below***************** 	
bad links listed here......

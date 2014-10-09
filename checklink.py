import os
import re

def scanforlinks(table_filename,rootdir):
    """ Pass in filename.txt and will parse out hyperlink #..\Data Files\Plant 1 Files\ODS\226-in.xls#
                                            or            #..\Data%20Files\Plant%201%20Files\ODS\10580.xls#
        If length of file is = 0 , ie. bad link it will return a list of bad ODS links
    """
    tot_good=0
    tot_bad=0
    tot_not_link = 0
    not_link = 0
    bad_links=[]

    with open(table_filename) as f:
        for line in f:
            hyper_link = parselink(line)
            # print hyper_link
            # try:
            if hyper_link[0]=='P':   # Absolute Path
                good,bad,filename = checkbadlink(hyper_link)

            elif hyper_link[0]=='N':   # NO link present
                good,bad,filename = checkbadlink(hyper_link)
                not_link = bad
                bad = 0

            else:
                rel_link = parselink(line) # Relative Path
                rel_link = os.path.normpath(rel_link)
                abs_link = rootdir+rel_link
                good,bad,filename = checkbadlink(abs_link)

            if bad==1:
                # bad_links.append('~~CHECKME~~ '+ table_filename + ' ~~ ' + line)
                bad_links.append(line)

            tot_good += good
            tot_bad +=  bad
            tot_not_link += not_link
            # except:
            #     bad_links.append('~~NO LINK~~ '+ table_filename + ' ~~ ' + line)
    # print tot_good,tot_bad
    return tot_good,tot_bad,tot_not_link,bad_links


def parselink(string):
    """ Pass in a string and parse out the hyperlink """
    #Convert %20 to spaces
    import urllib2
    string = urllib2.unquote(string)
    string = "r'{}'".format(string) # Convert string to raw text
    # list = string.split('#')
    # print list
    # raise SystemExit
    hyperlink_exp = r"(#)(P:.*)(#)|(#[.]{2})(.*)(#)"
    re_hyper = re.search(hyperlink_exp,string)
    if not re_hyper:
        re_hyper = 'NO Hyperlink Present'
        return  re_hyper
    if re_hyper.group(2):
        return re_hyper.group(2)
    if re_hyper.group(5):
        return re_hyper.group(5)

def commonize_filepath(string):
    import urllib2
    string = urllib2.unquote(string)
    print string
    # raw_str = "r" + "'" + string + "'"
    # # print 'temp str',temp_str
    # # raw_str = temp_str[1:-1]
    # print 'raw string',raw_str
    string.replace('\\', '\\\\')
    # string.replace('%20','')    
    print string
# def parselink(string):
#     """ Pass in a string and parse out the hyperlink """
    
#     import urllib2
#     import re
#     string = urllib2.unquote(string)

#     start_marker = end_marker = '#'

#     # string = 'Export Bay","Export-in",8/5/2004 0:00:00,"Export Bay Index","D","EXPORT-in#..\Data Files\Plant 1 Files\ODS\EXPORT-in.xls#'
#     # print 'string we are parsing:',string
#     # print 'start marker : ',start_marker
#     try:  
#         start = string.index(start_marker) + len(start_marker)
#         end = string.index(end_marker, start + 1)
#         n = string[start:end]
#     except ValueError:
#         n = 'NO Hyperlink Present'
#         return n
#     #Now remove .. before the \
#     # n= n[2:]
#     # print n
#     return n

def checkbadlink(filename):
    import os.path

    size = 0.0
    good = 0
    bad = 0

    good_file = os.path.isfile(filename)
    print 'good file',good_file

    print filename
    try:

        size = os.path.getsize(filename)
        # print filename + " Found It!"
        good=1
        return good,bad,filename

    except:
        bad=1
        return good,bad,filename


def print_header(accuracy,table_filename,good,bad,bad_links):

    try:
        accuracy =  good*1.0/(good+bad)*100
    except  ZeroDivisionError:
        print ''
        print 'ERROR???, EXITING, 0 Good and 0 Bad found???'
        print ''
        
    header1 = ""
    header2 = " ***** Summary for " + table_filename +" Table ***** "
    header3 = ("%.1f" % accuracy) + "% Accuracy Rate"
    header4 = str(good) + ' Links Good'
    header5 = str(bad) + ' Links Bad'
    header6 = " *******************Bad Links Below***************** "
    table_summary = [header1] + [header2] + [header3] + [header4] + [header5] + [header6] + bad_links
    return table_summary

def main():
    # s = "10304","68975540","see ODS Index 371-in#..\Data Files\Plant 1 Files\ODS\371-IN.XLS#","SU-371-in#..\Data Files\Plant 1 Files\Set-Up Instructions\Non-CNC Machines\SU-371in.xls#"
    # # s = '''"10575","10642",7/29/2013 0:00:00,"Shock Fram Hanger","A","10642#P:\ShopFloor\Data Files\Plant 1 Files\ODS\10642.xls#"'''
    # # # s = 'P:\ShopFloor\Data Files\Plant 1 Files\ODS\10642.xls'
    # s = "r'{}'".format(s)
    # print s
    # raise SystemExit
    # # s='''"10030","10564",6/28/2012 0:00:00,"Workhorse Shackle Assembly","B","10564#P:\ShopFloor\Data Files\Plant 1 Files\ODS\10564.xls#"'''
    # # s = '''30620","JSA 620",7/12/2011 0:00:00,"JOB SAFETY ANALYSIS",,"JSA 620#P:\Safety\Safety Programs\JSA\WC 620 7-12-11.doc#'''
    # f = parselink(s)
    # print f 
    # print checkbadlink(f)
    # raise SystemExit
    # s = """10030","10564",6/28/2012 0:00:00,"Workhorse Shackle Assembly","B","10564#P:\ShopFloor\Data Files\Plant 1 Files\ODS\10564.xls#"""
    # print parselink(s)
    # s = """10575","10645",8/19/2013 0:00:00,"R 1000 Hub Plate","A","10645#..\Data%20Files\Plant%201%20Files\ODS\10645.xls#"""
    # print parselink(s)
    # raise SystemExit
    # if results.txt present delete it !
    try:
        os.remove('results.txt')
    except OSError:
        pass
    # commonize_filepath('\Data%20Files\Plant%201%20Files\ODS\10640.xls')
    # commonize_filepath('/Data%20Files/Plant%201%20Files/ODS/10591.xls')
    # raise SystemExit
    rootdir = os.path.normpath("P:/ShopFloor/")
    list_tables=['ODS info.txt','index.txt','PART TABLE.txt','setup.txt']
    table_summary = []
    goodcount=0.0
    badcount=0.0
    notlinkcount=0.0
    
    for table_filename in list_tables:
        good,bad,not_link,bad_links = scanforlinks(table_filename,rootdir)


            # raise SystemExit
        accuracy = 0    
        table_summary = print_header(accuracy,table_filename,good,bad,bad_links)

        with open('results.txt', 'a') as thefile:
            for item in table_summary:
                thefile.write("%s\n" % item)
            thefile.write(2500*'@')
        goodcount+=good
        badcount+=bad
        notlinkcount+=not_link


    print 'goodcount',goodcount
    print 'badcount',badcount
    print 'No Link on Line',not_link
    # accuracy =  goodcount*1.0/(goodcount+badcount)*100
    # print accuracy

if __name__ == "__main__":   
    main()
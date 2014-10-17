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

            elif hyper_link[0:3]=='/..':
                hyper_link = hyper_link[3:]
                rel_link = hyper_link
                # rel_link = os.path.normpath(rel_link)
                rootdir = 'P:' #os.path.normpath("P:/")
                abs_link = rootdir+rel_link
                # print '***',abs_link
                good,bad,filename = checkbadlink(abs_link)                
                
            elif hyper_link[0]=='/':
                rel_link = hyper_link
                # rel_link = os.path.normpath(rel_link)
                rootdir = 'P:/ShopFloor/'
                abs_link = rootdir+rel_link
                # print '******',abs_link
                good,bad,filename = checkbadlink(abs_link)
            else:
                good=0
                bad=1
            
            if bad==1:
                bad_links.append(line)

            tot_good += good
            tot_bad +=  bad
            tot_not_link += not_link
    return tot_good,tot_bad,tot_not_link,bad_links


def parselink(string):
    """ Pass in a string and parse out the hyperlink """
    #Convert %20 to spaces
    import urllib2
    string = urllib2.unquote(string)
    string = "r'{}'".format(string) # Convert string to raw text
    string=string.replace('\\','/')

    hyperlink_exp = r"(#)(P:.*)(#)|(#)([.]{2})(.*)(#)"
    re_hyper = re.search(hyperlink_exp,string)
    if not re_hyper:
        re_hyper = 'NO Hyperlink Present'
        return  re_hyper
    # print re_hyper.groups()
    if re_hyper.group(2):
        return re_hyper.group(2)
    if re_hyper.group(5):
        return re_hyper.group(6)

def commonize_filepath(string):
    import urllib2
    string = urllib2.unquote(string)
    string.replace('\\', '\\\\')


def checkbadlink(filename):
    import os.path

    size = 0.0
    good = 0
    bad = 0
    good_file = os.path.isfile(filename)
    try:
        size = os.path.getsize(filename)
        # print size
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
    try:
        os.remove('results.csv')
    except OSError:
        pass
    rootdir = os.path.normpath("P:/ShopFloor/")
    list_tables=['ODS info.txt']
    table_summary = []
    goodcount=0.0
    badcount=0.0
    notlinkcount=0.0
    
    for table_filename in list_tables:
        good,bad,not_link,bad_links = scanforlinks(table_filename,rootdir)
        accuracy = 0    
        table_summary = print_header(accuracy,table_filename,good,bad,bad_links)

        with open('results.csv', 'a') as thefile:
            for item in table_summary:
                thefile.write("%s\n," % item)
        goodcount+=good
        badcount+=bad
        notlinkcount+=not_link

    print 'goodcount',goodcount
    print 'badcount',badcount
    print 'No Link on Line',not_link

if __name__ == "__main__":   
    main()
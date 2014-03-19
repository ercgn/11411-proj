# testing the qa algorthm 

from util.q_parser import QParser;
import sys;

# key_tokens = qx_parse.parse_question("What things did Aaron break today?")
# print key_token

def testQx():
    args = sys.argv[1:];
    argc = len(args);
    if argc < 1:
        print "ERROR: input\n";
        exit();
    else:
        inputFile = args[0];
        inFH = open(inputFile);
        for line in inFH:
            questParse = QParser(line.strip());
            key_tokens = questParse.find_keywords();
            print "LINE::",line,key_tokens,"\n";
        inFH.close();
    return;
       

if __name__ == "__main__":
    testQx();

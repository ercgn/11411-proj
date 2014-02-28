# testing the qa algorthm 

import qx_parse
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
            key_tokens = qx_parse.parse_question(line);
            print key_tokens;
        inFH.close();
    return;
       

def testComb():
    a = "For the love of Christ controls us, because we have concluded this: that one has died for all, therefore all have died; and he died for all, that those who live might no longer live for themselves but for him who for their sakes was raised."
    a = a.strip().split();
    b = [a[0]] + a[3:5] + a[8:10] + a[15:19];
    listX = qx_parse.combWords(b,a);
    print b;
    print listX;
    return;

if __name__ == "__main__":
    testQx();
#    testComb();

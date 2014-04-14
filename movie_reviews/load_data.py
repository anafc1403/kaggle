def load_base_training():
    file = open('data/train.tsv')

    # One dict for phrase length (in words)
    train_dicts = []
    for _ in range(53):  # Longest phrase contains 53 words
        train_dicts.append({})

    # Ignore heading
    file.next()

    #print file.next().strip().split('\t')
    for l in file:
        phraseid, sentenceid, phrase, sentiment = l.strip().split('\t')
        phrase = phrase.lower()
        words = phrase.split(' ')
        train_dicts[len(words)][phrase] = sentiment

    return train_dicts


def load_base_test():
    testfile = open('data/test.tsv')

    test_lines = []

    # Ignore Heading
    testfile.next()
    i=0;

    for l in testfile:
        #phraseid, sentenceid, phrase = l.strip().split('\t')
        #test_lines.append((phraseid, phrase.lower()))
        phraseid = l.strip().split('\t')
        phrase=""
        if(len(phraseid)>2):
            phrase=phraseid[2].lower()
        test_lines.append((phraseid[0], phrase))


    return test_lines



def lookup_dict(train_dicts, phrase):
    num_words = len(phrase.split(' '))

    if num_words > 52:
        return None

    #print "Looking for phrase: " + phrase + " -- Returning: " + str(train_dicts[num_words].get(phrase))
    return train_dicts[num_words].get(phrase)


def write_submission(array):
    filename = 'data/submission.csv'
    print "Writing output to filename: " + filename

    outputfile = open(filename, 'w')
    outputfile.write("PhraseId,Sentiment\n")

    for el in array:
        outputfile.write(str(el[0]) + "," + str(el[1]) + "\n")

    outputfile.close()


def calculate_most_frequent(train_dicts):
    most_frequent = []

    for i in range(len(train_dicts)):
        distrib_sentiments = [0]*6

        for item in train_dicts[i]:
            distrib_sentiments[int(train_dicts[i][item])] += 1
            distrib_sentiments[5] += 1
        print "Looking at phrase size: " + str(i) + ", total phrases: " + str(distrib_sentiments[5]) + " -->" + \
              str([round(float(x)/max(distrib_sentiments[5],1), 2) for x in distrib_sentiments[0:5]])
        most_frequent.append(max( (v, i) for i, v in enumerate(distrib_sentiments[0:5]) )[1])

    most_frequent = most_frequent + [2,]*100  # Autocomplete with 2s
    return most_frequent


def calculate_most_frequent2(lista):
    most_frequent = []

    distrib_sentiments = [0]*5

    for item in lista:
        distrib_sentiments[item] += 1

    most_freq=0;
    freq=0
    for i in range(0,4):
        if distrib_sentiments[i] >freq:
            freq=distrib_sentiments[i]
            most_freq=i



    return most_freq


#----------------
# read the dictionary
# split each line in different string
#  str1 \t str2\n
#create an element of the dictionary with the str1 as key=world and
# the str2 as value
def parse_dict():
    dict={}

    filename = 'data/AFINN-111.txt'
    fp= open(filename)
    for i in fp.readlines():
        temp=i.split("\t");
        temp2=temp[1].split("\n")
        dict[str(temp[0]).lower()] = temp2[0]

    fp.close()
    return dict



def create_corpus(train_dicts,media,moda,mediana):
    dictFreq={}
    dict={}
    print "Create corpus"
    for i in range(len(train_dicts)):

        for item in train_dicts[i]:
            SentimentOld=int(train_dicts[i][item])

           #palabras de longuitud 0 van directamente al corpus
            worlds=item.split(' ')
            for j in worlds:
                if not dictFreq.has_key(str(j).lower()):
                     dictFreq[str(j).lower()]=[]
                dictFreq[str(j).lower()].append(SentimentOld)




    for i in dictFreq:
        print i+" "+str(dictFreq[i])
        value=0.0;
        for j in dictFreq[i]:
            value+=j
        print value, len(dictFreq[i])
        if media==True:
            #dict[i]=int(round(float(value/len(dictFreq[i]))))
            dict[i]=calculate_most_frequent2(dictFreq[i])
        print dict[i]
    return dict


def get_sentimental_value(test_dicts,dict,media,moda,mediana):

    print "Get sentimental value"
    test_prediction = []

    for item in test_dicts:
            #print item
            value=[]
            missing=True

            worlds=item[1].split(' ')
            phraseid=item[0]
            for j in worlds:
                if dict.has_key(str(j).lower()):
                    value.append(int(dict[str(j).lower()]))
                    missing=False
            if media:
                #val=int(round((sum(value)+0.0)/len(worlds)))
                val=calculate_most_frequent2(value)
            if missing: #no existe poner el valor mas freq
                val=2
            print str(item[1]),value,str(val)
            test_prediction.append((phraseid, str(val)))
    return test_prediction






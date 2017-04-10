import nltk, csv

#Of the extracted phrases, get only the important part i.e. for phrases like imm_2_num, imm_2_den, get only the last part (num and den). Get NN and JJ,NN.


clustered_input = csv.reader(open('../Results/AttributeCluster_20_itr1000.csv','rb'))


def common_words(set1,set2):
    no_words = 0
    for word1 in set1:
        for word2 in set2:
            if word1 == word2: no_words += 1
    return no_words

clusters = set()
phrases = {}
for row in clustered_input:
    phrases[row[0]] = row[1]
    clusters.add(row[1])

#print phrases
ID_phrases = {}
id_new = 0
for ID in clusters:
    phrase_imp_words = {}
    phrase = [key for key, val in phrases.items() if val == ID]
    print phrase
    print '\n'
    for p in phrases:
        list_word = []
        tokenized = p.split('_')
        pos_phrase = nltk.pos_tag(tokenized)
        print pos_phrase
        for word in pos_phrase:
            #print word[1]
            if word[1] == 'JJ' or word[1] == 'NN':
                w = word[0]    
                list_word.append(w)
        phrase_imp_words[p] = list_word
    #print phrase_imp_words
    #print '\n'        

            
#print ID_phrases

# This function receives a list that contains all the results and exports the results as Srt
def exportAsSrt(ocrResults):
    output = ""
    k = 1
    for i in range(0, len(ocrResults)):
        if(ocrResults[i].string == ""):
            continue
        output = output + str(k) + "\n"
        output = output + ocrResults[i].time + "\n"
        output = output + ocrResults[i].string + "\n"
        output += "\n"
        k += 1
		
    fh = open('subtitle.srt', 'w', encoding='utf-8')
    fh.write(output)
    fh.close()

# This function receives a list that contains all the results and exports the results as string
def exportAsString(ocrResults):
    output = ""
    for i in range(0, len(ocrResults)):
        if(ocrResults[i].string == ""):
            continue
        output = output + ocrResults[i].string + "\n"

    fh = open('subtitle.txt', 'w', encoding='utf-8')
    fh.write(output)
    fh.close()

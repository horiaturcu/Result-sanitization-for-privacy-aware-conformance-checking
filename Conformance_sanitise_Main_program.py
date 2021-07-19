



#The following code requires pm4py this can be done by running the console and writing "pip install pm4py" it also uses the Mini-conda python.
class k_anon :
    import os
    from pm4py.objects.log.importer.xes import importer as xes_importer
    from pm4py.algo.discovery.inductive import algorithm as inductive_miner
    from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
    from pm4py.algo.conformance.alignments.petri_net.variants.state_equation_a_star import PARAM_MODEL_COST_FUNCTION
    from pm4py.objects.conversion.log import converter as log_converter
    from difflib import SequenceMatcher

    print('i am starting the import')
    # The "D:\UniMannheim\Bachelor\Event logs\A.xes" in the next line can be changed in order to show the path to the xes or csv file you want the inductive miner to run on
    log = xes_importer.apply(os.path.join("tests", "input_data", r"D:\UniMannheim\Bachelor\Event logs\A.xes"))
    print('i finished the import')
    net, initial_marking, final_marking = inductive_miner.apply(log,variant = inductive_miner.Variants.IMf,parameters={inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD : 0.3})
    print('i am aligning now')
    aligned_traces = alignments.apply_log(log, net, initial_marking, final_marking)

    def list_in(a, b):
        return any(map(lambda x: b[x:x + len(a)] == a, range(len(b) - len(a) + 1)))


    #The following for statement can be commented out in order to keep the (>>,None) alignments in the log
    for x in range(len(aligned_traces)) :
        for y in reversed(range(len(aligned_traces[x]['alignment']))) :
            if aligned_traces[x]['alignment'][y][0] == '>>' and aligned_traces[x]['alignment'][y][1] == None :
                aligned_traces[x]['alignment'].remove(aligned_traces[x]['alignment'][y])


   


    for x in range(len(aligned_traces)) :
        aligned_traces[x]['occurences'] = 1
        aligned_traces[x]['confirmed'] = -1

    aligned_list = list()
    for x in range(len(aligned_traces)) :
        aligned_list.append(aligned_traces[x])
    

    lcs_list = list()
    lcs_dict = {}
    counter = 0


    for x in range(len(aligned_traces)):
        spot = x+1
        seen = 0
        # flag = 0
        string1 = str(aligned_list[x]['alignment'])
         
        for y in range(spot,len(aligned_traces)) :
            flag = 0
            already_here = x
            string2 = str(aligned_list[y]['alignment'])
            match = SequenceMatcher(None, string1,string2).find_longest_match(0,len(string1),0,len(string2))
            size = len(string1[match.a: match.a +match.size])
            mod_string = string1[match.a: match.a +match.size]
            #This if statement can also be increased or decreased depending on how long/short you want your sub-sequences, default 40 in order to display a minimum of 3 tuples.
            if len(mod_string) < 40 :
                continue
            

            while mod_string[-1] != ')' :
                l = len(mod_string)
                mod_string = mod_string[:l-1]
            while mod_string[0] != '(' :
                mod_string = mod_string[1:]
            if '>>' not in mod_string :
                continue
            print(mod_string)
            sequence = eval('[' + mod_string +']')
            if counter == 0 :
                lcs_dict = {'alignment' : sequence, 'occurence' : 1, 'confirmed' : -1}
                lcs_list.append(lcs_dict)
                counter +=1
            else :
                for z in range(len(lcs_list)) :
                    if list_in(sequence , lcs_list[z]['alignment']) :
                        if lcs_list[z]['confirmed'] != x :
                            lcs_list[z]['occurence'] +=1
                            flag = 1
                            lcs_list[z]['confirmed'] = x
                            break
                if flag == 0 :
                    lcs_dict = {'alignment' : sequence , 'occurence' : 1, 'confirmed' : -1}
                    lcs_list.append(lcs_dict)
    
                
    # the if statement can be increased or decreased, default 5 in order to achieve higher or lower k-anonimity
    k_list = list()
    for x in lcs_list :
        if x['occurence'] >= 5 :
            k_list.append(x)

    import pandas as pd
    from pm4py.objects.conversion.log import converter as log_converter
    dataframe = log_converter.apply(k_list, variant=log_converter.Variants.TO_DATA_FRAME)
    # The "D:\UniMannheim\Bachelor\Event logs\results-expAtest.csv" can be chenged in order to export the final log to another location Note that this exports a csv file always
    dataframe.to_csv(r"D:\UniMannheim\Bachelor\Event logs\results-expCtest.csv")

    #The following for statement exists to show all the skips present in the end-event log, it prints them to the console, this for statement can be commented out if they do not present an interest
    cald = list()
    for x in range(len(k_list)) :
        for y in range(len(k_list[x]['alignment'])) :
            if k_list[x]['alignment'][y][0] == '>>' or k_list[x]['alignment'][y][1] == '>>' :
                if k_list[x]['alignment'][y][1] != None :
                    cald.append(k_list[x]['alignment'][y])
    print(cald)


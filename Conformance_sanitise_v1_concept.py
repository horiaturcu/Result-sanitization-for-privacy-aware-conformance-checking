

from pm4py.objects.log.importer.xes.importer import Variants


class a :
    import os
    from pm4py.objects.log.importer.xes import importer as xes_importer
    from pm4py.algo.discovery.inductive import algorithm as inductive_miner
    from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
    from pm4py.algo.conformance.alignments.petri_net.algorithm import Parameters
    from pm4py.algo.conformance.alignments.petri_net.variants.state_equation_a_star import PARAM_MODEL_COST_FUNCTION


    # def getTuples (list1 : list) :
    #     return_list = list()
    #     for x in list1 :
    #         return_list.append((x[0],x[1]))
    #     return return_list

    # def getTuple (list2 : list)

    print('i am starting the import')
    log = xes_importer.apply(os.path.join("tests", "input_data", r"D:\UniMannheim\Bachelor\Event logs\B.xes"))
    print('i finished the import')
    net, initial_marking, final_marking = inductive_miner.apply(log,variant = inductive_miner.Variants.IMf, parameters={inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD : 0.3})
    
    print('i am aligning now')
    aligned_traces = alignments.apply_log(log, net, initial_marking, final_marking)

    

    for x in range(len(aligned_traces)) :
        for y in reversed(range(len(aligned_traces[x]['alignment']))) :
            if aligned_traces[x]['alignment'][y][0] == '>>' and aligned_traces[x]['alignment'][y][1] == None :
                aligned_traces[x]['alignment'].remove(aligned_traces[x]['alignment'][y])




    for x in range(len(aligned_traces)) :
        aligned_traces[x]['occurances'] = 1
    new_list = list()
    new_list.append(aligned_traces[0])
  

    print('i ma doing a for now')
    for i in range(len(aligned_traces))[1:] :
        cost = aligned_traces[i]['cost']
        visited_states = aligned_traces[i]['visited_states']
        fitness = aligned_traces[i]['fitness']
        queued_states = aligned_traces[i]['queued_states']
        traversed_arcs = aligned_traces[i]['traversed_arcs']
        lp_solved = aligned_traces[i]['lp_solved']
        min = 99999
        spot = 0
        for j in range(len(new_list)) :
            cost2 = new_list[j]['cost']
            visited_states2 = new_list[j]['visited_states']
            fitness2 = new_list[j]['fitness']
            queued_states2 = new_list[j]['queued_states']
            traversed_arcs2 = new_list[j]['traversed_arcs']
            lp_solved2 = new_list[j]['lp_solved']
            sum = abs(cost - cost2) + abs(visited_states - visited_states2) + abs(queued_states - queued_states2) + abs(traversed_arcs - traversed_arcs2) + abs(lp_solved - lp_solved2) + abs(fitness -fitness2)
            if sum < min :
                min = sum
                spot = j
        if min >= 0 and min< 5 :
            new_list[spot]['occurances']+=1
        else :
            new_list.append(aligned_traces[i])
    
    k_list = list()
    for x in new_list :
        if x['occurances'] >= 5 :
            k_list.append(x)

    cald = list()
    for x in range(len(k_list)) :
        for y in range(len(k_list[x]['alignment'])) :
            if k_list[x]['alignment'][y][0] == '>>' or k_list[x]['alignment'][y][1] == '>>' :
                if k_list[x]['alignment'][y][1] != None :
                    cald.append(k_list[x]['alignment'][y])
    print(cald)

    import pandas as pd
    from pm4py.objects.conversion.log import converter as log_converter
    dataframe = log_converter.apply(k_list, variant=log_converter.Variants.TO_DATA_FRAME)
    dataframe.to_csv(r"D:\UniMannheim\Bachelor\Event logs\Bexportedaligned.csv")



    



  



    # for i  in range( len(aligned_traces)) :
    #     for j,k in range(len(aligned_traces[i]['alignment'])) :
    #         if aligned_traces[i]['alignment'][j] == aligned_traces[i+1]['alignment'][j] :
    #             print(aligned_traces[i]['alignment'][j])


    #variants_count = case_statistics.get_variant_statistics(log)
    #variants_count = sorted(variants_count, key=lambda x: x['count'], reverse=True)

    # skipped_list = list()
    # max = 0
    # for a in range(len(aligned_traces)) :
#     alignment_list = aligned_traces[a]['alignment']
#     for b in alignment_list :
#         if b[0] == '>>' or b[1] == '>>':
#                 skipped_list.append(aligned_traces[a])
            
                        
      
        
            # else :
            #     for n in skipped_list :
                   
            #         res = len(set(n['alignment']) & set(alignment_list[a])) / float(len(set(n['alignment']) | set(aligned_traces[a]['alignment']))) *100
            #         if res > max :
            #             max = res
            #     if max > 70 :
            #         skipped_list.append(n['alignment'])
            #     else :
            #         skipped_list.append(alignment_list[a])

            
   


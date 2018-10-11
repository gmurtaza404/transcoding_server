"""
    import choose_id.py to use the algorithm
    choose_id() function takes, a list of item, where each item should have a "memory_footprint" and a "value" attribute. 
    It can have additional attributes, and the resulting list will retain those values. and the second parameter is the maxweight.
    Maximum memory the webpage is allowed to consume.
    Make sure, that memory footprints and maxweight have same unit.
"""
import functools32

def choose_ids_knapsack(items, maxweight):
    result = [] # knapsack
    
    @functools32.lru_cache(maxsize=None)
    def bestvalue(i, j):
        if i == 0: return 0
        value= items[i - 1]["value"]
        weight= items[i - 1]["memory_footprint"]
        
        if weight > j:
            return bestvalue(i - 1, j)
        else:
            return max(bestvalue(i - 1, j),
                       bestvalue(i - 1, j - weight) + value)

    
    j = maxweight
    result = []
    
    for i in xrange(len(items), 0, -1):
        if bestvalue(i, j) != bestvalue(i - 1, j):
            result.append(items[i - 1])
            j -= items[i - 1]["memory_footprint"]
    result.reverse()
    
    return bestvalue(len(items), maxweight), result

def choose_id_greedily(items, maxweight):
    sorted_items = sorted(items, key=lambda k: k['memory_footprint'])
    index = 0
    selected_items = []
    while index <  len(sorted_items):
        if (maxweight - float(sorted_items[index]["memory_footprint"]) ) >= 0:
            selected_items.append(sorted_items[index])
            maxweight = maxweight - float(sorted_items[index]["memory_footprint"])
            index += 1
        else:
            break
    return (len(selected_items),selected_items)



#driver function
# def main():
#     knapsack_list = [{"id":1,"memory_footprint":12,"value":2},{"id":2,"memory_footprint":21,"value":3},{"id":3,"memory_footprint":11,"value":1}]
#     memory_capacity = 40
    
#     print choose_ids_knapsack(knapsack_list, memory_capacity)    

#main()
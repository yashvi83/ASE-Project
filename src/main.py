from tabulate import tabulate
import config 
from tests import *
from DATA import DATA
from LIB import LIB
import OPTIMIZATION
import DISCRETIZATION as discretization
import sys
lib = LIB()
sys.stdin.reconfigure(encoding='utf-8') 
sys.stdout.reconfigure(encoding='utf-8')


# def get_stats(data_array):
#     results = {}
#     for item in data_array:
#         statistics = lib.stats(item)
#         for k, v in statistics.items():
#             results[k] = results.get(k, 0) + v
#     for k, v in results.items():
#         results[k] /= 20

#     return results

def get_stats(data_array):
    n_items = len(data_array)
    statistics = [lib.stats(item) for item in data_array]
    results = {k: sum(stat[k] for stat in statistics) for k in statistics[0]}
    results = {k: v/20 for k, v in results.items()}

    return results

def main(options,help):    
        
        results = {"all": [], "sway": [], "sway2":[],"sway3":[],"xpln": [],"xpln2":[],"xpln3":[],"top": []}
    
        comparisons_table = [
            [["all", "all"], None],
            [["all", "sway"], None],
            [["all", "sway2"], None],
            [["all", "sway3"], None],
            [["sway", "sway2"], None],
            [["sway", "sway3"], None],
            [["sway2", "sway3"], None],
            [["sway", "xpln"], None],
            [["sway2", "xpln2"], None],
            [["sway3", "xpln3"], None],
            [["sway", "top"], None]
        ]
        count = 0
        data = None

        while count < 20:
            data = DATA(config.the['file'])
            rule = None
            while(rule==None):
                best,rest,evals = OPTIMIZATION.sway(data)
                rule, _ = discretization.xpln(data, best, rest)
                
                best2,rest2 = OPTIMIZATION.sway_with_kmeans(data)
                rule2,_ = discretization.xpln(data,best2,rest2)

                best3,rest3 = OPTIMIZATION.sway_with_agglo(data)
                rule3,_ = discretization.xpln(data,best3,rest3)
                
            data1 = DATA(data, discretization.selects(rule, data.rows))
            data2 = DATA(data,discretization.selects(rule2,data.rows))
            data3 = DATA(data,discretization.selects(rule3,data.rows))

            results['all'].append(data)
            results['sway'].append(best)
            results['xpln'].append(data1)
            results['sway2'].append(best2)
            results['xpln2'].append(data2)
            results['sway3'].append(best3)
            results['xpln3'].append(data3)
            top, _ = lib.betters(data, len(best.rows))
            top = DATA(data, top)
            results['top'].append(top)

            for i in range(len(comparisons_table)):
                    
                    [base, new], result = comparisons_table[i]
                   
                    if result is None:
                        comparisons_table[i][1] = ["=" for _ in range(len(data.cols.y))]
                        
                    for k in range(len(data.cols.y)):
                        
                        if comparisons_table[i][1][k] == "=":
                            
                            base_y, new_y = results[base][count].cols.y[k].col, results[new][count].cols.y[k].col
                            equals = lib.bootstrap(lib.has(base_y), lib.has(new_y)) and lib.cliffsDelta(lib.has(base_y), lib.has(new_y))

                            if not equals:
                                if i == 0:
                                    
                                    print("all to all {} {} {}".format(i, k, "false"))
                                    print(f"all to all failed for {results[base][count].cols.y[k].col.txt}")

                                comparisons_table[i][1][k] = "≠"
            count += 1
        
        
        headers = [y.col.txt for y in data.cols.y]
        table = []

        for key, value in results.items():
            stats = get_stats(value)
            stats_list = [key] + [stats[header] for header in headers]
            table.append(stats_list)
        
        print(tabulate(table, headers=headers, numalign="right"))
        print()

        table = []

        for [base, new], result in comparisons_table:
            table.append([f"{base} to {new}"] + result)

        print(tabulate(table, headers=headers, numalign="right"))

# eg("the","show settings", the_test)
# eg("num","demo of NUM",num_test)
# eg("sym","demo SYMS", sym_test)
# eg("some","demo of reservoir sampling", some_test)
# #eg("check_csv","reading csv files", csv_test)
# eg("data","showing data sets", data_test)
# eg("clone","replicate structure of a DATA", clone_test)
# eg("cliffs","stats tests", cliffs_test)
# eg("dist","check distance", dist_test)
# eg("half","divide data in half", half_test)
# eg("tree","make and show tree of clusters", tree_test)
# eg("Sway","optimizing", sway_test)
# eg("bins","find deltas between best and rest", bins_test)
#eg("xpln","explore explanation sets", xpln_test)
#main(config.the, config.help,egs)
main(config.the, config.help)

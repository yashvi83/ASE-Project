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
# def main(options, help, funs, saved = {}, fails = 0):
#     for k, v in lib.cli(lib.settings(help)).items():
#         options[k] = v
#         saved[k] = v
#     if options["help"]:
#         print(help)
#     else:
#         for what in funs:
#             if options["go"] == "all" or what == options["go"]:
#                 for k,v in saved.items():
#                     options[k] = v
#                 if funs[what]() == False:
#                     fails = fails + 1
#                     print("❌ fail:", what)
#                 else:
#                     print("✅ pass:", what)
#     exit(fails)


def get_stats(data_array):
    # gets the average stats, given the data array objects
    res = {}

    # accumulate the stats
    for item in data_array:
        #print("type of item",item)
        stats = lib.stats(item)

        # update the stats
        for k, v in stats.items():
            res[k] = res.get(k, 0) + v

    # right now, the stats are summed. change it to average
    for k, v in res.items():
        res[k] /= 20

    return res

def main(options,help):    
        
        results = {"all": [], "sway": [], "xpln": [], "top": []}
        n_evals = {"all": 0, "sway": 0, "xpln": 0, "top": 0}

        comparisons = [
            [["all", "all"], None],
            [["all", "sway"], None],
            [["sway", "xpln"], None],
            [["sway", "top"], None]
        ]
        count = 0
        data = None

        while count < 2:
            data = DATA(config.the['file'])
            rule = None
            while(rule==None):
                best,rest,evals = OPTIMIZATION.sway(data)
                
                rule, _ = discretization.xpln(data, best, rest)
                
            #if rule != -1:
            data1 = DATA(data, discretization.selects(rule, data.rows))
            
            results['all'].append(data)
            results['sway'].append(best)
            results['xpln'].append(data1)
            top, _ = lib.betters(data, len(best.rows))
            top = DATA(data, top)
            results['top'].append(top)

            n_evals["all"] += 0
            n_evals["sway"] += evals
            n_evals["xpln"] += evals
            n_evals["top"] += len(data.rows)
        
            for i in range(len(comparisons)):
                    
                    [base, diff], result = comparisons[i]
                   
                    if result is None:
                        comparisons[i][1] = ["=" for _ in range(len(data.cols.y))]
                        
                    for k in range(len(data.cols.y)):
                        # if not already marked as false
                        
                        if comparisons[i][1][k] == "=":
                            # check if it is false
                            base_y, diff_y = results[base][count].cols.y[k].col, results[diff][count].cols.y[k].col
                            equals = lib.bootstrap(lib.has(base_y), lib.has(diff_y)) and lib.cliffsDelta(lib.has(base_y), lib.has(diff_y))

                            if not equals:
                                if i == 0:
                                    # should never fail for all to all, unless sample size is large
                                    print("WARNING: all to all {} {} {}".format(i, k, "false"))
                                    print(f"all to all comparison failed for {results[base][count].cols.y[k].col.txt}")

                                comparisons[i][1][k] = "≠"
            count += 1
        
        
        headers = [y.col.txt for y in data.cols.y]
        table = []

        for k, v in results.items():
            # set the row equal to the average stats
            stats = get_stats(v)
            stats_list = [k] + [stats[y] for y in headers]

            # adds on the average number of evals
            stats_list += [n_evals[k] / 20]

            table.append(stats_list)
        
        print(tabulate(table, headers=headers + ["Avg evals"], numalign="right"))
        print()

        table = []

        # for each comparison of the algorithms
        #    append the = / !=
        for [base, diff], result in comparisons:
            table.append([f"{base} to {diff}"] + result)

        print(tabulate(table, headers=headers, numalign="right"))


# def main(options, help, funs, saved = {}, fails = 0):
#     for k, v in lib.cli(lib.settings(help)).items():
#         options[k] = v
#         saved[k] = v
#     if options["help"]:
#         print(help)
#     else:
#         for what in funs:
#             if options["go"] == "all" or what == options["go"]:
#                 for k,v in saved.items():
#                     options[k] = v
#                 if funs[what]() == False:
#                     fails = fails + 1
#                     print("❌ fail:", what)
#                 else:
#                     print("✅ pass:", what)
#     exit(fails)

# egs = {}
# def eg(key,str,func):
#     egs[key] = func
#     config.help = config.help + ("  -g  %s\t%s\n" % (key,str))

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

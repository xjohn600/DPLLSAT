#!/usr/bin/python3
# CMPT310 A2
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>


"""
#####################################################
#####################################################
import sys, getopt
import copy
import random
import time
import numpy as np
sys.setrecursionlimit(10000)


class SatInstance:
    def __init__(self):
        pass

    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if (maxvar > self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
        # Variables are numbered from 1 to p
        for i in range(1, self.p + 1):
            self.VARS.add(i)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s


def main(argv):
    inputfile = ''
    verbosity = False
    inputflag = False
    try:
        opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
    except getopt.GetoptError:
        print('DPLLsat.py -i <inputCNFfile> [-v] ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('DPLLsat.py -i <inputCNFfile> [-v]')
            sys.exit()
        ##-v sets the verbosity of informational output
        ## (set to true for output veriable assignments, defaults to false)
        elif opt == '-v':
            verbosity = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            inputflag = True
    if inputflag:
        instance = SatInstance()
        instance.from_file(inputfile)
        #start_time = time.time()
        solve_dpll(instance, verbosity)
        #print("--- %s seconds ---" % (time.time() - start_time))

    else:
        print("You must have an input file!")
        print('DPLLsat.py -i <inputCNFfile> [-v]')


# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#
#  You will need to define your own
#  DPLLsat(), DPLL(), pure-elim(), propagate-units(), and
#  any other auxiliary functions
def solve_dpll(instance, verbosity):
    # print(instance)
    # instance.VARS goes 1 to N in a dict
    # print(instance.VARS)
    # print(verbosity)
    ###########################################
    # Start your code
    clauses = instance.clauses

    variables = instance.VARS
    # print(instance)
    # print("clauses: ", clauses)
    assignment = set()
    variables = list(variables)
    # print("variables: ", variables)
    assignment = DPLLsat(clauses, variables, assignment)
    # print("Assigment:", assignment)
    if (assignment != False):
        assignment = [i for i in list(assignment) if 0 <= i]
        if (verbosity == True):
            print("SAT")
            print(assignment)
        else:
            print("SAT")
    else:
        print("UNSAT")
def DPLLsat(clauses, variables, assignment):
    #when it doesnt find sol, return false,
    #when returned false, 
    # print("DPLLSAT", variables, assignment, len(clauses))
    if (len(clauses) == 0):
        # print("returned: ", assignment)
        return assignment
    if (len(variables) == 0):
        # popped = assignment.pop()
        return False
        # print("hello")
    pure = findPure(clauses, variables)
    if (pure != False):
        targetVar = pure
        if (abs(targetVar) not in variables):
            return False
        variables.remove(abs(targetVar))
        assignment.add(targetVar)
        result = DPLLsat(removeVar(clauses, targetVar), variables, assignment)
        if (result != False):
            return result
        return False
    unit = findUnit(clauses)
    if (unit != False):
        targetVar = unit
        # print("Pure:", pure)
        if (abs(targetVar) not in variables):
            return False
        variables.remove(abs(targetVar))
        assignment.add(targetVar)
        result = DPLLsat(removeVar(clauses, targetVar), variables, assignment)
        if (result != False):
            return result
        return False
    else:
        targetVar = random.choice(variables)
        # print("target:", targetVar)
        # assignmentPos = copy.deepcopy(assignment)
        assignmentNeg = copy.deepcopy(assignment)
        # variablesPos = copy.deepcopy(variables)
        variablesNeg = copy.deepcopy(variables)
        # clausesPos = copy.deepcopy(clauses)
        clausesNeg = copy.deepcopy(clauses)
        # assignmentPos.add(targetVar)
        assignment.add(targetVar)
        assignmentNeg.add(-targetVar)
        # variablesPos.remove(targetVar)
        variables.remove(targetVar)
        variablesNeg.remove(targetVar)
        result1 = DPLLsat(removeVar(clauses, targetVar), variables, assignment)
        if (result1 != False):
            return result1
        #variables.append(-targetVar)
        result2 = DPLLsat(removeVar(clausesNeg, -targetVar), variablesNeg, assignmentNeg)
        #     variables.append(-targetVar)
        # else:
        return result2
        # variables.append(targetVar)
    # for clause in clauses:
    #     if (-targetVar in clause):
    #         clausesNeg.remove(clause)
    #         assignmentNeg.add(-targetVar)
    # print(variables, assignmentPos, assignmentNeg)
    # DPLLsat(clausesPos, variables, assignmentPos)
    # DPLLsat(clausesNeg, variables, assignmentNeg)
def findUnit(clauses):
    var = False
    for clause in clauses:
        if (len(clause) == 1):
            if (-var in clause):
                return False
            var = clause[0]
            # print(clause)
    return var
def findPure(clauses, variables):
    variables = np.append(variables, np.negative(variables))
    # print(variables)
    symbols = set([x for clause in clauses for x in clause])
    for var in symbols:
        if -var not in symbols:
            return var
    # for var in variables:
    #     pure = any(-var in sublist for sublist in clauses)
    #     if (pure == False):
    #         return var
    #     for clause in clauses:
    #         if (-var in clause):
    #             # print(var, "has neg value, breaks loop")
    #             pure = False
    #             break
    #     if (pure == True):
    #         # print(var, "has no neg value")
    #         return var
    return False
def propagateUnits(clauses, var):
    # print("target:", -var, clauses)
    for clause in clauses:
        if (-var in clause):
            if (len(clause) == 1):
                return False
            clause.remove(-var)
    clauses = [x for x in clauses if x != []]
    # print("after:", clauses)
    return clauses
def removeVar(clauses, var):
    # for clause in clauses:
    #     print("clause: ", clause)
    #     if (var in clause):
    #         print("finds var")
    #         clauses.remove(clause)
    # original = copy.deepcopy(clauses)
    ret = propagateUnits(clauses, var)
    if (ret == False):
        return clauses
    clauses = [clause for clause in ret if var not in clause]
    # print(var)
    return clauses
            # assignmentPos.add(targetVar)


    ###########################################


if __name__ == "__main__":
    main(sys.argv[1:])

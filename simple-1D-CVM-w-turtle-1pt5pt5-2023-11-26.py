# -*- coding: utf-8 -*-

####################################################################################################
#
#===================================================================================================
#
# INTELLECTUAL PROPERTY NOTICE AND LICENSE-TO-USE
#
#===================================================================================================
#
# Code Created at: Themesis Development Labs, Themesis, Inc.
#
# *** MIT License ***
#
# Copyright 2023 Themesis, Inc.
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the “Software”), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#        
##===================================================================================================
#
# CODE DEVELOPMENT, UPDATES, AUTHORSHIP
#
#===================================================================================================
#
# Code created by: Alianna J. Maren; assigned to Themesis, Inc.
# Initial code creation date: 2023-07-23
# Code based on earlier object-oriented experiments: July 27, 2018, by AJM
#
#
#===================================================================================================
#
# HIGH-LEVEL CODE DESCRIPTION:
#
#===================================================================================================
# 
# Computing configuration variables for the
#   and drawing the pattern using Python turtles
# Tutorial using object-oriented Python to create and populate a
#   list of nodes for the 1-D Cluster Variation Method (1D CVM),
#   and then compute the configuration variables for the resulting 1D CVM grid.
# The 1D CVM grid is printed out within the program, and is separately drawn using
#   Python turtles.
#
#
##===================================================================================================
#
# DETAILED CODE DESCRIPTION:
#
#===================================================================================================
# 
# This code works with a single Python object, Node.
# It creates a 1-D grid of Nodes, described initially by Kikuchi (1952) as a "single zigzag chain,"
#   initially populated with 0-value activations 
#   togetehr with 0-values for the next-nearest neighbor weights 'w' (in the same row only).
#
# Then, it creates a set of pre-defined values for certain Nodes, and then
#   computes the actual w-values associated with each of these Nodes.
# Then it prints the updated Node activations and w-values.
#
##===================================================================================================
#
# BUG REPORTS:
    # 2023/11/26 - Documentation in previous code (v1pt4) referred to the wLeft, wRight values 
    #              as "nearest-neighbor" when they should have been identified as "next-nearest-neighbor,"
    #              wLeft, wRight documentation now fixed for this version. 
    # 2023/11/26 - Duplicate functions removed - earlier (v1pt4) version had duplicate code for 
    #              computing the wLeft, wRight values for node_list2; those were removed
#
#===================================================================================================
# Address bug reports: themesisinc1@gmail.com
#
####################################################################################################

# Import the following Python packages

import random
import itertools
import numpy as np
import pylab
import matplotlib
from math import exp
from math import log
from matplotlib import pyplot as plt
# (not sure this is needed, since I'm importing random)
from random import randrange, uniform


import turtle


####################################################################################################
####################################################################################################
#
# Detailed code documentation is JUST ABOVE main(), at the very end of this program.
#
####################################################################################################
####################################################################################################
#
# Code Update Log:
#   07/26/2023: Created base code and GitHub public repository: Simple-1D-CVM-Demos
#     - Added a new pattern - a single big round of x1 in the middle of an x2 sea.
#
####################################################################################################
####################################################################################################


####################################################################################################
####################################################################################################
#
# Object-oriented class definition for Node.
#
####################################################################################################
####################################################################################################

class Node(object):
    """__init__() functions as the class constructor"""

    def __init__(self, node_num=None, row=None, col=None, activ=None, wLeft=None, wRight=None,
                 yLeft=None, yRight=None, zLeft=None, zRight=None):
        self.node_num = node_num
        self.row = row
        self.col = col
        self.activ = activ
        self.wLeft = wLeft
        self.wRight = wRight
        self.yLeft = yLeft
        self.yRight = yRight
        self.zLeft = zLeft
        self.zRight = zRight


####################################################################################################
####################################################################################################
#
# Printing procedures
#
####################################################################################################
####################################################################################################

#===================================================================================================
#
# WELCOME PRINT: Procedure to welcome the user and identify the code
#
#===================================================================================================

def welcome():

    print()
    print()
    print()
    print()
    print()
    print()
    print('******************************************************************************')
    print()
    print('Welcome to the 1-D Cluster Variation Method (1D CVM)')
    print('Version 1.1, 07/26/2023, A.J. Maren for Themesis, Inc.')
    print('  and updated 07/27/2023, by A.J. Maren for Themesis, Inc.')
    print()
    print('INTELLECTUAL PROPERTY DECLARATION:') 
    print('  This code has been developed under Internal Research and Development (IR&D) funding')
    print('    at the Development Labs of Themesis, Inc.')
    print('  Themesis, Inc. makes this code publicly available under the MIT License.')
    print()
    print('This version works with a pre-defined 1D array to identify the')
    print('  configuration variables,and also finds various thermodynamic values.')
    print('It uses a Python turtle to draw the 1D CVM grid.')
    print()
    print()
    print('For comments, questions, or bug-fixes, contact: themesisinc1@gmail.com')
    print()
    print('NOTE: In these calculations, x1 = A (units are at value 1),')
    print('                         and x2 = B (units are at value 0).')
    print()
    print('******************************************************************************')
    print()
    return()


#===================================================================================================
#
# DEBUG PRINT: Procedure to print out debug status of the code. 
#   Debug status can be changed within __main__
#
#===================================================================================================

def print_debug_status(debug_print_off):

    if not debug_print_off:
        print()
        print('Debug printing is on')  # debug_print_off false
    else:
        print('Debug printing is off')  # debug_print_off true
    print()
    print('******************************************************************************')
    print()
    return()


#===================================================================================================
#
# FIRST NODE SELECTION INFO PRINT: 
#   Procedure to tell user that the coming task is to select a first node.
#
#===================================================================================================

def print_first_node_selection_directions():

    print()
    print("You can select two nodes to swap; these should be one ON node and one OFF node")
    print()
    print("  First node:")
    print()
    return()


#===================================================================================================
#
# FIRST NODE SELECTION INFO PRINT: 
#   Procedure to tell user that the coming task is to select a first node.
#
#===================================================================================================

def print_second_node_selection_directions():
    print()
    print("You can now select the SECOND of two nodes to swap;")
    print("  this node should have a different activation (on/off status) from your first node.")
    print()
    print("  Second node:")
    print()        
    return()    

#===================================================================================================
#
#  GRID DIMENSIONS PRINT: Procedure to print out DIMENSIONS of the CVM grid. 
#
#===================================================================================================

def print_initial_array_size_values():
    print()
    print("This is the grid layout for a (currently 1-D) CVM grid")
    print("  This grid has dimensions of ", array_layers,
          "rows and ", array_length, " columns.")
    print()
    print("NOTE: If there are just two rows, then by default")
    print("  we are creating a single zig-zag chain for the 1-D CVM.")
    print()
    print("This print does not show the wrap-arounds.")
    print()
    return()


#===================================================================================================
#
#  PRINT GRID NODE VALUES: Procedure to print out the node activations and config var values for the grid 
#
#===================================================================================================

def print_grid_node_values(node_list):
    print()
    print("----------------------------------------------------------------------")
    print("  *** Node values after assigning certain nodes an activation of 1 ***")
    print("----------------------------------------------------------------------")
    x = 0
    for i in range(array_layers):
        print()
        print("Row ", i)
        print(" Col:   Activation:    wLeft      wRight     yLeft      yRight   zLeft      zRight    nodeNum")
        for j in range(array_length):
            thisCol = node_list[x].col
            thisActiv   = node_list[x].activ
            thisWLeft   = node_list[x].wLeft
            thisWRight  = node_list[x].wRight           
            thisYLeft   = node_list[x].yLeft
            thisYRight  = node_list[x].yRight
            thisZLeft   = node_list[x].zLeft
            thisZRight  = node_list[x].zRight            
            thisNum     = node_list[x].node_num
            print("  ", thisCol, "       ", thisActiv, "         ",
                  thisWLeft, "         ", thisWRight, "       ", 
                  thisYLeft, "         ", thisYRight, "       ", 
                  thisZLeft, "         ", thisZRight, "       ", thisNum)
            x = x+1
    
    print()
    print()
    print("This is a visual depiction of the grid layout")
    print("(showing wrap-around of first column to far right)")
    print()
    x = 0
    for i in range(array_layers):
        if i % 2 == 0:
            evenNum = True  # Even
        else:
            evenNum = False  # Odd
        print("Row ", i, ":  ", end="")
        if evenNum == False:
            print("  ", end="")
        for j in range(array_length):
            if node_list[x].activ == 0:
                print("-  ", end="")
            else:
                print("X  ", end="")
    # Print the wrap-around
            x = x+1
        if node_list[x-array_length].activ == 0:
            print('o  ', end='')
        else:
            print('x  ', end='')
        print('  ')
    return()


#===================================================================================================
#
#  PRINT FRACTIONAL CONVIGURATION VARIABLE VALUES: Procedure to print out the fractional config var values 
#
#===================================================================================================

def print_frac_config_values(config_vars_list, call_num):

    y1 = config_vars_list[0]
    y2 = config_vars_list[1]
    y3 = config_vars_list[2]   
    w1 = config_vars_list[3]
    w2 = config_vars_list[4]
    w3 = config_vars_list[5] 
    z1 = config_vars_list[6]
    z2 = config_vars_list[7]
    z3 = config_vars_list[8]   
    z4 = config_vars_list[9]
    z5 = config_vars_list[10]
    z6 = config_vars_list[11] 
    sum_y = y1 + y2 + y3
    sum_w = w1 + w2 + w3
    sum_z = z1 + z2 + z3 + z4 + z5 + z6
    
    print()
    print()
    print("----------------------------------------------------------------------")
    if call_num == 1:
        print("  *** Fractional Configuration Variable Values for the Original Grid ***")
    if call_num == 2:
        print("  *** Fractional Configuration Variable Values for the Revised Grid ***")
    print("----------------------------------------------------------------------")
    print()
    print("     y1       2*y2         y3         w1       2*w2         w3       Sum y      Sum w")
    print("  ", "%.3f" % y1, "    ", "%.3f" % y2, "    ", "%.3f" % y3,
          "    ", "%.3f" % w1, "    ", "%.3f" % w2, "    ", "%.3f" % w3, "    ", "%.3f" % sum_y, "    ", "%.3f" % sum_w)
    print()
    print("     z1       2*z2         z3         z4       2*z5         z6       Sum z")
    print("  ", "%.3f" % z1, "    ", "%.3f" % z2, "    ", "%.3f" % z3,
          "    ", "%.3f" % z4, "    ", "%.3f" % z5, "    ", "%.3f" % z6, "    ", "%.3f" % sum_z)
    print()
    return()
    


 ####################################################################################################
 ####################################################################################################
 #
 # Function to obtain the specifications for a turtleGridList
 #
 # Note: The code is ONLY set up to work with a grid consisting of an EVEN number of rows
 #
 ####################################################################################################
 ####################################################################################################

def obtain_turtle_grid_list(turtle_grid_list, array_size_list, node_list, node_list2, node1_num, node2_num):

   
#    print('In obtain_turtle_grid_list: The turtle_grid_list is', turtle_grid_list[0], turtle_grid_list[1]) 

    array_length = array_size_list[0]
    array_layers = array_size_list[1]  
    array_size = array_length*array_layers
 
# Create the initial node_list populated with position counts 
#   and zero-value fields for activation and config var counts

# Put the activations of the first node list (node_list) into the turtle_grid_list
    x=0
    for i in range(array_layers):
        for j in range(array_length):
            turtle_grid_list.append(node_list[x].activ)
            x = x+1

# Put the activations of the second node list (node_list2) into the turtle_grid_list
    x=0
    for i in range(array_layers):
        for j in range(array_length):
            turtle_grid_list.append(node_list2[x].activ)
            x = x+1            

# Change the activations in the turtle_grid_list nodes corresponding to the nodes 
#   whose activations were changed
    if node_list[node1_num].activ == 0:
        turtle_grid_list[array_size + node1_num] = 3          
    else:    
        turtle_grid_list[array_size + node1_num] = 2           
    if node_list[node2_num].activ == 0:
        turtle_grid_list[array_size + node2_num] = 3      
    else:    
        turtle_grid_list[array_size + node2_num] = 2  
        
    return (turtle_grid_list)


####################################################################################################
####################################################################################################
#
# Procedure to print turtle boxes depicting the 1D CVM grid
#
####################################################################################################
####################################################################################################

def turtle_grid(turtle_grid_list, array_length, array_size):
    
    window = turtle.Screen()
    turtle.speed(5)
    turtle.pensize(5)

    # draw the outline of a series of squares corresponding to the 1D CVM grid
    turtle.penup()


# draw the two rows of grids for the first grid (node_list)
    turtle.goto(-100, 100)
    initHorizStart = -350
    vertstart = 250
    for j in range(array_length):
        horizstart = j*50 + initHorizStart
        turtle.goto(horizstart, 50)
        turtle.pendown()
        if turtle_grid_list[j] == 0:
            turtle.color("blue", "white")
        if turtle_grid_list[j] == 1:
            turtle.color("black", "black")
        turtle.begin_fill()
        for i in range(4):
            turtle.forward(40)
            turtle.left(90)
        turtle.end_fill()
        turtle.penup()

    turtle.goto(-100, 100)
    initHorizStart = -325
    vertstart = 250
    for j in range(array_length):
        horizstart = j*50 + initHorizStart
        turtle.goto(horizstart, 0)
        turtle.pendown()
        if turtle_grid_list[j + array_length] == 0:
            turtle.color("blue", "white")
        if turtle_grid_list[j + array_length] == 1:
            turtle.color("black", "black")
        turtle.begin_fill()
        for i in range(4):
            turtle.forward(40)
            turtle.left(90)
        turtle.end_fill()
        turtle.penup()

# draw the two rows of grids for the second grid (node_list2)  

# starting position for the activations in node_list2

    turtle.goto(-100, 100)
    initHorizStart = -350
    vertstart = 250
    for j in range(array_length):
        horizstart = j*50 + initHorizStart
        turtle.goto(horizstart, 250)
        turtle.pendown()
        if turtle_grid_list[array_size + j] == 0:
            turtle.color("blue", "white")
        if turtle_grid_list[array_size + j] == 1:
            turtle.color("black", "black")
        if turtle_grid_list[array_size + j] == 2:
            turtle.color("red", "white")  
        if turtle_grid_list[array_size + j] == 3:
            turtle.color("red", "red")            
        turtle.begin_fill()
        for i in range(4):
            turtle.forward(40)
            turtle.left(90)
        turtle.end_fill()
        turtle.penup()
         
    turtle.goto(-100, 100)
    initHorizStart = -325
    vertstart = 250
    for j in range(array_length):
        horizstart = j*50 + initHorizStart
        turtle.goto(horizstart, 200)
        turtle.pendown()
        if turtle_grid_list[array_size + j + array_length] == 0:
            turtle.color("blue", "white")
        if turtle_grid_list[array_size + j + array_length] == 1:
            turtle.color("black", "black")
        if turtle_grid_list[array_size + j + array_length] == 2:
            turtle.color("red", "white")  
        if turtle_grid_list[array_size + j + array_length] == 3:
            turtle.color("red", "red")    
        turtle.begin_fill()
        for i in range(4):
            turtle.forward(40)
            turtle.left(90)
        turtle.end_fill()
        turtle.penup()         

    turtle.exitonclick()

    return()



####################################################################################################
####################################################################################################
#
# GRID DIMENSIONS VERSION 1: Function to obtain the array size specifications. 
#   Grid dimensions are currently DEFINED for the user; not a choice.
#
#   NOTE: The code is ONLY set up to work with a grid consisting of an EVEN number of rows.
#   NOTE: THIS is the function currently in use in the 1D CVM code version. 
#
####################################################################################################
####################################################################################################

def obtain_array_size_list():    

# The grid dimensions are fixed in this version of the code, and are set to create a 1D CVM grid. 
# Note that the variables array_length and array_layers are GLOBAL, but are encased in a list and 
#   passed back to the __main__ program to ensure consistency with future code versions.      
    array_length = 12
    array_layers = 2
                       
    array_size_list = (array_length, array_layers)  
    return (array_size_list)     



####################################################################################################
####################################################################################################
#
# GRID DIMENSIONS VERSION 2: Function to obtain the array size specifications.
#   This is a more general function, which can be used when defining the 2D CVM grid. 
#   Grid dimensions can be user-defined when this function is used. 
#   In the current 1D CVM code version, the grid dimensions are EFINED for the user; not a choice).
#
#   NOTE: The code is ONLY set up to work with a grid consisting of an EVEN number of rows.
#
####################################################################################################
####################################################################################################

def obtain_array_size_specs():

    #    x = input('Enter array_length: ')
    #    array_length = int(x)
    #    print 'array_length is', array_length

    #    x = input('Enter layers: ')
    #    layers = int(x)
    #    print 'layers is', layers

    #   NOTE: The system is designed to work with an even number of rows, e.g. layers must be an even number

    array_length = 12
    array_layers = 2

    array_size_list = (array_length, array_layers)


# TEST to ensure that the number of array_layers is even. 
    if array_layers % 2 == 0:
        even_layers == True  # then an even number of layers

# Determine the total number of PAIRS of zigzag chains. 
    pairs_layers = array_layers/2
    pairs = int(pairs_layers + 0.01)

# The following function is not defined for this version of the code. 
#    print_grid_size_specs () # Used when debugging

    return(array_size_list)
    


####################################################################################################
####################################################################################################
#
# Function to obtain values for the nodes in the grid,
#   as well as the following LOCAL configuration variables associated with each node:
#   - w (next-nearest-neighbor values)
# Returns the list of node objects (including their local config vars to )__main__
#
####################################################################################################
####################################################################################################

def obtain_node_list(node_list, array_size_list):

    array_length = array_size_list[0]
    array_layers = array_size_list[1]
    actvtn = 0
    wLeft = 0
    wRight = 0
    yLeft = 0
    yRight = 0
    zLeft = 0
    zRight = 0

    x = 0
    for i in range(array_layers):
        for j in range(array_length):
            node_list.append(Node(x, i, j, actvtn, wLeft, wRight, yLeft, yRight, zLeft, zRight))
            x = x+1

    return(node_list) 
 
  
####################################################################################################
####################################################################################################
#
# Function to obtain a list of the configuration variables; 
#   variable values initially assigned as 0. 
#
####################################################################################################
####################################################################################################

def obtain_config_vars_list():
    y1 = float(0.00)
    y2 = float(0.00)
    y3 = float(0.00)
    w1 = float(0.00)
    w2 = float(0.00)
    w3 = float(0.00) 
    z1 = float(0.00)
    z2 = float(0.00)
    z3 = float(0.00)
    z4 = float(0.00)
    z5 = float(0.00)
    z6 = float(0.00)       
    config_vars_list = [y1, y2, y3, w1, w2, w3, z1, z2, z3, z4, z5, z6]
    
    return(config_vars_list)    
      
####################################################################################################
####################################################################################################
#
# Function to obtain SPECIFIC activation values for the nodes in the grid,
# Returns the list of node objects (including their local config vars to) __main__
#
####################################################################################################
####################################################################################################
 
def assign_activations_node_list(node_list, array_size_list):        

    
    array_length = array_size_list[0]
    array_layers = array_size_list[1]  

    # This assigns activations of '1" to certain nodes
    x = 0
    for i in range(array_layers):
        for j in range(array_length):
            if i == 0:  # Turn on some nodes in Row 0
                # Assign value of "1" to first three nodes in Row 1  (nodes 0 .. 2)
                if j < 3:
                    node_list[x].activ = 1
                if j > 3:  # In the second set of four columns (columns 4 .. 7)
                    if j < 7:  # Assign value of "1" to nodes 4 .. 6 in Row 1
                        node_list[x].activ = 1
                if j > 7:  # In the third set of four columns (columns 8 .. 11)
                    if j < 11:  # Assign value of "1" to nodes 8 .. 10 in Row 1
                        node_list[x].activ = 1
            if i == 1:  # Turn on some nodes in Row 1
                if j < 1:  # Assign value of "1" to zeroth node in Row 1
                    node_list[x].activ = 1
                if j > 3:  # In the second set of four columns
                    if j < 5:  # Assign value of "1" to fourth node in Row 1
                        node_list[x].activ = 1
                if j > 7:  # In the third set of four columns
                    if j < 9:  # Assign value of "1" to eighth node in Row 1
                        node_list[x].activ = 1
            x = x+1
    return(node_list)



####################################################################################################
####################################################################################################
#
# Function to obtain the following LOCAL configuration variables associated with each node:
#   - w (next-nearest-neighbor values)
# Returns the list of node objects (including their local config vars to) __main__
#
####################################################################################################
####################################################################################################

def assign_local_config_vars_node_list(node_list, array_size_list):
# -------------------
    
    # wLEFT: This updates the wLeft values given that certain nodes now have an activation of "1"
    x = 0
    for i in range(array_layers):
        for j in range(array_length):
            q = array_length*i    # q denotes first node of the i-th row
        # test to see if at the beginning of row; if so, assign the LOCATION from last element on row
            if j == 0:
            # the location of the node-to-left is actually at the far right (the wrap-around)
            # this location is (i+1)*array_length - 1
                l_loc = (i+1)*array_length - 1
        # else: the node is NOT at the beginning of a row
            else: 
                l_loc = x - 1
        # The location of the next-nearest-neighbor node to the left is now identified as "l_loc."

        # For simplicity in expression, we create a varible for the activation of the 
        #   next-nearest-neighbor to the left. 
            l_activtn = node_list[l_loc].activ
        # Now, we denote the wLeft values based on the activation values for both the 
        #   node in question (x) and also the next-nearest-neighbor node to the left.               
            if node_list[x].activ == 1:
               if l_activtn == 1: 
                   node_list[x].wLeft = 1  # Denotation for w1; both activs = 1
               else: node_list[x].wLeft = 2  # Denotation for w2; one activ = 1, one = 0   
            else: # Case where node_list[x].activ == 0
               if l_activtn == 1: 
                   node_list[x].wLeft = 2  # Denotation for w2; one activ = 1, one = 0 
               else: node_list[x].wLeft = 3  # Denotation for w3; both activs = 0   
            x = x+1

# -------------------

    # wRIGHT: This updates the wRight values given that certain nodes now have an activation of "1"
    x = 0
    for i in range(array_layers):
        for j in range(array_length):
            q = array_length*i    # q denotes first node of the i-th row
        # test to see if at the end of row; if so, assign the LOCATION from first element on row
            if j == array_length-1:
            # The location of the node-to-right is actually at the far left (the wrap-around)
            #   this location is (i)*array_length.
            # For the first row (i = 0), the node-to-the-right for the far right node is at
            #   location 0 (r_loc = 0), which we can compute as i*array_length = 0*12 = 0. 
            # For the second row (i = 1), the node-to-the-right for the far right node is at
            #  location i*array_length, which in this case is 1 * 12 = 12.
                r_loc = i*array_length
        # else: the node is NOT at the end of a row
            else: 
                r_loc = x + 1
        # The location of the next-nearest-neighbor node to the right is now identified as "r_loc."
        
        # Now - DIFFERENT from the code for wLeft (above) - we consider the case where we are
        #  at the end of the SECOND ROW, and we need to look back at the beginning of the 
        #  SECOND ROW to find the corresponding node for wRight. 
        

        # For simplicity in expression, we create a varible for the activation of the 
        #   next-nearest-neighbor to the right. 
            r_activtn = node_list[r_loc].activ
        # Now, we denote the wRight values based on the activation values for both the 
        #   node in question (x) and also the next-nearest-neighbor node to the right.               
            if node_list[x].activ == 1:
               if r_activtn == 1: 
                   node_list[x].wRight = 1  # Denotation for w1; both activs = 1
               else: node_list[x].wRight = 2  # Denotation for w2; one activ = 1, one = 0   
            else: # Case where node_list[x].activ == 0
               if r_activtn == 1: 
                   node_list[x].wRight = 2  # Denotation for w2; one activ = 1, one = 0 
               else: node_list[x].wRight = 3  # Denotation for w3; both activs = 0    
            x = x+1

# -------------------

    # yLEFT: This updates the yLeft values given that certain nodes now have an activation of "1"
    # Computations for both yLeft and yRight are for nodes on the diagonal to the given node, 
    #   meaning that they are on the row above or below the row for the given node. 
    # For the 1-D CVM, if we are in row 0 (an EVEN row), then the row for yLeft and yRight is row 1; 
    #   if we are in row 1 (an ODD) row, then the row for yLeft and yRight is row 0.
    # We will do an even/odd row number test, to make the code more general (and applicable for the 2-D case).
    
    x = 0
    for i in range(array_layers):
    # Identify whether we are in an even or odd row. 
        if (i%2) == 0:  # Then we are in an EVEN row
        # Case for an EVEN row
            for j in range(array_length):
            # test to see if at the beginning of row; if so, assign the LOCATION from last element on NEXT row
                if j == 0:
                # the location of the node-to-lower-left is actually 
                #   at the far right (the wrap-around) of the NEXT ROW DOWN
                # this location is (i+1)*array_length + array_length - 1
                #   or (i+2)*array_length - 1
                    l_diag_loc = (i+2)*array_length - 1
            # else: the node is NOT at the beginning of a row
            #   the yLeft is at the next row down, but at the SAME "j" value (due to offset of that next row)
                else: 
                    l_diag_loc = (i+1)*array_length + j - 1
            # The location of the nearest-neighbor node to the left is now identified as "l_diag_loc."
            #
            # For simplicity in expression, we create a varible for the activation of the 
            #   nearest-neighbor to the left. 
                l_activtn = node_list[l_diag_loc].activ
#                print('node = ', x, 'node-activ = ', node_list[x].activ, 'yLeft = ', l_diag_loc, 'yLeft-activ = ', node_list[l_diag_loc].activ)
            # Now, we denote the yLeft values based on the activation values for both the 
            #   node in question (x) and also the nearest-neighbor node to the left.               
                if node_list[x].activ == 1:
                   if l_activtn == 1: 
                       node_list[x].yLeft = 1  # Denotation for y1; both activs = 1
                   else: node_list[x].yLeft = 2  # Denotation for y2; one activ = 1, one = 0   
                else: # Case where node_list[x].activ == 0
                   if l_activtn == 1: 
                       node_list[x].yLeft = 2  # Denotation for y2; one activ = 1, one = 0 
                   else: node_list[x].yLeft = 3  # Denotation for y3; both activs = 0   
                x = x+1

        else:  # We are in an ODD row
        # Case for an ODD row
            for j in range(array_length):
            # We don't need a separate test to see if at the beginning of row; 
            #   all the yLeft elements have the same "j" value and are on UPPER row
                l_diag_loc = (i-1)*array_length + j
            # The location of the nearest-neighbor node to the left is now identified as "l_diag_loc."      
            #
            # For simplicity in expression, we create a varible for the activation of the 
            #   nearest-neighbor to the left. 
                l_activtn = node_list[l_diag_loc].activ
 #               print('node = ', x, 'node-activ = ', node_list[x].activ, 'yLeft = ', l_diag_loc, 'yLeft-activ = ', node_list[l_diag_loc].activ)
            # Now, we denote the yLeft values based on the activation values for both the 
            #   node in question (x) and also the nearest-neighbor node to the left.               
                if node_list[x].activ == 1:
                   if l_activtn == 1: 
                       node_list[x].yLeft = 1  # Denotation for y1; both activs = 1
                   else: node_list[x].yLeft = 2  # Denotation for y2; one activ = 1, one = 0   
                else: # Case where node_list[x].activ == 0
                   if l_activtn == 1: 
                       node_list[x].yLeft = 2  # Denotation for y2; one activ = 1, one = 0 
                   else: node_list[x].yLeft = 3  # Denotation for y3; both activs = 0   
                x = x+1

# -------------------

    # yRIGHT: This updates the yRight values given that certain nodes now have an activation of "1"
    x = 0
    for i in range(array_layers):
    # Identify whether we are in an even or odd row. 
        if (i%2) == 0:  # Then we are in an EVEN row
        # Case for an EVEN row
            for j in range(array_length):
            # We don't need to test whether we are at the beginning or end of the row,
            #   our yRight value is at thes SAME column number, next row DOWN
                r_diag_loc = (i+1)*array_length + j
            # For simplicity in expression, we create a varible for the activation of the 
            #   next-nearest-neighbor to the right. 
                r_activtn = node_list[r_diag_loc].activ
            # Now, we denote the yRight values based on the activation values for both the 
            #   node in question (x) and also the nearest-neighbor node to the right.               
                if node_list[x].activ == 1:
                   if r_activtn == 1: 
                       node_list[x].yRight = 1  # Denotation for y1; both activs = 1
                   else: node_list[x].yRight = 2  # Denotation for y2; one activ = 1, one = 0   
                else: # Case where node_list[x].activ == 0
                   if r_activtn == 1: 
                       node_list[x].yRight = 2  # Denotation for y2; one activ = 1, one = 0 
                   else: node_list[x].yRight = 3  # Denotation for y3; both activs = 0    
                x = x + 1

        else:
        # Case for an ODD row
           for j in range(array_length):       
            # Test to see if at the end of row; if so, assign the LOCATION from first element on row ABOVE
            #   for the case of a 1-D CVM; it will be the row BELOW for a 2-D, with wrap-arounds. 
                if j == array_length-1:
                # The location of the diagonal-node-to-right is actually at the far left (the wrap-around)
                #   of the row ABOVE (for the 1-D zigzag chain); 
                #   this location is (i-1)*array_length + (i)*array_length;
                #   which is i*array_length.
                    r_diag_loc = i*array_length
            # else: the node is NOT at the end of a row
                else: 
                # The location of the     
                    r_diag_loc = (i-1)*array_length + j + 1
            # The location of the nearest-neighbor node to the right is now identified as "r_diag_loc."
            # For simplicity in expression, we create a varible for the activation of the 
            #   next-nearest-neighbor to the right. 
                r_activtn = node_list[r_diag_loc].activ
                # Now, we denote the yRight values based on the activation values for both the 
                #   node in question (x) and also the nearest-neighbor node to the right.               
                if node_list[x].activ == 1:
                   if r_activtn == 1: 
                       node_list[x].yRight = 1  # Denotation for y1; both activs = 1
                   else: node_list[x].yRight = 2  # Denotation for y2; one activ = 1, one = 0   
                else: # Case where node_list[x].activ == 0
                   if r_activtn == 1: 
                       node_list[x].yRight = 2  # Denotation for y2; one activ = 1, one = 0 
                   else: node_list[x].yRight = 3  # Denotation for y3; both activs = 0    
                x = x+1

# -------------------

    # zLEFT: This updates the zLeft values given that certain nodes now have an activation of "1"
    x = 0
    for i in range(array_layers):
        for j in range(array_length):             
            if node_list[x].activ == 1:  # Our node-for-computation is in state "A," and -
               if node_list[x].yLeft == 1:  # Our node to the lower-left diagonal is "A," and -
                   if node_list[x].wLeft == 1:  # Our node to the next-nearest-neighbor-left is "A," thus 
                       node_list[x].zLeft = 1  # We have an A-A-A triplet.
                   else:  # Our node to the next-nearest-neighbor-left is "B," thus - 
                       node_list[x].zLeft = 2  # We have a B-A-A triplet, counting from the left edge in. 
               else: # The middle node in the triplet is a "B" - 
                   if node_list[x].wLeft == 1:  # Our node to the next-nearest-neighbor-left is "A," thus 
                       node_list[x].zLeft = 3  # We have an A-B-A triplet.
                   else:  # Our node to the next-nearest-neighbor-left is "B," thus - 
                       node_list[x].zLeft = 5  # We have a B-B-A triplet, counting from the left edge in. 
            else:  # Our specific node is in state "B," so:  
               if node_list[x].yLeft == 3:  # Our node to the lower-left diagonal is "B," and - 
                   if node_list[x].wLeft == 3:  # Our node to the next-nearest-neighbor-left is "B," thus - 
                       node_list[x].zLeft = 6  # We have a B-B-B triplet.
                   else:  # Our node to the next-nearest-neighbor-left is "A," thus - 
                       node_list[x].zLeft = 5  # We have an A-B-B triplet, counting from the left edge in. 
               else: # The middle node in the triplet is an "A," and
                   if node_list[x].wLeft == 3:  # Our node to the next-nearest-neighbor-left is "B," thus - 
                       node_list[x].zLeft = 4  # We have an B-A-B triplet.
                   else:  # Our node to the next-nearest-neighbor-left is "A," thus - 
                       node_list[x].zLeft = 2  # We have a A-A-B triplet, counting from the left edge in.             
            x = x + 1


# -------------------

    return(node_list)



####################################################################################################
####################################################################################################
#
# USER INTERACTION: 
# Procedure to obtain user's first selection of a node to switch (in node_list2),
#   we will obtain the node activation here, and update the node config-vars in a 
#   different procedure.the selected node, as well as its activation, to __main__.
#
####################################################################################################
####################################################################################################
 
# --------------------------------------------------------------------
# User Interaction 1
# --------------------------------------------------------------------    

def obtain_new_node_list2 (array_length, array_layers):

    total_rows = array_layers
    total_columns = array_length

    # User picks a new row
    print("Select a row number between 0 and ", total_rows-1, "inclusive" )
    user_row = int(input("Please enter a row number: "))
    success = True
    if user_row>1:
        success = False
    if user_row<0:
        success = False   
    if success == True:
        print("Successful row pick")
        print()
    if success == False:
        new_try = 0
        while newTry < 3:
            new_try = new_try + 1
            user_row = int(input("Please select a row number that is either 0 or 1: "))
            if user_row < 2:
                if user_row > -1:
                    success = True
                    print("Successful row pick on new try: ", new_try, "with row number: ", user_row)
                    print()
                    break
                print("New try number: ", new_try)
    if success == False: 
        print("Oops! Looks like you're out of tries to select a row.")  
    
    # User picks a new column
    print("Select a column number between 0 and ", total_columns, "inclusive" )    
    user_col = int(input("Please enter a column number: "))
    success = True
    if user_col>total_columns:
        success = False
    if user_col<0:
        success = False   
    if success == True:
        print("Successful column pick")
        print()    
    if success == False:
        new_try = 0
        while new_try < 3:
            new_try = new_try + 1
            user_col = int(input("Please select a column number that is within range: "))
            if user_col < total_columns:
                if user_col > -1:
                    success = True
                    print("Successful column pick on new try: ", new_try, "with column number: ", user_col)
                    print()
                    break
                print("New try number: ", new_try)
    if success == False: 
        print("Oops! Looks like you're out of tries to select a column.")  
       
    print()
    print("Your node selection is at row ", user_row, " and column ", user_col)
    node1_num = user_row*total_columns + user_col
    print()
    
    return(node1_num)


# --------------------------------------------------------------------
# Test the user-selected nodes to be sure they are different
# --------------------------------------------------------------------  

def node_difference_test(node1_num, node2_num, nodes_different, node_list):

    node1_activ = node_list[node1_num].activ 
    node2_activ = node_list[node2_num].activ  
    print ('Node 1 activation is', node1_activ, 'and node 2 activation is', node2_activ)
    if node1_activ != node2_activ :
        nodes_different = True
        print ('The two nodes have different activations.')
    else:
        print ('The two nodes do NOT have different activations; program closing.')    
    return (nodes_different)



# --------------------------------------------------------------------
# Identify and update the new (swapped) node activations 
# --------------------------------------------------------------------    

def interchange_activations_node_list2(node1_num, node2_num, node_list, node_list2):
      
    node1_old_activ = node_list[node1_num].activ
    node2_old_activ = node_list[node2_num].activ
# Swap the activations
    node_list2[node1_num].activ = node2_old_activ
    node_list2[node2_num].activ = node1_old_activ

    print ('For the initial grid, node 1 activation is', node1_old_activ, 'and node 2 activation is', node2_old_activ)
    print ('For the new grid,     node 1 activation is', node_list2[node1_num].activ, 'and node 2 activation is', node_list2[node2_num].activ) 
    return(node_list2)



# --------------------------------------------------------------------
# Compute the actual fractional configuration variables 
# --------------------------------------------------------------------    

def obtain_actual_config_vars_list(config_vars_list, node_list, array_length, array_layers):
      
    Y1 = config_vars_list[0]
    Y2 = config_vars_list[1]
    Y3 = config_vars_list[2]
    W1 = config_vars_list[3]
    W2 = config_vars_list[4]
    W3 = config_vars_list[5]    
    Z1 = config_vars_list[6]
    Z2 = config_vars_list[7]
    Z3 = config_vars_list[8]
    Z4 = config_vars_list[9]
    Z5 = config_vars_list[10]
    Z6 = config_vars_list[11]       
 
    x = 0
    for i in range(array_layers):
        for j in range(array_length):
            if node_list[x].yLeft == 1: Y1 = Y1 + 1
            if node_list[x].yLeft == 2: Y2 = Y2 + 1
            if node_list[x].yLeft == 3: Y3 = Y3 + 1            
            if node_list[x].wLeft == 1: W1 = W1 + 1
            if node_list[x].wLeft == 2: W2 = W2 + 1
            if node_list[x].wLeft == 3: W3 = W3 + 1  
            if node_list[x].zLeft == 1: Z1 = Z1 + 1
            if node_list[x].zLeft == 2: Z2 = Z2 + 1
            if node_list[x].zLeft == 3: Z3 = Z3 + 1            
            if node_list[x].zLeft == 4: Z4 = Z4 + 1
            if node_list[x].zLeft == 5: Z5 = Z5 + 1
            if node_list[x].zLeft == 6: Z6 = Z6 + 1  
            x = x + 1
 
 # Obtain the total number of nodes in the grid
#    array_length = array_size_list[0]
#    array_layers = array_size_list[1]
    total_nodes = array_length * array_layers
    
 # Obtain the fractional values for the configuration variables   

    y1 = Y1/total_nodes
    y2 = Y2/total_nodes
    y3 = Y3/total_nodes
    w1 = W1/total_nodes
    w2 = W2/total_nodes
    w3 = W3/total_nodes
    z1 = Z1/total_nodes
    z2 = Z2/total_nodes
    z3 = Z3/total_nodes
    z4 = Z4/total_nodes
    z5 = Z5/total_nodes
    z6 = Z6/total_nodes
    
 
    config_vars_list[0] = y1
    config_vars_list[1] = y2
    config_vars_list[2] = y3
    config_vars_list[3] = w1
    config_vars_list[4] = w2
    config_vars_list[5] = w3   
    config_vars_list[6] = z1
    config_vars_list[7] = z2
    config_vars_list[8] = z3
    config_vars_list[9] = z4
    config_vars_list[10] = z5
    config_vars_list[11] = z6   
    
    return(config_vars_list)


# --------------------------------------------------------------------
# Compute the system entropy 
# --------------------------------------------------------------------    

def compute_neg_entropy(config_vars_list):

    neg_entropy = 0

    y1 = config_vars_list[0]
    y2 = config_vars_list[1]*0.5 # Divide by two to account for degeneracy in counting originally
    y3 = config_vars_list[2]
    w1 = config_vars_list[3]
    w2 = config_vars_list[4]*0.5 # Divide by two to account for degeneracy in counting originally
    w3 = config_vars_list[5]    
    z1 = config_vars_list[6]
    z2 = config_vars_list[7]*0.5 # Divide by two to account for degeneracy in counting originally
    z3 = config_vars_list[8]
    z4 = config_vars_list[9]
    z5 = config_vars_list[10]*0.5 # Divide by two to account for degeneracy in counting originally
    z6 = config_vars_list[11]       
 
    neg_entropy_y = y1*log(y1) + 2.0* y2*log(y2) + y3*log(y3) 
    neg_entropy_z = z1*log(z1) + 2.0*z2*log(z2) + z3*log(z3) + \
                z4*log(z4) + 2.0*z5*log(z5) + z6*log(z6)   
                
    neg_entropy = -2.0*neg_entropy_y + 2.0*neg_entropy_z

    return(neg_entropy)

# --------------------------------------------------------------------
# Compute the system entropy 
# --------------------------------------------------------------------    

def compute_free_energy(config_vars_list, neg_entropy):

    enthalpy_range = 50
    enthalpy_incr = 0.01

    z2 = config_vars_list[7]*0.5 # Divide by two to account for degeneracy in counting originally
    z3 = config_vars_list[8]
    z4 = config_vars_list[9]
    z5 = config_vars_list[10]*0.5 # Divide by two to account for degeneracy in counting originally
     
    sum_z_enthalpy_terms = z2 + z3 + z4 + z5
    for i in range(enthalpy_range):
        epsilon1 = -(i*enthalpy_incr)
        enthalpy = epsilon1*sum_z_enthalpy_terms 
        free_energy = enthalpy + neg_entropy
        print('  When eps1 = ', "%.3f" % epsilon1, ' the enthalpy is ', "%.3f" % enthalpy, ' the free_energy is ', "%.3f" % free_energy)             

    return()

####################################################################################################
####################################################################################################

def main():

 ####################################################################################################
 # Obtain unit array size in terms of array_length (M) and layers (N)
 ####################################################################################################

    # Define global array parameters for the CVM grid
    global array_length
    global array_layers
    global even_layers
    global pairs

# Define global print parameters
    global blnkspc

# Define global debug parameters
    global debug_print_off
    global detailed_debug_print_off
    global z_debug_print_off
    global show_progress_adjust_matrix_off
    global explanation_thermodynamic_plot_off

# Define Boolean value for the grid array having an even number of layers
    even_layers = True
    
# Define a Boolean value for whether the two user-selected nodes are different
    nodes_different = False    

# Define a blank space value for printing
    blnkspc = ' '

# Define Boolean values for the global debug variables
#   Not all of these are used in the simple 1D CVM program(s) 
    debug_print_off = True
    detailed_debug_print_off = True
    z_debug_print_off = True
    show_progress_adjust_matrix_off = True
    explanation_thermodynamic_plot_off = True
    perform_analytics = True

# This is a local variable; it will be passed to compute_config_variables
# It will determine whether we print the contents of the x-array at the
#   beginning and end of the adjust-matrix step.
    beforeAndAfterAdjustedMatrixPrintOff = True
    


####################################################################################################
# The actual __main__ program starts here with function and procedure calls
####################################################################################################

# Start the welcome sequence
    welcome()
    print_debug_status(debug_print_off)

# Function call to get the actual dimensions of the 2D CVM grid
# This is kept in the 1D CVM code for consistency
    array_size_list = list()  # empty list
    array_size_list = obtain_array_size_list()
    array_length = array_size_list[0]
    array_layers = array_size_list[1]  

# Print the dimensions of the grid we will create
    print_initial_array_size_values()    

# Populate the grid with initial values
    node_list = list()  # empty list
    node_list = obtain_node_list(node_list, array_size_list)
    node_list = assign_activations_node_list(node_list, array_size_list)
    node_list = assign_local_config_vars_node_list(node_list, array_size_list) 
    
    print_grid_node_values(node_list)

# Function call to create the initial configuration variables list
    config_vars_list1 = list()  
    config_vars_list1 = obtain_config_vars_list()
    
# Function call to create the second configuration variables list
    config_vars_list2 = list()  
    config_vars_list2 = obtain_config_vars_list()    
  
#===================================================================================================     
# USER INTERACTION: Interchange two nodes.
#   These two nodes must have different activation values. 

# Populate a second grid to be identical to the first; 
#   This grid is what the user will modify.
    node_list2 = list()  # empty list
    node_list2 = obtain_node_list(node_list2, array_size_list)
    node_list2 = assign_activations_node_list(node_list2, array_size_list) 
    node_list2 = assign_local_config_vars_node_list(node_list2, array_size_list)
    
# There is no need to print this grid right now; 
#   it is currently identical to the first.  
    
# USER INTERACTION: Inform the user that the next task is to select a first node.    
    print_first_node_selection_directions()

# USER INTERACTION: Obtain the first node that the user wishes to swap.
    node1_num = obtain_new_node_list2 (array_length, array_layers) 

# USER INTERACTION: Inform the user that the next task is to select a second node.  
    print_second_node_selection_directions() 

# USER INTERACTION: Obtain the second node that the user wishes to swap.
    node2_num = obtain_new_node_list2 (array_length, array_layers) 
    
# Test to be sure the two nodes have different activations
    nodes_different = node_difference_test(node1_num, node2_num, nodes_different, node_list) 
    if nodes_different:
        node_list2 = interchange_activations_node_list2(node1_num, node2_num, node_list, node_list2)
        node_list2 = assign_local_config_vars_node_list(node_list2, array_size_list)

        print_grid_node_values(node_list2)  
       
    config_vars_list1 = obtain_actual_config_vars_list(config_vars_list1, node_list, array_length, array_layers)
    config_vars_list2 = obtain_actual_config_vars_list(config_vars_list2, node_list2, array_length, array_layers)
    
    call_num = 1
    print_frac_config_values(config_vars_list1, call_num)
    call_num = 2
    print_frac_config_values(config_vars_list2, call_num)   
    
    neg_entropy1 = compute_neg_entropy(config_vars_list1)
    neg_entropy2 = compute_neg_entropy(config_vars_list2)
    
    print('  Neg-Entropy for the original system is: ', "%.3f" % neg_entropy1)   
    print('  Neg-Entropy for the revised system is: ', "%.3f" % neg_entropy2)  
    
#    print()
#    print('  The free energy for the original system is ',  "%.3f" % neg_entropy1, ' where the enthalpy is 0.')
#   compute_free_energy(config_vars_list2, neg_entropy2)
    
#===================================================================================================


# Create a turtle_grid_list where the values are the activations of the nodes, in simple list order. 
    array_size = array_length*array_layers
    turtle_grid_list = list()
    turtle_grid_list = obtain_turtle_grid_list(turtle_grid_list, array_size_list, node_list, node_list2, 
                                               node1_num, node2_num)  

# Print the turtle grid. 
#    turtle_grid(turtle_grid_list, array_length, array_size)
    
####################################################################################################
# Conclude specification of the MAIN procedure
####################################################################################################

if __name__ == "__main__":
    main()

####################################################################################################
# End program

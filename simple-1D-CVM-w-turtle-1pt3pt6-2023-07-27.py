# -*- coding: utf-8 -*-

####################################################################################################
# Themesis, Inc.
# MIT License
# Code created by: Alianna J. Maren; assigned to Themesis, Inc.
# Initial code creation date: 2023-07-23
# Code based on earlier object-oriented experiments: July 27, 2018, by AJM
#
# HIGH-LEVEL CODE DESCRIPTION:
# Computing configuration variables for the
#   and drawing the pattern using Python turtles
# Tutorial using object-oriented Python to create and populate a
#   list of nodes for the 1-D Cluster Variation Method (1D CVM),
#   and then compute the configuration variables for the resulting 1D CVM grid.
# The 1D CVM grid is printed out within the program, and is separately drawn using
#   Python turtles.
#
# DETAILED CODE DESCRIPTION:
# This code works with a single Python object, Node.
# It creates a 1-D grid of Nodes, initially populated with 0-value activations
#   and 0-values for the next-nearest neighbor weights 'w' (in the same row only).
#
# Then, it creates a set of pre-defined values for certain Nodes, and then
#   computes the actual w-values associated with each of these Nodes.
# Then it prints the updated Node activations and w-values.
#
# Bug reports: themesisinc1@gmail.com
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

    def __init__(self, node_num=None, row=None, col=None, activ=None, wLeft=None, wRight=None):
        self.node_num = node_num
        self.row = row
        self.col = col
        self.activ = activ
        self.wLeft = wLeft
        self.wRight = wRight



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
        print(" Col:   Activation:    wLeft      wRight    nodeNum")
        for j in range(array_length):
            thisCol = node_list[x].col
            thisActiv = node_list[x].activ
            thisWLeft = node_list[x].wLeft
            thisWRight = node_list[x].wRight
            thisNum = node_list[x].node_num
            print("  ", thisCol, "       ", thisActiv, "         ",
                  thisWLeft, "         ", thisWRight, "       ", thisNum)
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



 ####################################################################################################
 ####################################################################################################
 #
 # Function to obtain the specifications for a turtleGridList
 #
 # Note: The code is ONLY set up to work with a grid consisting of an EVEN number of rows
 #
 ####################################################################################################
 ####################################################################################################

def obtain_turtle_grid_list(turtle_grid_list, array_size_list, node_list):

#    turtle_grid_list = list()
#    turtle_grid_list = [0, 1]
   
#    print('In obtain_turtle_grid_list: The turtle_grid_list is', turtle_grid_list[0], turtle_grid_list[1]) 

    array_length = array_size_list[0]
    array_layers = array_size_list[1]  
 
# Create the initial node_list populated with position counts 
#   and zero-value fields for activation and config var counts
    x=0
    for i in range(array_layers):
        for j in range(array_length):
            turtle_grid_list.append(node_list[x].activ)
            x = x+1
    
    return (turtle_grid_list)


####################################################################################################
####################################################################################################
#
# Procedure to print turtle boxes depicting the 1D CVM grid
#
####################################################################################################
####################################################################################################

def turtle_grid(turtle_grid_list, array_size_list):

    array_length = array_size_list[0]
    array_layers = array_size_list[1]  
    
    window = turtle.Screen()
    turtle.speed(5)
    turtle.pensize(5)

    # draw the outline of a series of squares corresponding to the 1D CVM grid
    turtle.penup()

    turtle.goto(-100, 100)
    initHorizStart = -350
    vertstart = 250
    for j in range(array_length):
        horizstart = j*50 + initHorizStart
        turtle.goto(horizstart, 100)
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

    next_row_start = array_length 

    turtle.goto(-100, 100)
    initHorizStart = -325
    vertstart = 250
    for j in range(array_length):
        horizstart = j*50 + initHorizStart
        turtle.goto(horizstart, 50)
        turtle.pendown()
        if turtle_grid_list[j + next_row_start] == 0:
            turtle.color("blue", "white")
        if turtle_grid_list[j + next_row_start] == 1:
            turtle.color("black", "black")
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

    wLeft = 0
    wRight = 0
    array_length = array_size_list[0]
    array_layers = array_size_list[1]
    unitVal = 0

    x = 0
    for i in range(array_layers):
        for j in range(array_length):
            node_list.append(Node(x, i, j, 0, 0, 0))
            print('Node number', node_list[x].node_num, 'Node row', node_list[x].row, 'node_list.col', node_list[x].col)
            x = x+1

    return(node_list) 
 
         
####################################################################################################
####################################################################################################
#
# Function to obtain SPECIFIC values for the nodes in the grid,
#   as well as the following LOCAL configuration variables associated with each node:
#   - w (next-nearest-neighbor values)
# Returns the list of node objects (including their local config vars to )__main__
#
####################################################################################################
####################################################################################################
 
def fill_values_node_list(node_list, array_size_list):        

    
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

# -------------------
    
    # wLEFT: This updates the wLeft values given that certain nodes now have an activation of "1"
    x = 0
    for i in range(array_layers):
        for j in range(array_length):
            q = array_length*i    # q denotes first node of the i-th row
            if j == 0:
                # test to see if at the beginning of row; if so, assign wRight from last element on row
                if node_list[q-1].activ == 0:
                    node_list[x].wLeft = 0
                else:
                    node_list[x].wLeft = 1
            else:
                if node_list[x-1].activ == 0:
                    node_list[x].wLeft = 0
                else:
                    node_list[x].wLeft = 1
            x = x+1

# -------------------

    # wRIGHT: This updates the wRight values given that certain nodes now have an activation of "1"
    x = 0
    for i in range(array_layers):
        for j in range(array_length):
            q = array_length*i    # q denotes first node of the i-th row
            # test to see if at the end of row; if so, assign wRight from first element on row
            if j == array_length-1:
                if node_list[q].activ == 0:
                    node_list[x].wRight = 0
                else:
                    node_list[x].wRight = 1
            else:
                if node_list[x+1].activ == 0:
                    node_list[x].wRight = 0
                else:
                    if node_list[x+1].activ == 0:
                        node_list[x].wRight = 0
                    else:
                        node_list[x].wRight = 1
            x = x+1

    return(node_list)



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

# Define a blank space value for printing
    blnkspc = ' '

# Define Boolean values for the global debug variables
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
    node_list = fill_values_node_list(node_list, array_size_list)
    
    print_grid_node_values(node_list)

# Create a turtle_grid_list where the values are the activations of the nodes, in simple list order. 
    turtle_grid_list = list()
    turtle_grid_list = obtain_turtle_grid_list(turtle_grid_list, array_size_list, node_list)  

# Print the turtle grid. 
    turtle_grid(turtle_grid_list, array_size_list)
    
####################################################################################################
# Conclude specification of the MAIN procedure
####################################################################################################

if __name__ == "__main__":
    main()

####################################################################################################
# End program

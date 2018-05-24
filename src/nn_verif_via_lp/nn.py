'''
Author: Daniel S. Fava
Year: 2018
License: CC BY 4.0
https://creativecommons.org/licenses/by/4.0/
'''
import numpy as np
import matplotlib.pyplot as plt

def nn_to_formula_components(coefs, intercepts, debug=False):
    layer_sizes = get_layer_sizes(coefs, intercepts)
    n_layers = len(layer_sizes)
    if debug: print(layer_sizes)
    formula_components = []
    for l, (layer_size_a, layer_size_b) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        if debug: print("Processing layer", l)
        for o in range(layer_size_b):
            neuron = []
            if debug: print("Processing neuron", o)
            neuron_name = "Y%d_%d" % (l,o)
            neuron_formula_components = []
            for m in range(layer_size_a):
                if (l==0):
                    input_name = "X%d" % m
                else:
                    input_name = "Y%d_%d" % (l-1,m)
                if debug: print(m,o)
                weight_str = str(round(coefs[l][m, o],4))
                neuron_formula_components.append(input_name + "*" + weight_str)
            bias = str(round(intercepts[l][o],4))
            neuron_formula_components.append(bias)
            formula_components.append([neuron_name, " + ".join(neuron_formula_components)])
    return formula_components

# Neural network to DNF form
def formula_components_to_dnf(formula_components, debug=False):
    formula = []
    for comb in range(0, 2 ** len(formula_components)):
        if debug: print("0b{0:b}".format(comb))
        clause = []            
        for idx in range(0,len(formula_components)):
            flag = (comb >> idx) & 0b1
            if (flag):
                if debug: print("one %d" % idx)
                clause.append("%s == %s" % (formula_components[idx][0], formula_components[idx][1]))
                clause.append("%s > 0" % formula_components[idx][0])
            else:
                if debug: print("zero %d" % idx)
                clause.append("%s == 0" % formula_components[idx][0])
                clause.append("%s <= 0" % formula_components[idx][1])
        if debug: print(clause); print()
        formula.append(clause)
    return formula

def get_layer_sizes(coefs, intercepts):
    in_layer_size = len(coefs[0])
    out_layer_size = len(intercepts[len(intercepts)-1])
    hidden_layer_sizes = []
    for hidden in coefs[1:]:
        hidden_layer_sizes.append(len(hidden))
    return [in_layer_size] + hidden_layer_sizes + [out_layer_size]

# The function below comes from a gist originally developed by @craffel,
# then improved by @ljhuang2017, then improved by @dvgodoy, then modified by @dfava
# https://gist.githubusercontent.com/dvgodoy/0db802cfb8edd488dfbd524302ca4be7/raw/f4b03e5a456329ab49c3c2f7af5a7ce8107156c4/draw_neural_net.py
def draw_neural_net(ax, left, right, bottom, top, coefs_, intercepts_, n_iter_, loss_):
    '''
    Draw a neural network cartoon using matplotilb.
    
    :usage:
        >>> fig = plt.figure(figsize=(12, 12))
        >>> draw_neural_net(fig.gca(), .1, .9, .1, .9, [4, 7, 2])
    
    :parameters:
        - ax : matplotlib.axes.AxesSubplot
            The axes on which to plot the cartoon (get e.g. by plt.gca())
        - left : float
            The center of the leftmost node(s) will be placed here
        - right : float
            The center of the rightmost node(s) will be placed here
        - bottom : float
            The center of the bottommost node(s) will be placed here
        - top : float
            The center of the topmost node(s) will be placed here
        - layer_sizes : list of int
            List of layer sizes, including input and output dimensionality
    '''
    layer_sizes = get_layer_sizes(coefs_, intercepts_)
    n_layers = len(layer_sizes)
    v_spacing = (top - bottom)/float(max(layer_sizes))
    h_spacing = (right - left)/float(len(layer_sizes) - 1)
    
    # Input-Arrows
    layer_top_0 = v_spacing*(layer_sizes[0] - 1)/2. + (top + bottom)/2.
    for m in range(layer_sizes[0]):
        plt.arrow(left-0.18, layer_top_0 - m*v_spacing, 0.12, 0,  lw =1, head_width=0.01, head_length=0.02)
    
    # Nodes
    for n, layer_size in enumerate(layer_sizes):
        layer_top = v_spacing*(layer_size - 1)/2. + (top + bottom)/2.
        for m in range(layer_size):
            circle = plt.Circle((n*h_spacing + left, layer_top - m*v_spacing), v_spacing/8.,
                                color='w', ec='k', zorder=4)
            if n == 0:
                plt.text(left-0.125, layer_top - m*v_spacing, r'$X_{'+str(m+1)+'}$', fontsize=15)
            elif (n_layers == 3) & (n == 1):
                plt.text(n*h_spacing + left+0.00, layer_top - m*v_spacing+ (v_spacing/8.+0.01*v_spacing), r'$H_{'+str(m+1)+'}$', fontsize=15)
            elif n == n_layers -1:
                plt.text(n*h_spacing + left+0.10, layer_top - m*v_spacing, r'$y_{'+str(m+1)+'}$', fontsize=15)
            ax.add_artist(circle)
    # Bias-Nodes
    for n, layer_size in enumerate(layer_sizes):
        if n < n_layers -1:
            x_bias = (n+0.5)*h_spacing + left
            y_bias = top + 0.005
            circle = plt.Circle((x_bias, y_bias), v_spacing/8., color='w', ec='k', zorder=4)
            plt.text(x_bias-(v_spacing/8.+0.10*v_spacing+0.01), y_bias, r'$1$', fontsize=15)
            ax.add_artist(circle)   
    # Edges
    # Edges between nodes
    for n, (layer_size_a, layer_size_b) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        layer_top_a = v_spacing*(layer_size_a - 1)/2. + (top + bottom)/2.
        layer_top_b = v_spacing*(layer_size_b - 1)/2. + (top + bottom)/2.
        for m in range(layer_size_a):
            for o in range(layer_size_b):
                line = plt.Line2D([n*h_spacing + left, (n + 1)*h_spacing + left],
                                  [layer_top_a - m*v_spacing, layer_top_b - o*v_spacing], c='k')
                ax.add_artist(line)
                xm = (n*h_spacing + left)
                xo = ((n + 1)*h_spacing + left)
                ym = (layer_top_a - m*v_spacing)
                yo = (layer_top_b - o*v_spacing)
                rot_mo_rad = np.arctan((yo-ym)/(xo-xm))
                rot_mo_deg = rot_mo_rad*180./np.pi
                xm1 = xm + (v_spacing/8.+0.05)*np.cos(rot_mo_rad)
                if n == 0:
                    if yo > ym:
                        ym1 = ym + (v_spacing/8.+0.12)*np.sin(rot_mo_rad)
                    else:
                        ym1 = ym + (v_spacing/8.+0.05)*np.sin(rot_mo_rad)
                else:
                    if yo > ym:
                        ym1 = ym + (v_spacing/8.+0.12)*np.sin(rot_mo_rad)
                    else:
                        ym1 = ym + (v_spacing/8.+0.04)*np.sin(rot_mo_rad)
                plt.text( xm1, ym1,\
                         str(round(coefs_[n][m, o],4)),\
                         rotation = rot_mo_deg, \
                         fontsize = 10)
    # Edges between bias and nodes
    for n, (layer_size_a, layer_size_b) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        if n < n_layers-1:
            layer_top_a = v_spacing*(layer_size_a - 1)/2. + (top + bottom)/2.
            layer_top_b = v_spacing*(layer_size_b - 1)/2. + (top + bottom)/2.
        x_bias = (n+0.5)*h_spacing + left
        y_bias = top + 0.005 
        for o in range(layer_size_b):
            line = plt.Line2D([x_bias, (n + 1)*h_spacing + left],
                          [y_bias, layer_top_b - o*v_spacing], c='k')
            ax.add_artist(line)
            xo = ((n + 1)*h_spacing + left)
            yo = (layer_top_b - o*v_spacing)
            rot_bo_rad = np.arctan((yo-y_bias)/(xo-x_bias))
            rot_bo_deg = rot_bo_rad*180./np.pi
            xo2 = xo - (v_spacing/8.+0.01)*np.cos(rot_bo_rad)
            yo2 = yo - (v_spacing/8.+0.01)*np.sin(rot_bo_rad)
            xo1 = xo2 -0.05 *np.cos(rot_bo_rad)
            yo1 = yo2 -0.05 *np.sin(rot_bo_rad)
            plt.text( xo1, yo1,\
                 str(round(intercepts_[n][o],4)),\
                 rotation = rot_bo_deg, \
                 fontsize = 10)    
                
    # Output-Arrows
    layer_top_0 = v_spacing*(layer_sizes[-1] - 1)/2. + (top + bottom)/2.
    for m in range(layer_sizes[-1]):
        plt.arrow(right+0.015, layer_top_0 - m*v_spacing, 0.16*h_spacing, 0,  lw =1, head_width=0.01, head_length=0.02)
    # Record the n_iter_ and loss
    plt.text(left + (right-left)/3., bottom - 0.005*v_spacing, \
             'Steps:'+str(n_iter_)+'    Loss: ' + str(round(loss_, 6)), fontsize = 15)

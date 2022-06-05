# EH2745-FEN3251-VT22-1-COMPUTER-APPLICATIONS-IN-POWER-SYSTEMS-ASSIGNMENT-2
Use of k-means and k-NN for power systems

## Description:
The purpose of Assignment II is to combine  the  machine  learning  techniques  and  the power system modeling techniques.
It  involves  defining  a  model  of  a  powergrid  using  PandaPower  and  then  run  a  time  series simulation  in  this  grid  to  create  a  dataset  of  measurements. This dataset in turn will serve as the base for a machine learning experiment. The two different machine learning algorithm are k-means and k-NearestNeighbor.

## What will you find:
All the scripts are "connected" meaning that some modules are used in more than one algorithm. Therefore, I'll explain what is the scope of each script:
- classes_A2: will contain the definition of the special classes used in all the other scripts
- dscreation_A2: creation of the dataset, dividing the result of the simulation into to matrices (training and validation).
- k-means: the k-mean algorithm is implemented here
- k-NN_optk: the k-NN algorithm is implemented here. In this case, the number of k depends on the result of the k-means algorithm (the optimal k)
- k-NN_GUI: the k-NN algorithm is implemented here. In this case, the number of k is decided by the user and the corresponding accuracy will be shown.

## Please note:
In the "dscreation_A2" there are some lines that need changes depending on the path of the file in your computer.
The number of the lines are: 162-164 and 178-180. 

By Alice Scalamandrè

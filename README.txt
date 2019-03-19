USAGE: COM_analysis.py <body definition file> <models file> <max value for colour scaling - optional>
---
body definition file = four columns text file
body_name       start_AA        end_AA      chain

models file =  text file list of models one per line 
---


models must be aligned to each other before running - use my script
'align_pdbs_on_body.py' from github.com/attamatti/movement_analysis 
or do it some other way.

max value for color sclaing is the max used for the colors in the correlatoin matrix.  This can be set if you want to make matrices for several different datasets but want them all on the same absolute color scale. If this is left blank the maximum value for the set you are running on is used.

If you need to use the resulting bildfiles in figures. Use the script bildfile_figure.py to change the sizes of the spheres and replace the vectors connecting them with thicker cylinders, whch will look much better.

USAGE: bildfile_figure.py <bild file> <cylinder thickness> <sphere size>

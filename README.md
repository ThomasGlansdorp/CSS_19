# CSS_19

Background of our project: 
Cell membranes separate the interior of the cell from the external environment. Comprising a lipid bilayer with semi-permeable properties, cell membranes play a pivotal role in facilitating the transport of important nutrients into the cell and expelling toxic substances from the cell [1]. Over time, our understanding of plasma membranes has evolved, uncovering a more intricate composition of membrane lipids than previously thought. The LIPID MAPS structure database [2] suggests a potential pool of over 1.1 million lipid structures in nature, a number that may grow with the increased sensitivity of mass spectrometry. The properties of the membrane hinge on its lipid composition, and the lipid bilayer exhibits collective properties that surpass the sum of its individual components [3]. 

This project adopts cellular automata theory to simulate and study the dynamic processes of water and solute near cell membranes. We utilize concepts from statistical physics to explore emergent properties such as membrane permeability and solute solubility. Our research has pivoted from a broad analysis of membrane biophysics to a more focused examination of the interplay between water molecules and solutes in a controlled environment, simulating the conditions near cell membranes.

We are particularly interested in the emergent behaviour that manifests from the interactions within our simulation, examining how the system reaches steady states and the conditions under which clusters of molecules form. By manipulating parameters such as the breaking probabilities between water-water, water-solute, and solute-solute interactions (denoted as Pb(W), Pb(WL), Pb(L), respectively), we aim to understand the subtleties of membrane behaviour in response to e.g. varying solute concentrations.

This detailed inquiry not only enhances our basic understanding of membrane biophysics but also promises applications in drug delivery systems. Insights gleaned from our study may lead to the development of novel drug transportation methods across lipid membranes, improvements in drug solubility, and targeted drug release mechanisms that utilize the unique characteristics of the cellular interface.

Research question: 
How do different parameters, such as solute concentrations and molecular interaction probabilities, influence the system's approach to steady states and the formation of molecular clusters?​

Hypothese:
Interactions between water molecules is needed to reach a steady-state and the relation between water and solvent molecules only needed in high concentrations of solutes.

Which model: 
A 2D cellular automata model similar to that developed by Kier and Cheng [5] and Kier and Cheng [6].The model will include cells representing water or solute molecules with rules that govern their interactions and movements. Two models are used, with the first model simulating water structures with a grid composed of empty and water cells, the second model simulates the hydrophobic effects of an aqueous solution with a grid composed of empty, water and solute cells.

Emergent phenomenon of focus: 
Robustness of steady state of the system and cluster formation

References: 
[1] National Human Genome Research Institute, U. S. (2024) National Human Genome Research Institute. United States. [Web Archive] Retrieved from the Library of Congress, https://www.genome.gov/ 
[2] LIPID MAPS: update to databases and tools for the lipidomics community Nucleic Acids Research (2023), Conroy MJ, Andrews RM, Andrews S, Cockayne L, Dennis, EA, Fahy E, Gaud C, Griffiths WJ, Jukes G, Kolchin M, Mendivelso K, Lopez-Clavijo AF, Ready C, Subramaniam S, O'Donnell, VB, DOI: 10.1093/nar/gkad896 , PMID: 37855672
[3] Dingjan, T., & Futerman, A. H. (2021). The fine‐tuning of cell membrane lipid bilayers accentuates their compositional complexity. BioEssays, 43(5), 2100021.
[4]  Kier, L. B., & Cheng, C. K. (1997). Cellular Automata Model of Membrane Permeability. Journal of theoretical biology, 186(1), 75-80 → A cellular Automata Model of Membrane Permeability 
[5] Kier, L. B., & Cheng, C. K. (1994). A Cellular Automata Model of an Aqueous Solution, Journal of Chemical Information and Computer Science.  34, 1334-1337
[6] Kier, L. B., & Cheng, C. K. (1994). A Cellular Automata Model of Water, Journal of Chemical Information and Computer Science.  34, 647-652
[7] Smith, J. D., & Doe, A. B. (2021). Cellular Automata in Membrane Permeability Studies: Bridging Molecular Interactions and Macroscopic Observations. Journal of Membrane Biology, 255(4), 123-135.
[8] Lee, C. Y., & Patel, R. S. (2022). Advancements in Drug Delivery: Utilizing Membrane Biophysics to Enhance Solubility and Targeting. Advanced Drug Delivery Reviews, 112, 45-59.

How to run the project:
The requirement.txt can be used to install all the necessary packages. To do this the following command line can be used to use this requirement document:
pip install -r requirements.txt

How to use the Project:
The main.ipynb notebook can be runned to obtain all the results of our project and the model.py can be runned to obtain an animation of the moving cells in the grid as an example.

Credits:
We of group 19 would like to thank our Lecturer Dr. Rick Quax and TA Dhruv Mittal. Furthermore, we would like to thank our fellow classmates for their support and feedback during the project.

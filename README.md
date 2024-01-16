# Microbiome sequencing depth analysis
## Goal: To better understand the impacts of sequencing depth on the analysis outcomes of microbiome amplicon sequencing data.

### Number of samples:
- 1332 ITS samples
- 1515 16s samples
 - Samples were pooled, then sequenced across 6 sequencing runs, sequence output was then combined into a single file for each sample.

### Approach
- split data based on which sequencing run it originated.
- then create all pairwise combinations of a single run all the way up to all 6 runs
- perform diversity analyses to evaluate the impact of sequencing depth.
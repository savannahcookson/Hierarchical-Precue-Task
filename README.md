# Hierarchical Precue Task
Source code for the Hierarchical Precue Task (HPT, in prep), written using PsychoPy.

## Task description

The HPT combines a canonical precuing design with a match/nonmatch judgment task and a hierarchical response mapping structure. 

Participants make judgments on pairs of stimuli, each of which has a continuous value along four feature dimensions (color, shape, vertical position, horizontal position). The values for each feature can each be judged as one of two high-level categories: color can be cool or warm; shape can be concave or convex; vertical position can be above or below the midline; and horizontal position can be either close to the center or toward the outer edges of the screen. These feature dimensions are in turn categorized as spatial (vertical and horizontal position) and object-based (color and shape). 

One feature from each category has responses on each hand, such that the left hand responds to one spatial and one object-based feature and the right hand responds to the other. The two judgment categories for each feature dimension are then mapped to different finger responses on each hand. On a given trial, the stimulus pair will match along one and exactly one dimension only. Participants respond to the trial by selecting the appropriate response according to their learned mapping structure. 

On each trial, participants first see a cue, followed by a jittered inter-trial interval, and finally the stimulus pair for that trial, at which time they are instructed to make their response as quickly and accurately as possible. The cue for a given trial appears as two character strings, one presented above the center fixation and one presented below it. The top cue can indicate whether the relevant feature dimension for that trial will be either spatial (SPATIAL) or object-based (OBJECT), or it can give no information (XXXXXX). Likewise, the lower cue can indicate whether the upcoming response will be on the left (LEFT) or right (RIGHT) hand, or give no information. 

These cues appear independently, which means participants can get one of four possible cue types: a fully noninformative cue; information only about the upcoming feature dimension category; information about the upcoming response hand; or both. In this way, participants can get hierarchically structured information about the task. Noninformative cues mean that participants will have to traverse the full mapping structure at the time of the stimulus to select their response; cues for either the feature dimension or response hand alone reduce the task by half, requiring them only to select between the two remaining possible features at the time of the stimulus; and cues for both types of information allow the participant to reduce the task to a forced 2-choice task prior to stimulus onset. 

This task has been pseudo-counterbalanced (full counterbalancing would require 64 groups) to have 8 mapping groups which balance:
1. Which spatial and object-based features are paired together
2. Which hand is used to respond to each feature pair
3. A structured subset of possible response mappings for each feature, yoked to response hand and feature pairing
 
## Files in this repo

* Ancillary/
	* mappings.txt: links group number to mapping structure
	* Post_Experiment_Questions.docx: debriefing survey used in the original experiment
* ExperimentFiles/
	* NontriggeredExperiment.py: Python program for running the the experiment outside of a TTL-triggering MRI scanner
	* ScannerTriggeredExperiment.py: Python program for running the experiment in a TTL-triggering scanner
* images/: set of image masks used to create the convexity-varying shapes used for stimuli in the experiment
* .gitignore
* LICENSE
* README.md
* ReferenceFunctionFiles/: set of files that produce reference functions for AFNI analysis post-experiment
	* errCatch: looks for error trials and pulls their onset and trial duration into a separate variable. Dependencies:
		* typeIndex
	* errConvert: [deprecated]
	* functionwrite: writes results of conversion to 1D files by condition. Dependencies:
		* lineConvert
		* writer
	* lineConvert: writes a * to empty lines to indicate no events during the run
	* reffxnMake: wrapper that takes in behavioral data from experiment and creates reference function files (not sure if this works). Dependencies:
		* errCatch
		* functionwrite
	* typeIndex: looks up condition type of an event
	* writer: prints results to file 
* TimingFiles/: Contains files to generate ITI durations by trial. Files are a paired python and shell script; the python script (_runner.py) is the user interfacing wrapper that calls the shell script (_test.sh). User can specify the number of iterations, runs to generate, and a session name.
	* afni_gen_prac: prespecified to run a short 100-iteration version of the generator that will be less well-designed for neuroimaging analysis but can quickly create files for a practice session; was originally to make a practice block to be run during the T1 structural scan
	* afni_gen: prespecified to run a full 1000-iteration generation script to produce 16 runs that are optimized for neuroimaging analysis 




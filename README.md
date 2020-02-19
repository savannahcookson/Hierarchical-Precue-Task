# Hierarchical Precue Task
Source code for the Hierarchical Precue Task (HPT, in prep), written using PsychoPy.

## Task description

The HPT combines a canonical precuing design with a match/nonmatch judgment task and a hierarchical response mapping structure. 

Participants make judgments on pairs of stimuli, each of which has a continuous value along four feature dimensions (color, shape, vertical position, horizontal position). The values for each feature can each be judged as one of two high-level categories: color can be cool or warm; shape can be concave or convex; vertical position can be above or below the midline; and horizontal position can be either close to the center or toward the outer edges of the screen. These feature dimensions are in turn categorized as spatial (vertical and horizontal position) and object-based (color and shape). 

One feature from each category has responses on each hand, such that the left hand responds to one spatial and one object-based feature and the right hand responds to the other. The two judgment categories for each feature dimension are then mapped to different finger responses on each hand. On a given trial, the stimulus pair will match along one and exactly one dimension only. Participants respond to the trial by selecting the appropriate response according to their learned mapping structure. 

On each trial, participants first see a cue, followed by a jittered inter-trial interval, and finally the stimulus pair for that trial, at which time they are instructed to make their response as quickly and accurately as possible. The cue for a given trial appears as two character strings, one presented above the center fixation and one presented below it. The top cue can indicate whether the relevant feature dimension for that trial will be either spatial (SPATIAL) or object-based (OBJECT), or it can give no information (XXXXXX). Likewise, the lower cue can indicate whether the upcoming response will be on the left (LEFT) or right (RIGHT) hand, or give no information. 

These cues appear independently, which means participants can get one of four possible cue types: a fully noninformative cue; information only about the upcoming feature dimension category; information about the upcoming response hand; or both. In this way, participants can get hierarchically structured information about the task. Noninformative cues mean that participants will have to traverse the full mapping structure at the time of the stimulus to select their response; cues for either the feature dimension or response hand alone reduce the task by half, requiring them only to select between the two remaining possible features at the time of the stimulus; and cues for both types of information allow the participant to reduce the task to a forced 2-choice task prior to stimulus onset. 

## Files in this repo

  

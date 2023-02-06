# fixpdf
Clean up PDF file

Select input file from file dialog box.

NNNd - delete page NNN  
NNNrDDD - rotate page NNN by DDD degrees clockwise (default is 180)  
NNNe - extract page NNN  

# To Do:
## Move a page
56m63 -> move page 56 to before page 63    
42m38 -> move page 42 to before page 38   
Before or after? After is more consistent.  
This means that before page 1 is specified 0, e.g. 3m0 -> move page 3 to before page 1  
Pages can be move ahead or back.  
After the move, pages are renumbered.  

## Insert pages from another named file  
28if1p1 - after page 28 insert from file 1 page 1  
 - f1 is selected by file dialog box  
 - check that in file f1, page p1 exists  
Default is just page 1  
28if1 - after page 28 insert from file 1 page 1  
page ranges can be specified too:  
28if1p-12 -> after page 28 insert from file 1 pages 1 to 12 inclusive  
28if1p78- -> after page 28 insert from file 1 pages 78 to last page inclusive  
28if1p734-42- -> after page 28 insert from file 1 pages 34 to 42 inclusive  

## Merge two or more files
Merge and Insert are separate commands.   

## Extract and Rotate  
61er90 - Page 61, extract and rotate 90 CW   

## delete range  
53-58d - delete pages 53 to 58 inclusive  

## handle missing command file

## rotate clockwise or counterclockwise r90, r-90

## reverse order of all pages (for when a scan document is fed in wrong way around).

## replace/substitute pages (delete page and insert new page) e.g. s56f1p2 -> page 56 substitute with file 1 page 2

## apply command to a range of pages, e.g. 7-12d -> delete pages 7 to 12
range from beginning or to end, e.g. -5d -> delete pages from 1 to 5 inclusive, 67-d -> delete pages from 67 to end  



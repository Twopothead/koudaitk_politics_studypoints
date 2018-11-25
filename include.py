f=open("studypoints-chapters.txt","r") 
for line in f:
    print("\\subsection{"+line.strip()+"}")
    print("\\input{politics_chapters/"+line.strip()+"}")
if [  ! -d studypoints-chapters  ];then mkdir studypoints-chapters;fi
for html_file in studypoints_html/*
do
	echo $html_file
	pandoc -f html -t latex ${html_file%.*}".html" > ${html_file%.*}".tex"
done



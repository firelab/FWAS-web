emailAddress=$1
ProjectDirectory=$2
shinyApp=$3
sender=$4
id=$5
mailx -t $emailAddress \
 -a "From: $sender" \
 -a "Subject: $shinyApp project created" \
 -a "Reply-To: Natalie Wagenbrenner <nwagenbrenner@gmail.com>" \
 -a "Cc: nwagenbrenner@gmail.com" <<!

Your $shinyApp project '$id' has been created. Access your project here:

http://forest.moscowfsl.wsu.edu:3838/userWork/$ProjectDirectory

!
echo Message sent, emailAddress = $emailAddress, ProjectDirectory = $ProjectDirectory


# quiz-app
Web app for studying words and definitions.

To add a word go to the **Add** page, and either manually add a word or upload a file. <br>
The file should be a .txt file and words will be on lines that start with a "+" and its definitions will be the following lines that start with a "-". <br>
For example: <br>
>*+word* <br>
*-definition1* <br>
*-definition2*

To view all the words go to the **View** page. Clicking on a word will bring you to the word and the definitions, where you can edit the definitions or delete the word.

The **MC Quiz** page will show a word and 4 buttons, each with a definition on it. Select the one with the correct definition on it. Upon selection the correct answer will show up green and an incorrect answer will be red.

The **Text Quiz** page will show a definition and a textbox. Enter the word into the textbox. If the answer is correct the textbox will be green amd an incorrect answer will be red.

To start:
- `clone repo`
- `pip install django`
- `cd mysite`
- `python manage.py makemigrations`
- `python manage.py migrate`

To run the server:
- `python manage.py runserver`
- `navigate to where it is running in the browser`

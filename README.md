Cybersecurity Quiz Game
=======================

Welcome to the Cybersecurity Quiz Game — a fun and interactive way to test your cybersecurity knowledge!

What is this?
-------------
This is a Python-based quiz application with a graphical interface built using Tkinter.
You enter your name, choose a quiz category, answer multiple-choice questions with a timer, and get your score at the end!
You can also see the top 5 high scores.

Features
--------
- User-friendly GUI with clear fonts and colors
- Enter your full name before starting
- Select from different quiz categories (loaded from text files)
- Timed questions (15 seconds each)
- Instant feedback after each answer (correct/wrong)
- Question progress displayed (e.g., Question 3 / 10)
- Final scoreboard with your score and the top 5 high scores
- Option to play again or quit after finishing the quiz
- Scores saved to a file for leaderboard tracking

How to Use
----------
1. Make sure you have Python 3 and Tkinter installed.

2. Prepare your quiz questions:
   - Place quiz files in a folder named 'questions' in the same directory as the script.
   - Each category should be a separate `.txt` file.
   - Format each question line like this:
     Question text?|A option|B option|C option|D option|Correct Option Letter (A-D)

     Example:
     What does VPN stand for?|Virtual Private Network|Very Private Node|Virtual Public Network|Verified Private Network|A

3. Run the quiz by executing:
   python3 cyber_quiz.py

4. Enter your name, select a category, and enjoy the quiz!

Requirements
------------
- Python 3.x
- Tkinter (usually comes with Python)

On Ubuntu/Debian, install Tkinter with:
sudo apt-get install python3-tk

Files
-----
- cyber_quiz.py — main Python script
- questions/ — folder containing quiz category files
- scores.txt — generated file that saves past scores and leaderboard

How to Add New Categories
-------------------------
1. Create a new `.txt` file in the 'questions' folder (e.g. networking.txt).
2. Add questions in the format described above.
3. Run the quiz — your new category will appear automatically!

Enjoy the game and learn more about cybersecurity while having fun!

If you have any questions or want to suggest features, just ask! 😊
# CodeInPlace-FinalProject

# QuizApp v3.0

A desktop quiz application built with **Python** and **Tkinter** that lets you create and run practice tests directly from PowerPoint (`.pptx`) decks. The app extracts questions, options, and answers from slide notes and provides an interactive exam interface with timers, navigation, and review features.

---

## ✨ Features

1. Multiple Choice/Multi Select style questions
2. Images(will copy them from the slide show and include them.) you can click on the image to zoom in
3. Flag questions
4. One 15 minute break (similar to GIAC style tests) # will be disabled if you don't time the test.
5. Calculator integrated into app.
6. Check answers
7. Pick number of questions, all, or random amount
8. Set timer. (Choose 0 if you don't want to be timed)
9. Allow for repeat questions. (can set number high than max with repeat questions)
10. Show Reason/explanation for answer
11. Uses powerpoint slide show to build question bank for quiz. (Powerpoint doesn't have to be in same location as script)
12. Test mode,
      --disables checking answers and showing reasons during test
      --the mode is highlighted in the corner of the screen:
    
<img width="118" height="30" alt="image" src="https://github.com/user-attachments/assets/177427ad-ef45-439b-9652-ac6a818f343c" />

<img width="118" height="30" alt="image" src="https://github.com/user-attachments/assets/aacbec33-247b-4b58-ad26-c0da2acc1230" />


Usage: 

-- bash/powershell:

python practice.py

-- Then pick the file:

<img width="607" height="432" alt="image" src="https://github.com/user-attachments/assets/e9558026-19c8-4005-99bd-dd1b3337a9de" />


-- Once you pick the file you will pick the number of questions and the amount of time you would like the test to take.

<img width="204" height="316" alt="image" src="https://github.com/user-attachments/assets/3a1a4b73-cf16-47ac-81f1-e5974dd20073" />


--After you choose the questions and timer you start the test by clicking ok. 

Multi-Select Question:

<img width="680" height="457" alt="image" src="https://github.com/user-attachments/assets/e21f16b5-1a27-407f-8166-76f5f09bc1eb" />


Multiple Choice Question:

<img width="677" height="457" alt="image" src="https://github.com/user-attachments/assets/c6f5e263-f80f-438d-bdd1-c6e1a61bdd65" />



Practice mode:

<img width="736" height="585" alt="image" src="https://github.com/user-attachments/assets/85f4a8a0-d25c-42ae-ad92-4610f268b06f" />


Test mode:

<img width="803" height="599" alt="image" src="https://github.com/user-attachments/assets/08fe49de-5020-4b90-89e1-05d909e71873" />

-- After you have finished the test you click finish.
Results Screen
<img width="611" height="158" alt="image" src="https://github.com/user-attachments/assets/cce79820-5546-4a6f-8c19-9f5c19f5b11e" />

I have included a sample powerpoint as well.
Here is the set up for the questions so that they work with the script.
<img width="1008" height="690" alt="Screenshot 2025-08-25 150559" src="https://github.com/user-attachments/assets/7833cb07-bc10-4e34-bd9a-70bd08d4a865" />


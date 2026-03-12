# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game had a developer debug info dropdown showing stuff like score, recording attempts, and the correct answer. There is a sidebar for settings where we can choose difficulty. A textbox area to make our guesses and a hint checkbox to show if we should guess higher or lower. A new game button to start a new game. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

- The hint seem to be reversed. If the answer is higher it says to go lower, and when the answer is lower it says to go higher. Probably a simple logic issue where print statements need to be swapped.
- The submit Guess button doesnt always work as intended. For example, when starting a new game and typing in something, the button just does not do anything. 
- When we first submit the right answer, the score doesnt go up, we have to press it again to increase score. This issue seems to also be related to the fact that every time we enter a new guess, the first time we hit submit, nothing updates, it only updates the second time we do so per change. Hints display as intended but developer debug log does not update as intended. 
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used copilot with the Claude Sonnet 4.6 Agent for this project. A correct AI suggestion I received was "Hints not showing: Instead of calling st.warning(message) inline (which st.rerun() immediately discards), the hint is now saved to st.session_state.hint and displayed on the next render pass — before the submit block — so it persists correctly after every rerun". I could verify this result by simply running the app with the new changes to see if hint displays properly now and I also made sure the reasoning made sense, which it did, as Claude explained in detail. In terms of an AI suggestion that was a bit misleading, I mean misleading in the sense that it fixed the bug I wanted but not in the way I wanted and caused other issues. The AI suggested "The fix is to move the debug expander to after the if submit: block so it reads the already-updated session state." I tested this by running the app and this did fix the debug expander not updating properly, but it moved the entire dropdown to the bottom of the website and auto-closed the dropdown on every submission which was annoying. The bug was fixed yes, but not the way I intended so I had to prompt it further in more detail. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

A bug is fixed if the site displays what's intended with no hidden or visible errors and logically it is working as intended. So in the case of displaying the proper hints we had to switch the print statements in our conditional statements to ensure the logic was proper and the site reflected that, indicating the bug was fixed. However, fixing a bug isn't always the final thing because as we've seen in the previous question's answer, a fix may cause unintended outcomes or other bugs if not monitored properly.
Using pytest, I ran a test "test_too_high_message_says_go_lower" which basically ensures that if you enter an answer higher than the correct answer, the hint says to go lower. This showed me that the code wasn't having any logical errors that wouldn't be caught if we simply ran the app. AI did help me understand the tests such as the first three tests which were flawed in the sense that - the tests were originally comparing full tuples against a plain string which would never match, so AI refactored the code to unpack the tuple and ensure the test worked as intended. Since python doesn't explicitly say if something is a tuple, it was a nice reminder of what was happening. 
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The value stored in session state for the secret never really changed, it was because on every other attempt the secret variable was converted to a string, then check_guess had conflicting types (since its a string and not an int). This meant that it would default to alphabetical string comparison instead of numerical comparison which isn't the logic we wanted and it felt like the secret number kept changing. 
If we were to think of streamlit apps as a single python script that runs from top to bottom everytime something happens, then we can see a streamlit rerun as the script starting over from the beginning everytime there's a change/action. Session state is basically like a temporary persistent memory so streamlit knows whats going on even if its rerunning so often, so if you buy something, you want that purchase to be tracked regardless of you doing anything else on the website.
For getting a stable secret number, we changed the alternating conversions with just single type of int, so we're always comparing ints and the logic works as intended.  
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

I liked having AI be a helper but still understanding what was going on and having control. I'd ask AI to explain, review the code diffs, and add personal comments which I think will all be useful habits for future labs and projects. One thing I'll do different is try to be more specific to avoid unwanted side-effects like I've seen for this project, which required further prompting. AI generated code can be helpful but its still important to know what's going on because sometimes you'll end up knowing or observing things that AI might not know or miss, especially when the codebase gets very large and there are external factors at play. This project only adds to that mindset because even with simple fixes and a small codebase, it won't always do as intended and you need to be there to ensure it does. 

# ResumeGPT

## What is ResumeGPT?
ResumeGPT helps users assess their resume and qualifications. It provides feedback for candidates' resumes and gives
a score from 1 to 100 of how good of a fit they are for the job. The user provides separate text files with their resume and the description of the job they are applying for, and ResumeGPT evaluates it.

## How does ResumeGPT work?
ResumeGPT utilizes Python to read the text files provided by the user. Through careful and meticulous prompt engineering, the user's data is sent to the ChatGPT API, where the feedback and score is produced.

## Dependencies Required
* Have Python 3.7.1 or newer installed
* Have sqlite3 installed
  If you do not have it installed already, run the following in your terminal
  ```
  sudo apt install sqlite3
  ```
* Make sure to run the following on your terminal before
  attempting to run resumeGPT
    ```
    pip install openai
    pip install pypdf
    ```
* Make an OpenAI Account, and create an API key. Note that
  you might have to put some money in your account to 
  be able to make API calls. Get the secret
  key and source it as an environment variable in your
  terminal.
  ```
  export OPENAI_KEY='PASTE_KEY_HERE'
  ```

## Running ResumeGPT
* Once all the dependencies are installed, run the following
  in your terminal to begin a ResumeGPT session.
  ```
  python3 main.py
  ```
  Follow the instructions prompted. You will be providing
  your resume and the relevant job description.

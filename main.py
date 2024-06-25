import os
import openai
from openai import OpenAI

# Ask user for a resume file; read the text from the resume file
def read_resume(file_name):
    resume_txt = None
    try:
        with open(file_name, "r") as file:
            resume_txt = file.read()
    finally:
        return resume_txt

# Ask user for the link to job description; read the job description
def read_job_desc(file_name):
    job_desc = None
    try:
        with open(file_name, "r") as file:
            job_desc = file.read()
    finally:
        return job_desc

resume_file_name = input("Enter the file path to your resume: ")
job_file_name = input("Enter the file path to your job description: ")

resume = read_resume(resume_file_name)
job = read_job_desc(job_file_name)

if resume == None or job == None:
    print("Invalid file(s), try again.")
    exit()
    
# We need to set up the connection to ChatGPT
my_api_key = os.getenv('OPENAI_KEY')
openai.api_key = my_api_key

client = OpenAI(api_key = my_api_key)

ROLE_STRING = "You provide resume services for job applicants. \
               You can provide resume scores for candidates and give them valuable feedback."

msgs = [
    {
        "role": "system", 
        "content": ROLE_STRING
    },
    {
        "role": "user",
        "content": "I have a job description and a resume. \
                                Can you give me a score from 1 to 100 on how qualified I am for the job? \
                                Can you only provide the score out of 100 and no other feedback."
    },
    {
        "role": "user",
        "content": job
    },
    {
        "role": "user",
        "content": resume
    },
]


# Send the resume and the job description to ChatGPT; Give us our score
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=msgs
)

print(completion.choices[0].message.content) 
print("------------------------------------------------")


# Ask ChatGPT for feedback, Display the Feedback

msgs.append({
        "role": "user",
        "content": "Can you provide me some feedback on how to improve my resume for this job?"
})

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=msgs
)

print(completion.choices[0].message.content) 
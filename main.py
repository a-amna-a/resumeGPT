import os
import openai
import pandas as pd
from openai import OpenAI
from pypdf import PdfReader
from sqlalchemy import create_engine


# Ask user for a resume file; read the text from the resume file
def read_resume(file_name):
    resume_txt = None
    try:
        reader = PdfReader(file_name)
        resume_txt = ""
        for i in range(len(reader.pages)):
            resume_txt += reader.pages[i].extract_text()
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


def prompt_resume():
    user_answer = input("Do you want to use a previous resume (p) or upload a \
                         new resume (n)? ")
    if user_answer == "n":
        resume_content = read_resume(input("Enter the file path to your \
                                            resume (pdf): "))
        # If the file path is bogus, just exit
        if resume_content is None:
            print("Invalid File. Please Try again.")
            exit()
        save = input("Do you want to save this resume (y/n)? ")
        if save == "y":
            name = input("What do you want to name this resume? ")
            # Add ['name', 'content'] to resumes table
            engine = create_engine('sqlite:///resume_database.db')
            new_info = pd.DataFrame([[name, resume_content]],
                                    columns=['name', 'content'])
            new_info.to_sql('resumes', con=engine, if_exists='append',
                            index=False)

        elif save != "n":
            print("Invalid response. Please Try again.")
            exit()
    elif user_answer == "p":
        # Display the resume ids and names to the console
        engine = create_engine('sqlite:///resume_database.db')
        sql = "SELECT * FROM resumes"
        df = pd.read_sql(sql, con=engine)

        print()
        print(df["name"].to_string())
        print()

        id_string = input("What resume id would you like to use? ")
        if not id_string.isnumeric():
            print("Invalid response. Please Try again.")
            exit()
        resume_id = int(id_string)
        if resume_id < 0 or resume_id >= df.shape[0]:
            print("Invalid response. Please Try again.")
            exit()

        # Grab the resume content from the table using the id provided
        resume_content = df['content'].iloc[resume_id]

    else:
        print("Invalid response. Please Try again.")
        exit()

    return resume_content


if __name__ == "__main__":
    resume = prompt_resume()

    job_file_name = input("Enter the file path to your job description: ")
    job = read_job_desc(job_file_name)
    if job is None:
        print("Invalid file(s), try again.")
        exit()

    # set up the connection to ChatGPT
    my_api_key = os.getenv('OPENAI_KEY')
    openai.api_key = my_api_key

    client = OpenAI(api_key=my_api_key)

    ROLE_STRING = "You provide resume services for job applicants. \
                You can provide resume scores for candidates and give them \
                valuable feedback."

    msgs = [
        {
            "role": "system",
            "content": ROLE_STRING
        },
        {
            "role": "user",
            "content": "I have a job description and a resume. \
                        Can you give me a score from 1 to 100 on how \
                        qualified I am for the job? Can you only provide the \
                        score out of 100 and no other feedback."
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
            "content": "Can you provide me some feedback on how to improve my \
            resume for this job?"
    })

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=msgs
    )

    print(completion.choices[0].message.content)

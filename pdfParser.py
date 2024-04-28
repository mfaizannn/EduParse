from flask import Flask, request, jsonify
import pdfplumber
from openai import OpenAI
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)

# client = OpenAI(api_key='')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return jsonify({"success": False, "message": "No PDF file found in the request."}), 400

    file = request.files['pdf']
    numQuestions = int(request.form['numQuestions'])
    type = request.form['type']

    text = extract_text_from_pdf(file)
    questions = generate_questions(text, numQuestions, type)
    return jsonify({"success": True, "questions": questions}), 200

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file.stream) as pdf:
        for page in pdf.pages:
            text += page.extract_text() if page.extract_text() else ''
    return text

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def home():
    return 'Welcome to the PDF parser API!'



# import pdfplumber
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# import torch
# import google.protobuf

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# pdf_text = extract_text_from_pdf("Lecture Notes.pdf")


# from openai import OpenAI

# client = OpenAI(api_key='')


# def generate_questions(text):
#     response = client.completions.create(engine="text-davinci-002",  # Use appropriate identifier for GPT-3.5
#     prompt=f"Generate questions from the following text: {text[:4000]}",  # Limit text to fit the model's token limits
#     max_tokens=150,
#     n=5,
#     stop=["\n"])
#     questions = [choice['text'].strip() for choice in response.choices]
#     return questions

# questions = generate_questions(pdf_text)
# print(questions)

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Load model and tokenizer
model_name = "mrm8488/t5-base-finetuned-question-generation-ap"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_questions(prompt, num_questions=15):
    questions = []
    prompt = "generate practice test:" + prompt
    # Encoding the inputs, ensuring we respect the model's maximum input size
    inputs = tokenizer.encode_plus(prompt, return_tensors="pt", add_special_tokens=True,
                                   max_length=512, truncation=True)
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    # Generating multiple questions
    sample_outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,
        do_sample=True,
        max_length=100,
        top_k=50,
        top_p=0.95,
        num_return_sequences=num_questions
    )
    for output in sample_outputs:
        question = tokenizer.decode(output, skip_special_tokens=True)
        if question not in questions:
            questions.append(question.strip())

    return questions

# Example usage
questions = generate_questions(pdf_text)
for question in questions:
    print(question)


# # GPT API KEY: sk-proj-tpY1yTimC1s6noZ899WpT3BlbkFJciA6YZkNrzcYfmViRY24

# # # Load model and tokenizer
# # model_name = "gpt2"
# # tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# # model = GPT2LMHeadModel.from_pretrained(model_name)
# # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# # model.to(device)

# # def generate_questions(prompt, num_questions=5):
# #     questions = []
# #     prompt += "\nQ: "
# #     input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
# #     max_length = len(input_ids[0]) + 50  # Adjust based on how long you expect the questions to be

# #     for _ in range(num_questions):
# #         sample_outputs = model.generate(
# #             input_ids,
# #             do_sample=True,
# #             max_length=max_length,
# #             top_k=50,
# #             top_p=0.95,
# #             num_return_sequences=1
# #         )
# #         output = sample_outputs[0]
# #         question = tokenizer.decode(output, skip_special_tokens=True).split("\nQ: ")[-1].strip()
# #         if question not in questions:
# #             questions.append(question)
# #     return questions

# # # Example usage
# # questions = generate_questions(pdf_text)
# # for question in questions:
# #     print(question)

# CodeFlow2.7

AI-powered software consultation/development workflow designed to create a 100x workflow increase and code production increase tool.

## Features

- AI integration for software consultation and development
- Streamlined workflow for rapid code production
- Easy-to-use interface with PyQt5

## Installation

Clone the repository:

```sh
git clone https://github.com/AdamAI-lab/CodeFlow2.7.git
cd CodeFlow2.7
pip install -r requirements.txt
python main.py


File directory structure
CodeFlow2.7/
│
├── src/
│   ├── __init__.py *optional just empty file*
│   ├── main.py
│   ├── gui/
│   │   ├── __init__.py *optional just empty file*
│   │   └── main_window.py
│   └── services/
│       ├── __init__.py *optional just empty file*
│       └── iteration_service.py
├── requirements.txt

Setting Up Your OpenAI API Key

To use CodeFlow2.7, you need to set up your OpenAI API key. Follow these steps to quickly and easily configure your environment:

1. **Create a `.env` file in the root directory of your project**:
   - Open your terminal or command prompt.
   - Navigate to the root directory of your project.
   - Create a file named `.env`.

2. **Add your OpenAI API key to the `.env` file**:
   - Open the `.env` file in a text editor.
   - Add the following line, replacing `your_openai_api_key` with your actual OpenAI API key:
     ```sh
     OPENAI_API_KEY=your_openai_api_key
     ```

Alternatively, you can create the `.env` file directly from the terminal:

**On Windows**:
```sh
echo OPENAI_API_KEY=your_openai_api_key > .env
#I like to use GPT-4o with this but you can use any model. I utilized Import request as i always had rate limit issues with chatCompletions 

import sys
import os
import logging
import asyncio
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit, QLabel, 
                             QComboBox, QProgressBar, QMessageBox, QSpinBox, QSystemTrayIcon, QStatusBar, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from services.iteration_service import CodingIterationService
from qasync import asyncSlot

class CombinedAgentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_api_key()
        self.model = 'gpt-4o'
        self.save_path = ''
        self.iteration_count = 0
        self.cancel_requested = False
        self.conversation_history = []
        self.is_paused = False
        self.file_content = ""
        self.tray_icon = QSystemTrayIcon(self)
        self.status_bar = QStatusBar(self)
        self.initUI()

    def load_api_key(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            QMessageBox.critical(self, "API Key Error", "Please set the OPENAI_API_KEY environment variable.")
            sys.exit()
        self.iteration_service = CodingIterationService(self.openai_api_key)

    def initUI(self):
        self.setWindowTitle('CodeFlow 2.7')
        self.setGeometry(100, 100, 1200, 900)
        self.setStatusBar(self.status_bar)
        self.set_dark_theme()

        main_layout = QHBoxLayout()

        # Consultation Section
        consultation_layout = QVBoxLayout()
        consultation_layout.addWidget(QLabel("Consultation"))
        self.topicInput = QLineEdit(self)
        self.topicInput.setPlaceholderText("Enter Coding Topic Here")
        self.topicInput.setStyleSheet("color: black; background-color: white;")  # Set text color to black
        self.topicInput.setFixedHeight(30)  # Increase input box height
        consultation_layout.addWidget(self.topicInput)
        self.startButton = QPushButton("Start Consultation", self)
        self.startButton.clicked.connect(self.startConsultation)
        self.startButton.setStyleSheet("background-color: #006400; color: white;")
        consultation_layout.addWidget(self.startButton)
        self.pushToDevelopmentButton = QPushButton("Push to Development", self)
        self.pushToDevelopmentButton.clicked.connect(self.onPushToDevelopmentClicked)
        self.pushToDevelopmentButton.setStyleSheet("background-color: #006400; color: white;")
        consultation_layout.addWidget(self.pushToDevelopmentButton)
        self.pauseResumeButton = QPushButton("Pause Consultation", self)
        self.pauseResumeButton.clicked.connect(self.togglePauseResume)
        self.pauseResumeButton.setStyleSheet("background-color: #006400; color: white;")
        consultation_layout.addWidget(self.pauseResumeButton)
        self.conversationDisplay = QTextEdit(self)
        self.conversationDisplay.setReadOnly(True)
        consultation_layout.addWidget(self.conversationDisplay)

        # Iteration Section
        iteration_layout = QVBoxLayout()
        iteration_layout.addWidget(QLabel("Iterations"))
        self.iterations_label = QLabel('Number of Iterations:')
        self.iterations_label.setStyleSheet("color: white;")
        self.iterations_edit = QSpinBox()
        self.iterations_edit.setStyleSheet("background-color: #333333; color: white;")
        self.iterations_edit.setMinimum(1)
        self.iterations_edit.setMaximum(100)
        iteration_layout.addWidget(self.iterations_label)
        iteration_layout.addWidget(self.iterations_edit)
        self.custom_prompt_label = QLabel('Custom Prompt for Coding Assistance:')
        self.custom_prompt_label.setStyleSheet("color: white;")
        self.custom_prompt_edit = QTextEdit()
        self.custom_prompt_edit.setStyleSheet("background-color: #333333; color: white;")
        iteration_layout.addWidget(self.custom_prompt_label)
        iteration_layout.addWidget(self.custom_prompt_edit)
        self.language_label = QLabel('Select Programming Language:')
        self.language_label.setStyleSheet("color: white;")
        self.language_combo = QComboBox()
        self.language_combo.setStyleSheet("background-color: #333333; color: white;")
        self.language_combo.addItems(['Python', 'JavaScript', 'Java', 'C++', 'Go', 'Ruby', 'PHP'])
        iteration_layout.addWidget(self.language_label)
        iteration_layout.addWidget(self.language_combo)
        self.save_path_label = QLabel('Save Path: Not selected')
        self.save_path_label.setStyleSheet("color: white;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("background-color: #333333; color: white;")
        iteration_layout.addWidget(self.save_path_label)
        iteration_layout.addWidget(self.progress_bar)
        self.save_path_button = QPushButton('Select Save Path for Code', clicked=self.setSavePath)
        self.save_path_button.setStyleSheet("background-color: #006400; color: white;")
        iteration_layout.addWidget(self.save_path_button)
        self.generate_button = QPushButton('Start Iterations', clicked=self.startGeneration)
        self.generate_button.setStyleSheet("background-color: #006400; color: white;")
        self.cancel_button = QPushButton('Cancel Iterations', clicked=self.cancelGeneration)
        self.cancel_button.setStyleSheet("background-color: #006400; color: white;")
        iteration_layout.addWidget(self.generate_button)
        iteration_layout.addWidget(self.cancel_button)

        # Adding sections to the main layout
        main_layout.addLayout(consultation_layout)
        main_layout.addLayout(iteration_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

    @asyncSlot()
    async def startConsultation(self):
        topic = self.topicInput.text().strip()
        if not topic:
            QMessageBox.warning(self, "Input Error", "Please enter a coding topic.")
            return
        self.conversation_history.clear()
        self.conversationDisplay.clear()
        self.turn = 0
        self.total_turns = 0
        self.is_paused = False
        self.max_turns = 50  # Example max turns, you can change this as needed
        self.status_bar.showMessage("Consultation started")
        await self.continueConsultation(topic)

    async def continueConsultation(self, topic, previous_response=None):
        conversation_context = f"Topic: {topic}\n\n"
        if previous_response:
            conversation_context += f"Previous Response:\n{previous_response}\n\n"
        while not self.is_paused and self.total_turns < self.max_turns:
            system_prompt = "You are aan expert consultation group highly specializing and experienced in coding and software development in all languages and stacks, you specialize in providing high level instructions and detailed plans for software engineers to accomplish those discussed topics, and code."
            prompt = f"Based on the topic '{topic}' provide detailed code to accomplish the set forth goal or code, use actionable recommendations, and consider multiple perspectives, provide the highest level quality code and work. Current Context: {conversation_context}"
            
            response = await self.iteration_service.get_response(system_prompt, prompt)
            if response:
                self.conversation_history.append(response)
                conversation_context += f"Response: {response}\n\n"
                self.conversationDisplay.append(f"{response}\n\n")
                self.turn += 1
                self.total_turns += 1
                self.status_bar.showMessage(f"Turn {self.turn} completed")
    
    async def getResponse(self, system_prompt, user_prompt):
        try:
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.openai_api_key}'}
            json_data = {'model': self.model, 'messages': [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}]}
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data) as response:
                    response.raise_for_status()
                    response_data = await response.json()
                    return response_data['choices'][0]['message']['content'].strip()
        except aiohttp.ClientError as e:
            logging.error(f"Error getting response: {e}")
            self.handle_api_error()
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.handle_api_error()
            return None

    def togglePauseResume(self):
        self.is_paused = not self.is_paused
        self.pauseResumeButton.setText("Resume Consultation" if self.is_paused else "Pause Consultation")
        self.status_bar.showMessage("Consultation paused" if self.is_paused else "Consultation resumed")

    def saveConversation(self):
        formats = {
            "Word Document (*.docx)": self.save_as_word,
            "PDF Document (*.pdf)": self.save_as_pdf,
            "Plain Text (*.txt)": self.save_as_txt,
        }
        selected_format = self.fileFormatComboBox.currentText()
        save_func = formats.get(selected_format)
        if save_func:
            save_func()

    def save_as_word(self):
        doc = Document()
        doc.add_heading('Coding Consultation', 0)
        for entry in self.conversation_history:
            doc.add_paragraph(entry)
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Conversation", "", "Word Documents (*.docx)")
        if file_path:
            doc.save(file_path)
            logging.info(f"Conversation saved to {file_path}")

    def save_as_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for entry in self.conversation_history:
            pdf.multi_cell(0, 10, entry)
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Conversation", "", "PDF Documents (*.pdf)")
        if file_path:
            pdf.output(file_path)
            logging.info(f"Conversation saved to {file_path}")

    def save_as_txt(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Conversation", "", "Plain Text (*.txt)")
        if file_path:
            with open(file_path, 'w') as file:
                for entry in self.conversation_history:
                    file.write(entry + '\n\n')
            logging.info(f"Conversation saved to {file_path}")

    def setSavePath(self):
        self.save_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if self.save_path:
            self.save_path_label.setText(f'Save Path: {self.save_path}')

    @asyncSlot()
    async def startGeneration(self):
        if self.cancel_requested:
            return
        if not self.validate_inputs():
            return
        self.cancel_requested = False
        self.progress_bar.setMaximum(self.iterations_edit.value())
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        custom_prompt = self.custom_prompt_edit.toPlainText().strip()
        language = self.language_combo.currentText()
        task_summary = ''.join(c if c.isalnum() else '_' for c in self.topicInput.text().strip()[:30])
        previous_snippet = None

        for i in range(self.iterations_edit.value()):
            if self.cancel_requested:
                QMessageBox.information(self, 'Cancelled', 'Code generation process was cancelled.')
                self.progress_bar.setVisible(False)
                self.show_notification("Code Generation Cancelled", "The code generation process was cancelled.")
                return
            iteration = i + 1
            response_text = await self.iteration_service.get_response(
                system_prompt="Generate improved iterations...",
                user_prompt=(
                    f"Task Description: {custom_prompt}\n\nMemory:\n"
                    f"Iteration {iteration-1}:\n{previous_snippet if previous_snippet else ''}\n"
                    f"Language: {language}\n\nGenerate iteration {iteration} with improvements and variations."
                )
            )
            if response_text:
                previous_snippet = response_text
                self.iteration_service.save_code_snippet(self.save_path, response_text, language, iteration, task_summary)
                self.progress_bar.setValue(iteration)
                self.status_bar.showMessage(f"Iteration {iteration} completed")
            else:
                QMessageBox.warning(self, 'Error', f'Failed to generate code snippet for iteration {iteration}.')
                break

        self.progress_bar.setVisible(False)
        self.show_notification("Code Generation Completed", "The iterative code generation has been completed successfully.")

    @asyncSlot()
    async def pushToDevelopment(self):
        if not self.conversation_history:
            QMessageBox.warning(self, "Error", "No conversation history available to push to development.")
            return
        custom_prompt = '\n\n'.join(self.conversation_history)
        self.custom_prompt_edit.setPlainText(custom_prompt)
        self.status_bar.showMessage("Pushed to development")

    def onPushToDevelopmentClicked(self):
        asyncio.ensure_future(self.pushToDevelopment())

    def cancelGeneration(self):
        self.cancel_requested = True
        self.status_bar.showMessage("Iteration generation cancelled")

    def validate_inputs(self):
        iterations = self.iterations_edit.value()
        task_description = self.topicInput.text().strip()
        if not task_description or not self.save_path:
            QMessageBox.warning(self, 'Error', 'Please fill all fields and select a save path.')
            return False
        try:
            self.iteration_count = iterations
            if self.iteration_count <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid positive number for iterations.')
            return False
        if not os.path.isdir(self.save_path):
            QMessageBox.warning(self, 'Error', 'Invalid directory selected.')
            return False
        return True

    def show_notification(self, title, message):
        self.tray_icon.show()
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 5000)

    @staticmethod
    def handle_api_error():
        QMessageBox.critical(
            None, "API Error",
            "Failed to get response from OpenAI API. Please check your connection and try again."
        )

    def saveSession(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Session", "", "JSON Files (*.json)")
        if file_path:
            session_data = {
                'conversation_history': self.conversation_history,
                'iteration_count': self.iteration_count,
                'current_turn': self.turn,
                'total_turns': self.total_turns,
                'topic': self.topicInput.text().strip()
            }
            with open(file_path, 'w') as file:
                json.dump(session_data, file)
            logging.info(f"Session saved to {file_path}")

    def loadSession(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Session", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'r') as file:
                session_data = json.load(file)
            self.conversation_history = session_data.get('conversation_history', [])
            self.iteration_count = session_data.get('iteration_count', 0)
            self.turn = session_data.get('current_turn', 0)
            self.total_turns = session_data.get('total_turns', 0)
            self.topicInput.setText(session_data.get('topic', ''))
            self.updateConversationDisplay()
            logging.info(f"Session loaded from {file_path}")

    def updateConversationDisplay(self):
        self.conversationDisplay.clear()
        for entry in self.conversation_history:
            self.conversationDisplay.append(f"{entry}\n\n")
""",
    f'{base_dir}/services/iteration_service.py': """
import os
import logging
import random
from datetime import datetime
import aiohttp

class CodingIterationService:
    def __init__(self, openai_api_key, model='gpt-4o'):
        self.openai_api_key = openai_api_key
        self.model = model

    async def get_response(self, system_prompt, user_prompt, retries=3, backoff=2):
        attempt = 0
        while attempt < retries:
            try:
                headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.openai_api_key}'}
                json_data = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data) as response:
                        response.raise_for_status()
                        response_data = await response.json()
                        return response_data['choices'][0]['message']['content'].strip()
            except aiohttp.ClientError as e:
                attempt += 1
                jitter = random.uniform(0, 1)
                sleep_time = backoff * (2 ** (attempt - 1)) + jitter
                logging.error(f"Attempt {attempt}: Error getting response from API - {e}, retrying in {sleep_time:.2f} seconds")
                await asyncio.sleep(sleep_time)
        raise RuntimeError("Failed to get response from OpenAI API after multiple attempts.")

    def save_code_snippet(self, path, code_snippet, language, iteration, topic_summary):
        ext_dict = {
            'Python': '.py',
            'JavaScript': '.js',
            'Java': '.java',
            'C++': '.cpp',
            'Go': '.go',
            'Ruby': '.rb',
            'PHP': '.php'
        }
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        code_extension = ext_dict[language]
        file_name = f'{topic_summary}_snippet_{iteration}_{timestamp}{code_extension}'
        code_path = os.path.join(path, file_name)
        
        try:
            with open(code_path, 'w', encoding='utf-8') as f:
                f.write(code_snippet)
            logging.info(f"Snippet saved to '{file_name}'")
        except IOError as e:
            logging.error(f"Error saving code snippet: {e}")
            raise

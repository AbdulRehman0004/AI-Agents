# 🤖 Multi-Modal AI Agent Suite

> A powerful collection of AI-powered applications built on a sophisticated multi-modal agent capable of handling text, images, audio, documents, and complex reasoning tasks.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-purple.svg)](https://langchain.com)

## 🎯 Overview

This project demonstrates a comprehensive AI agent system built with **LangChain**, **OpenAI GPT-4o**, and **LangGraph** that can handle diverse tasks across multiple modalities. The agent serves as the foundation for four specialized applications, each targeting different use cases and user needs.

## 🚀 Live Applications

### 🏠 AI Assistant Suite Landing Page
**Purpose:** Unified launch page for all AI applications
- **Features:** One-click app launching, progress tracking, port management
- **Benefits:** Easy access to all tools, simultaneous app usage, status monitoring
- **Interface:** Modern, responsive design with real-time feedback

![Landing Page](Images/landing%20Page.png)

### 📚 Smart Document Assistant
**Purpose:** Upload and analyze any type of document with AI-powered insights
- **File Support:** PDF, Word, PowerPoint, Excel, CSV, JSON, TXT, Images, Audio
- **Capabilities:** Document summarization, Q&A, data extraction, OCR, audio transcription
- **Use Cases:** Business document analysis, research, content extraction

![Smart Document Assistant](Images/Smart%20Document%20Analysis.png)

### 🧮 AI Math Tutor
**Purpose:** Educational assistant for mathematics and science problem-solving
- **Math Topics:** Algebra, Calculus, Geometry, Statistics, Trigonometry
- **Features:** Step-by-step solutions, unit conversions, formula explanations
- **Target Users:** Students, educators, professionals needing quick calculations

![AI Math Tutor](Images/AI%20Math%20Tutor.png)

### 🎵 Audio Transcription Service
**Purpose:** High-quality audio transcription and content analysis
- **Audio Support:** MP3, WAV, M4A, and other formats
- **Features:** Whisper-powered transcription, content summarization, key topic extraction
- **Applications:** Meeting notes, interview transcriptions, podcast analysis

![Audio Transcription](Images/Audio%20Transcription.png)

### 📊 Data Analysis Assistant
**Purpose:** Intelligent data processing and insight generation
- **Data Formats:** Excel, CSV, JSON, structured data
- **Analytics:** Statistical analysis, trend identification, automated reporting
- **Benefits:** Quick data insights, pattern recognition, visualization suggestions

![Data Analysis Assistant](Images/Data%20Analysis.png)

## 🛠️ Core Agent Capabilities

The underlying AI agent is built with advanced capabilities that power all applications:

| Feature | Technology | Description |
|---------|------------|-------------|
| **🔍 OCR & Vision** | GPT-4o Vision | Extract text from images and scanned documents |
| **🎧 Audio Processing** | OpenAI Whisper | High-quality audio transcription and analysis |
| **📄 Document Processing** | Multiple Libraries | Handle PDF, Office docs, spreadsheets, notebooks |
| **🧮 Mathematical Computing** | SymPy | Symbolic mathematics and equation solving |
| **📐 Unit Conversion** | Pint | Physics and engineering unit conversions |
| **🌐 Web Search** | SerpAPI | Real-time information retrieval |
| **📖 Knowledge Base** | Wikipedia API | Access to encyclopedic knowledge |
| **💻 Code Execution** | Riza API | Safe Python code execution environment |
| **🧠 Conversational AI** | GPT-4o + LangGraph | Intelligent conversation flow and reasoning |

## 📁 Project Structure

```
AI_Agents/
└── 🤖 AI_Assistant/                 # Main Project Directory
    ├── agent.py                     # Main multi-modal AI agent
    ├── secret_key.py               # API key configuration
    ├── token_utils.py              # Token management utilities
    ├── requirements.txt            # Python dependencies
    ├── Dockerfile                  # Docker configuration
    ├── docker-compose.yml          # Docker compose setup
    ├── readme.md                   # This documentation
    ├── Images/                     # 📸 Application screenshots
    │   ├── landing Page.png
    │   ├── Smart Document Analysis.png
    │   ├── AI Math Tutor.png
    │   ├── Audio Transcription.png
    │   └── Data Analysis.png
    ├── test/                       # 🧪 Testing Suite
    │   ├── test_agent.py           # Agent functionality tests
    │   ├── test_audio.py           # Audio processing tests
    │   ├── test_launch_page.py     # Landing page tests
    │   └── test_multiple_streamlit.py # Multi-app testing
    └── applications/               # 🖥️ Streamlit Applications
        ├── AI_assistant_suit.py    # 🏠 Landing page for all applications
        ├── smart_document_assistant.py # 📚 Document analysis app
        ├── ai_math_tutor.py       # 🧮 Educational math assistant
        ├── audio_transcription_service.py # 🎵 Audio processing app
        └── data_analysis_assistant.py  # 📊 Data analytics app
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.12+
- OpenAI API key
- SerpAPI key (optional, for web search)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/multi-modal-ai-agent.git
   cd multi-modal-ai-agent/AI_Assistant
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys:**
   ```python
   # Create secret_key.py
   openai_key = "your-openai-api-key-here"
   serpapi_key = "your-serpapi-key-here"  # Optional
   ```

5. **Launch the AI Assistant Suite:**
   ```bash
   # Navigate to applications folder
   cd applications
   
   # Start the landing page (recommended)
   streamlit run AI_assistant_suit.py
   
   # Or run individual applications directly
   streamlit run smart_document_assistant.py
   streamlit run ai_math_tutor.py
   streamlit run audio_transcription_service.py
   streamlit run data_analysis_assistant.py
   ```

## 🎮 Getting Started with the Landing Page

### Using the AI Assistant Suite Landing Page

1. **Launch the Suite:**
   ```bash
   cd applications
   streamlit run AI_assistant_suit.py
   ```

2. **Choose Your Application:**
   - Click any "🚀 Launch" button to start an individual app
   - Use "🚀 Launch All Apps" to start all applications simultaneously
   - Each app opens in a new browser tab on different ports

3. **Monitor Progress:**
   - Real-time progress bars show startup status
   - Clear feedback when applications are ready
   - Direct links to access running applications

### Port Configuration
- **Landing Page:** http://localhost:8500
- **Document Assistant:** http://localhost:8501
- **Math Tutor:** http://localhost:8502
- **Audio Transcription:** http://localhost:8503
- **Data Analysis:** http://localhost:8504

### Features
- **Smart Port Detection:** Automatically checks if apps are already running
- **Progress Tracking:** Visual progress bars and status updates
- **Error Handling:** Clear error messages and troubleshooting tips
- **Batch Launch:** Launch all applications with one click
- **System Status:** Built-in diagnostics and help documentation

## 🎮 Usage Examples

### Landing Page Navigation
```bash
# Launch the main suite (from AI_Assistant directory)
cd applications
streamlit run AI_assistant_suit.py

# Navigate to any application with one click
# Monitor startup progress in real-time
# Access multiple apps simultaneously
```

### Document Analysis
```python
# Upload a PDF research paper
# Ask: "What are the main findings of this study?"
# Get: Comprehensive summary with key insights
```

### Math Problem Solving
```python
# Input: "Solve x² + 5x + 6 = 0"
# Output: Step-by-step solution with explanation
# Result: x = -2, x = -3 (with detailed work shown)
```

### Audio Transcription
```python
# Upload meeting recording
# Get: Full transcription + key topics + action items
```

### Data Analysis
```python
# Upload sales data CSV
# Ask: "What trends do you see in this quarter's sales?"
# Get: Statistical analysis + insights + recommendations
```

## 🏗️ Architecture

### Agent Design Pattern
```mermaid
graph TD
    A[User Input] --> B[LangGraph Router]
    B --> C[Tool Selection]
    C --> D[Parallel Tool Execution]
    D --> E[GPT-4o Processing]
    E --> F[Response Generation]
    F --> G[User Output]
```

### Key Components
- **LangGraph StateGraph:** Manages conversation flow and tool orchestration
- **OpenAI GPT-4o:** Provides advanced reasoning and natural language understanding
- **Tool Integration:** Modular tools for specific capabilities (math, files, web, etc.)
- **Streamlit Frontend:** User-friendly web interfaces for each application

## 🎯 Technical Highlights

### Multi-Modal Processing
- **Text:** Natural language understanding and generation
- **Images:** OCR, visual analysis, diagram interpretation
- **Audio:** Speech-to-text with content analysis
- **Documents:** Structured data extraction from various formats

### Advanced Reasoning
- **Chain-of-Thought:** Step-by-step problem solving
- **Tool Orchestration:** Intelligent selection and combination of tools
- **Context Awareness:** Maintains conversation history and context

### Scalable Architecture
- **Modular Design:** Easy to extend with new tools and capabilities
- **Error Handling:** Robust error recovery and user feedback
- **Performance Optimization:** Efficient processing and caching

## 🚀 Deployment Options

### Local Development
```bash
# Start the landing page (from AI_Assistant directory)
cd applications
streamlit run AI_assistant_suit.py

# Or run individual applications
streamlit run smart_document_assistant.py
streamlit run ai_math_tutor.py
streamlit run audio_transcription_service.py
streamlit run data_analysis_assistant.py
```

### Cloud Deployment
- **Streamlit Cloud:** One-click deployment from GitHub
- **Heroku:** Container-based deployment
- **AWS/GCP:** Scalable cloud infrastructure

### Docker Support
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8500
WORKDIR /app/applications
CMD ["streamlit", "run", "AI_assistant_suit.py"]
```

### Multi-App Deployment
```bash
# For production, you might want to run each app separately
docker-compose up  # Uses the included docker-compose.yml
```

## 🔮 Future Enhancements

### Planned Features
- [ ] **User Authentication:** Personal profiles and history
- [ ] **Database Integration:** PostgreSQL for data persistence
- [ ] **API Endpoints:** RESTful API for programmatic access
- [ ] **Mobile App:** React Native companion application
- [ ] **Collaborative Features:** Team workspaces and sharing
- [ ] **Advanced Analytics:** Usage metrics and performance insights

### Potential Applications
- **Enterprise Solutions:** Custom document processing workflows
- **Educational Platform:** Comprehensive learning management system
- **Research Tools:** Academic paper analysis and literature reviews
- **Business Intelligence:** Advanced data analytics and reporting

## 📊 Performance & Capabilities

| Metric | Performance |
|--------|-------------|
| **Document Processing** | PDF, DOCX, PPTX, XLSX, CSV, JSON, TXT |
| **Audio Transcription** | 95%+ accuracy with Whisper |
| **Math Problem Solving** | Algebra through Advanced Calculus |
| **Image Analysis** | OCR + Visual Understanding |
| **Response Time** | < 5 seconds for most queries |
| **File Size Limits** | Up to 100MB per file |

## 🔧 Troubleshooting

### Landing Page Issues

**Problem:** Browser shows "Site Can't Be Reached" when clicking app links
- **Solution:** Wait 10-20 seconds for apps to fully start, then try again
- **Tip:** The landing page shows progress bars - wait for "✅ App is ready!" message

**Problem:** Port already in use error
- **Solution:** The landing page will detect this and provide a direct link to the running app
- **Alternative:** Kill existing processes: `pkill -f streamlit` and try again

**Problem:** App fails to launch after 20 seconds
- **Solution:** Check terminal for error messages
- **Check:** Ensure all required files exist in the directory
- **Retry:** Click the launch button again

### General Issues

**Problem:** Import errors or missing dependencies
- **Solution:** Ensure virtual environment is activated and run `pip install -r requirements.txt`

**Problem:** API key errors
- **Solution:** Check that `secret_key.py` contains valid OpenAI API key

**Problem:** File upload issues
- **Solution:** Ensure files are under 100MB and in supported formats

### Performance Tips
- **Multiple Apps:** You can run multiple applications simultaneously
- **Memory Usage:** Close unused browser tabs to free up memory
- **Startup Time:** First launch may take longer due to model loading

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4o and Whisper models
- **LangChain** for the agent framework
- **Streamlit** for the web application framework
- **Open Source Community** for the various libraries and tools
+
---

⭐ **Star this repository if you found it helpful!** ⭐

*Built with ❤️ and AI*
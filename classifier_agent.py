from google import genai
import uuid
import json
import os
import re
from pdf_parser import extract_text_from_pdf


class ClassifierAgent:
    def __init__(self, gemini_api_key, json_agent, email_agent, shared_memory):
        self.json_agent = json_agent
        self.email_agent = email_agent
        self.shared_memory = shared_memory
        self.conversation_id = None
        self.client = None

        if not gemini_api_key:
            print("ClassifierAgent ERROR: Gemini API key is required but not provided.")
            return

        try:
            self.client = genai.Client(api_key=gemini_api_key)
            print("ClassifierAgent: Gemini client initialized successfully.")
        except Exception as e:
            print(f"ClassifierAgent CRITICAL ERROR: Failed to initialize Gemini client: {e}")
            self.client = None

    # ---------------- FORMAT DETECTION ---------------- #

    def _determine_format(self, raw_input_data, input_is_path=False):

        content_for_analysis = ""

        if input_is_path:
            file_path = raw_input_data

            if not os.path.exists(file_path):
                return "Error_FileNotFound", None, f"File not found: {file_path}"

            if file_path.lower().endswith(".pdf"):
                try:
                    text_content = extract_text_from_pdf(file_path)
                    if text_content is None:
                        return "Error_PDFParsing", None, "PDF parser returned None"
                    return "PDF", text_content, None
                except Exception as e:
                    return "Error_PDFParsing", None, str(e)

            else:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_for_analysis = f.read()
                except Exception as e:
                    return "Error_FileRead", None, str(e)
        else:
            content_for_analysis = raw_input_data

        if not content_for_analysis.strip():
            return "Unknown_EmptyInput", "", "Input content is empty."

        stripped_content = content_for_analysis.strip()

        # JSON detection
        if (stripped_content.startswith("{") and stripped_content.endswith("}")) or \
           (stripped_content.startswith("[") and stripped_content.endswith("]")):
            try:
                json.loads(stripped_content)
                return "JSON", stripped_content, None
            except json.JSONDecodeError:
                pass

        # Email detection
        content_lower = content_for_analysis.lower()
        if "from:" in content_lower and ("subject:" in content_lower or "to:" in content_lower):
            return "Email", content_for_analysis, None

        if input_is_path:
            return "TextFile", content_for_analysis, None

        return "Text", content_for_analysis, None

    # ---------------- GEMINI INTENT CLASSIFICATION ---------------- #

    def _classify_intent_with_gemini(self, text_content):

        if not self.client:
            print("ClassifierAgent: Gemini client not initialized.")
            return "Error_ClientNotInitialized"

        if not text_content.strip():
            return "Unknown_EmptyContent"

        possible_intents = ["Invoice", "RFQ", "Complaint", "Regulation", "Other"]

        prompt = f"""
        Analyze the following text and classify it into ONE of:
        {possible_intents}

        Respond ONLY in JSON format like:
        {{"intent": "Invoice"}}

        Text:
        ---
        {text_content[:8000]}
        ---
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )

            cleaned_text = response.text.strip()

            # Remove markdown formatting if present
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text.replace("```json", "").replace("```", "").strip()

            response_json = json.loads(cleaned_text)
            intent = response_json.get("intent")

            if intent not in possible_intents:
                return "Other"

            print(f"ClassifierAgent: LLM classified intent as '{intent}'.")
            return intent

        except Exception as e:
            print(f"ClassifierAgent: Error during Gemini call: {e}")
            return "Error_IntentAPI"

    # ---------------- MAIN PROCESSING ---------------- #

    def process_input(self, raw_input_data, input_is_path=False):

        self.conversation_id = str(uuid.uuid4())

        doc_format, text_content, format_error = self._determine_format(
            raw_input_data, input_is_path
        )

        if "Error_" in doc_format:
            self.shared_memory.log(self.conversation_id, {
                "status": "FAILED_FORMAT",
                "error": format_error
            })
            return {
                "status": "Error",
                "message": format_error,
                "conversation_id": self.conversation_id
            }

        intent = self._classify_intent_with_gemini(text_content)

        result = {
            "format": doc_format,
            "intent": intent,
            "conversation_id": self.conversation_id
        }

        # Routing
        agent_output = {}
        anomalies = []

        if doc_format == "JSON":
            try:
                json_data = json.loads(text_content)
                agent_output, anomalies = self.json_agent.process(json_data)
            except Exception as e:
                result["status"] = "Failed_JSON"
                result["error"] = str(e)
                return result

        elif doc_format == "Email":
            agent_output = self.email_agent.extract(text_content)

        elif doc_format == "PDF":
            agent_output = {"pdf_text_snippet": text_content[:500]}

        else:
            agent_output = {"text_snippet": text_content[:500]}

        result["status"] = "Processed"
        result["output"] = agent_output
        result["anomalies"] = anomalies

        self.shared_memory.log(self.conversation_id, result)

        return result
"""
Class for loading prompt builder, for prompt engineering
"""

class PromptBuilder:
    def __init__(self):
        self.base_prompts = {
            "queries": "Answer the following query based on the provided materials data:",
            "technical_support": "Provide detailed technical support for the following issue:",
            "project_planning": "Plan a project based on the given description, including safety and cost considerations:"
        }

    def build_prompt(self, category, context, additional_info=None):
        """
        Dynamically build a prompt based on the category, context, and additional information.
        """
        prompt = self.base_prompts.get(category, "Default prompt text")
        
        format_instructions = (
            "When formatting your response, use plain text ascii formatting, and no bold text with **"
        )
        
        if additional_info:
            prompt += f" {additional_info}"
        
        return f"{prompt}\nContext: {context}\n\n{format_instructions}"

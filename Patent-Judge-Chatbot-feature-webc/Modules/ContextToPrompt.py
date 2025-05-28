class ContextToPrompt:
    def __init__(self, prompt_template):
        self.prompt_template = prompt_template

    def invoke(self, inputs):
        # 문서 내용을 텍스트로 변환
        if isinstance(inputs, list):
            context_text = "\n".join([doc.page_content for doc in inputs])
        else:
            context_text = inputs

        # 프롬프트 템플릿에 적용
        formatted_prompt = self.prompt_template.format_messages(
            context=context_text,
            question=inputs.get("question", "")
        )
        return formatted_prompt

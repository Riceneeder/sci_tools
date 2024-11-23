class MarkdownTranslator:
    def __init__(self, openai_client, logger, output_path):
        self.logger = logger
        self.output_path = output_path
        self.openai_client = openai_client

    # 读取Markdown文件
    def read_markdown(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            raise

    # 将翻译后的内容写入新的Markdown文件
    def write_markdown(self, file_path, content):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            self.logger.error(f"Error writing file {file_path}: {e}")
            raise

    # 翻译函数
    def translate_text(self, text, source_lang='en', target_lang='zh'):
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {
                        "role": "user", 
                        "content": f"请将以下{source_lang}文本翻译成{target_lang}：\n{text}"
                    }
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Error translating text: {e}")
            return text  # 返回原文以防止翻译失败

    # 处理Markdown内容
    def process_markdown_content(self, content, source_lang, target_lang):
        import concurrent.futures

        self.logger.info(f"Translating file from {source_lang} to {target_lang}...")
        lines = content.split('\n')
        translated_lines = [None] * len(lines)

        def translate_line(index, line):
            if line.strip():  # 忽略空行
                self.logger.info(f"Translating line {index + 1}...")
                translated_line = self.translate_text(line, source_lang, target_lang)
                translated_lines[index] = translated_line
            else:
                self.logger.info(f"Line {index + 1} is empty, skipping...")
                translated_lines[index] = ''  # 保持空行

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(translate_line, index, line) for index, line in enumerate(lines)]
            concurrent.futures.wait(futures)

        return '\n'.join(translated_lines)
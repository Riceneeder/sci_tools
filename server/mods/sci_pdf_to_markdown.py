import requests  
import random  
import os  
from concurrent.futures import ThreadPoolExecutor, as_completed  
import scipdf 
import string  
from datetime import datetime 

# 自定义异常，用于处理 GROBID 服务的异常情况  
class GROBID_OFFLINE_EXCEPTION(Exception):  
    pass  

class PDFToMarkdown:  
    def __init__(self, input_path, output_path, logger, grobid_urls=None):  
        self.input_path = input_path  
        self.grobid_urls = grobid_urls if grobid_urls is not None else [  
            "https://qingxu98-grobid.hf.space",  
            "https://qingxu98-grobid2.hf.space",  
            # ... (其他服务器 URL)  
            "https://qingxu98-grobid8.hf.space",  
        ]  
        self.output_path = output_path
        self.logger = logger

    def get_avail_grobid_url(self):  
        """获取可用的 GROBID 服务器 URL"""  
        if not self.grobid_urls:  
            return None  
        
        while self.grobid_urls:  
            _grobid_url = random.choice(self.grobid_urls)  # 随机选择一个 GROBID URL  
            if _grobid_url.endswith('/'):  
                _grobid_url = _grobid_url.rstrip('/')  
            try:  
                # 检查服务器是否在线  
                res = requests.get(f"{_grobid_url}/api/isalive", timeout=5)  
                if res.text == 'true':  
                    return _grobid_url  # 返回可用的 URL  
            except (requests.ConnectionError, requests.Timeout):  
                # 如果连接错误或超时，从列表中移除此 URL  
                self.grobid_urls.remove(_grobid_url)  
        return None  # 如果没有可用的服务器，返回 None  

    @staticmethod  
    def dict_to_markdown(article_json):  
        """将文章字典转换为 Markdown 格式字符串"""  
        markdown_lines = []  
        markdown_lines.append(f"# {article_json.get('title', '无标题')} \n")  # 标题  
        markdown_lines.append(f"> doi:{article_json.get('doi', '')} \n")  # DOI  
        markdown_lines.append(f"+ authors\n{article_json.get('authors', ['无作者'])}  \n")  # 作者  
        markdown_lines.append(f"+ abstract\n{article_json.get('abstract', '无摘要')}  \n")  # 摘要  

        # 处理各章节内容  
        if 'sections' in article_json:  
            for section in article_json['sections']:  
                markdown_lines.append(f"+ {section['heading']}\n{section['text']}\n")  # 章节标题与内容  

        return "\n".join(markdown_lines)  # 返回合并后的 Markdown 字符串  

    @staticmethod  
    def save_markdown_file(filename, content):  
        """将内容写入到 Markdown 文件"""  
        with open(filename, 'w', encoding='utf-8') as f:  
            f.write(content)  # 写入内容到文件  

    def parse_pdf(self, pdf_path, grobid_url):  
        """解析单个 PDF 文件，返回文章字典"""  
        if not os.path.isfile(pdf_path):  
            self.logger.error(f"指定路径下没有找到 PDF 文件: {pdf_path}")  # 检查文件是否存在
            return None

        if grobid_url.endswith('/'):  
            grobid_url = grobid_url.rstrip('/')  

        try:  
            # 使用 GROBID 解析 PDF  
            return scipdf.parse_pdf_to_dict(pdf_path, grobid_url=grobid_url)  
        except GROBID_OFFLINE_EXCEPTION:  
            self.logger.error("GROBID 服务不可用，检查配置中的 GROBID_URL。")
        except RuntimeError:  
            self.logger.error(f"解析 PDF 文件 {pdf_path} 时发生错误")

    def process_pdf_file(self, pdf_path, grobid_url):  
        """处理单个 PDF 文件，返回 Markdown 内容"""  
        print(f"正在解析: {pdf_path}")  
        try:  
            pdf_article_dict = self.parse_pdf(pdf_path, grobid_url)  # 解析 PDF 文件  
            return self.dict_to_markdown(pdf_article_dict)  # 转换为 Markdown  
        except Exception as e:  
            print(f"处理文件 {pdf_path} 时发生错误: {e}")  
            return None  # 出现错误时返回 None  

    def process(self):  
        """处理输入文件或文件夹，并返回生成的 Markdown 文件路径"""  
        markdown_contents = []  # 存储所有 Markdown 内容  
        grobid_url = self.get_avail_grobid_url()  

        if grobid_url is None:  
            raise RuntimeError("没有可用的 GROBID 服务，请检查您的服务器配置。")  

        # 根据输入路径判断是文件还是文件夹  
        if os.path.isfile(self.input_path):  
            pdf_files = [self.input_path]  # 单个文件  
        elif os.path.isdir(self.input_path):  
            # 收集文件夹中的所有 PDF 文件  
            pdf_files = [os.path.join(dirpath, filename)  
                         for dirpath, _, filenames in os.walk(self.input_path)  
                         for filename in filenames if filename.endswith('.pdf')]  
        else:  
            raise ValueError("输入路径既不是文件也不是文件夹。")  

        # 使用线程池并行处理 PDF 文件  
        with ThreadPoolExecutor(max_workers=5) as executor:  
            future_to_file = {executor.submit(self.process_pdf_file, pdf, grobid_url): pdf for pdf in pdf_files}  

            # 收集生成的 Markdown 内容  
            for future in as_completed(future_to_file):  
                result = future.result()  
                if result:  
                    markdown_contents.append(result)  

        # 如果有有效的 Markdown 内容，将其保存到文件  
        if markdown_contents:  
            # 生成时间戳  
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  
            # 生成两位随机字母  
            random_suffix = ''.join(random.choices(string.ascii_lowercase, k=2))  
            output_filename = os.path.join(self.output_path, f"output_{timestamp}_{random_suffix}.md") 
            self.save_markdown_file(output_filename, "\n\n".join(markdown_contents))  # 合并并保存为 Markdown 文件  
            self.logger.info(f"所有 Markdown 文件已合并并保存为 {output_filename}") 
            return output_filename  # 返回生成文件路径  
        else:  
            self.logger.error("没有有效的 Markdown 内容生成。")
            return None  
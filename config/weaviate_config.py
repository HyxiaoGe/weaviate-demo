"""
Weaviate 连接配置模块
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class WeaviateConfig:
    """Weaviate 配置类"""

    def __init__(self):
        self.weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        self.ollama_api_endpoint = os.getenv("OLLAMA_API_ENDPOINT", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "bge-m3")

    def get_connection_params(self):
        """获取连接参数"""
        return {
            "url": self.weaviate_url,
            "timeout_config": (5, 15),  # (连接超时, 读取超时)
        }

    def get_ollama_config(self):
        """获取 Ollama 配置"""
        return {
            "api_endpoint": self.ollama_api_endpoint,
            "model": self.ollama_model,
        }

    def __str__(self):
        return f"WeaviateConfig(url={self.weaviate_url}, ollama={self.ollama_model})"


# 创建全局配置实例
config = WeaviateConfig()
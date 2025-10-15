import requests
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

    def __str__(self):
        return f"WeaviateConfig(url={self.weaviate_url}, ollama={self.ollama_model})"

# 创建配置实例
config = WeaviateConfig()


def test_connection():
    """测试 Weaviate 连接"""
    print("正在连接到 Weaviate...")
    print(f"   URL: {config.weaviate_url}")
    print(f"   Ollama: {config.ollama_api_endpoint} ({config.ollama_model})")
    print()

    try:
        # 使用 requests 直接测试连接
        meta_url = f"{config.weaviate_url}/v1/meta"
        response = requests.get(meta_url, timeout=10)

        if response.status_code == 200:
            print("连接成功！")

            # 解析服务器信息
            meta = response.json()

            # 获取服务器信息
            print("\n服务器信息:")
            print(f"   版本: {meta['version']}")
            print(f"   主机名: {meta['hostname']}")
            print(f"   最大消息大小: {meta['grpcMaxMessageSize']} bytes")

            # 检查可用模块
            print("\n可用模块:")
            modules = meta.get('modules', {})
            if modules:
                for module_name, module_info in modules.items():
                    print(f"   [OK] {module_name}")
                    if 'documentationHref' in module_info:
                        print(f"      文档: {module_info['documentationHref']}")
            else:
                print("   [X] 未找到任何模块")

            # 检查 Ollama 模块状态
            if 'text2vec-ollama' in modules:
                print(f"\nOllama 模块已启用!")
                print(f"   模型: {config.ollama_model}")
                print(f"   API: {config.ollama_api_endpoint}")
            else:
                print(f"\n警告: Ollama 模块未启用")
                print("   请检查 Weaviate 配置是否包含 text2vec-ollama 模块")

            return True
        else:
            print(f"连接失败: HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"连接失败: {e}")
        print("\n故障排除建议:")
        print("   1. 检查 Weaviate 服务是否正在运行")
        print("   2. 验证 URL 配置是否正确")
        print("   3. 确认网络连接是否正常")
        print("   4. 检查防火墙设置")
        return False


def test_basic_operations():
    """测试基本操作"""
    print("\n测试基本操作...")

    try:
        # 列出所有现有的类
        print("检查现有数据类...")
        schema_url = f"{config.weaviate_url}/v1/schema"
        response = requests.get(schema_url, timeout=10)

        if response.status_code == 200:
            schema = response.json()
            classes = schema.get('classes', [])

            if classes:
                print(f"   找到 {len(classes)} 个数据类:")
                for cls in classes:
                    print(f"   - {cls['class']}")
            else:
                print("   当前没有任何数据类 (这是正常的)")

            print("\n基本操作测试通过")
            return True
        else:
            print(f"Schema 查询失败: HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"基本操作测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("Weaviate 连接测试")
    print("=" * 60)

    # 显示配置信息
    print(f"配置信息: {config}")
    print()

    # 测试连接
    connection_success = test_connection()

    if connection_success:
        # 测试基本操作
        operations_success = test_basic_operations()

        if operations_success:
            print("\n所有测试通过! Weaviate 环境准备就绪")
        else:
            print("\n部分测试失败，请检查配置")
    else:
        print("\n连接失败，请检查 Weaviate 服务状态")
        print("\n快速修复:")
        print("   1. 确保 Weaviate 容器正在运行")
        print("   2. 检查 .env 文件中的 WEAVIATE_URL 配置")
        print("   3. 尝试重新启动 Weaviate 服务")


if __name__ == "__main__":
    main()
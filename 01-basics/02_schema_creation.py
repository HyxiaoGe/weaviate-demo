import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class WeaviateClient:
    def __init__(self):
        self.weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        self.headers = {"Content-Type": "application/json"}

    def create_class(self, class_definition):
        """创建数据类"""
        url = f"{self.weaviate_url}/v1/schema"
        response = requests.post(url, json=class_definition, headers=self.headers)
        return response

    def list_classes(self):
        """列出所有数据类"""
        url = f"{self.weaviate_url}/v1/schema"
        response = requests.get(url)
        return response

    def delete_class(self, class_name):
        """删除数据类"""
        url = f"{self.weaviate_url}/v1/schema/{class_name}"
        response = requests.delete(url)
        return response

def create_movie_schema():
    """创建电影数据 Schema"""
    movie_class = {
        "class": "Movie",
        "description": "电影信息数据",
        "vectorizer": "text2vec-ollama",
        "moduleConfig": {
            "text2vec-ollama": {
                "model": "bge-m3",
                "apiEndpoint": "http://192.168.1.4:11434"
            }
        },
        "properties": [
            {
                "name": "title",
                "dataType": ["text"],
                "description": "电影标题",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": False,
                        "vectorizePropertyName": False
                    }
                }
            },
            {
                "name": "description",
                "dataType": ["text"],
                "description": "电影简介",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": False,
                        "vectorizePropertyName": False
                    }
                }
            },
            {
                "name": "year",
                "dataType": ["int"],
                "description": "上映年份",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "genre",
                "dataType": ["text"],
                "description": "电影类型",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "rating",
                "dataType": ["number"],
                "description": "评分 (0-10)",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            }
        ]
    }
    return movie_class

def create_article_schema():
    """创建文章数据 Schema"""
    article_class = {
        "class": "Article",
        "description": "新闻文章数据",
        "vectorizer": "text2vec-ollama",
        "moduleConfig": {
            "text2vec-ollama": {
                "model": "bge-m3",
                "apiEndpoint": "http://192.168.1.4:11434"
            }
        },
        "properties": [
            {
                "name": "title",
                "dataType": ["text"],
                "description": "文章标题",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": False,
                        "vectorizePropertyName": False
                    }
                }
            },
            {
                "name": "content",
                "dataType": ["text"],
                "description": "文章内容",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": False,
                        "vectorizePropertyName": False
                    }
                }
            },
            {
                "name": "author",
                "dataType": ["text"],
                "description": "作者",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "publishDate",
                "dataType": ["date"],
                "description": "发布日期",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "category",
                "dataType": ["text"],
                "description": "文章分类",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            }
        ]
    }
    return article_class

def test_create_schema():
    """测试创建 Schema"""
    client = WeaviateClient()

    print("开始创建 Weaviate Schema...")

    # 1. 创建电影数据类
    print("\n1. 创建 Movie 数据类...")
    movie_schema = create_movie_schema()
    response = client.create_class(movie_schema)

    if response.status_code == 200:
        print("   [OK] Movie 数据类创建成功")
    else:
        print(f"   [X] Movie 数据类创建失败: {response.status_code}")
        if response.status_code == 422:
            print(f"   错误详情: {response.text}")

    # 2. 创建文章数据类
    print("\n2. 创建 Article 数据类...")
    article_schema = create_article_schema()
    response = client.create_class(article_schema)

    if response.status_code == 200:
        print("   [OK] Article 数据类创建成功")
    else:
        print(f"   [X] Article 数据类创建失败: {response.status_code}")
        if response.status_code == 422:
            print(f"   错误详情: {response.text}")

def list_existing_schema():
    """列出现有的 Schema"""
    client = WeaviateClient()

    print("\n检查现有数据类...")
    response = client.list_classes()

    if response.status_code == 200:
        schema = response.json()
        classes = schema.get('classes', [])

        if classes:
            print(f"   找到 {len(classes)} 个数据类:")
            for cls in classes:
                print(f"   - {cls['class']}")
                print(f"     描述: {cls.get('description', '无描述')}")
                print(f"     向量化器: {cls.get('vectorizer', '无')}")
                print(f"     属性数量: {len(cls.get('properties', []))}")
                print()
        else:
            print("   当前没有任何数据类")
    else:
        print(f"   [X] 获取 Schema 失败: {response.status_code}")

def clean_existing_schema():
    """清理现有的 Schema（可选）"""
    client = WeaviateClient()

    print("\n清理现有数据类...")
    response = client.list_classes()

    if response.status_code == 200:
        schema = response.json()
        classes = schema.get('classes', [])

        for cls in classes:
            class_name = cls['class']
            print(f"   删除 {class_name}...")
            delete_response = client.delete_class(class_name)

            if delete_response.status_code == 200:
                print(f"   [OK] {class_name} 删除成功")
            else:
                print(f"   [X] {class_name} 删除失败: {delete_response.status_code}")

def main():
    """主函数"""
    print("=" * 60)
    print("Weaviate Schema 创建测试")
    print("=" * 60)

    # 显示配置信息
    weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    ollama_model = os.getenv("OLLAMA_MODEL", "bge-m3")
    print(f"Weaviate URL: {weaviate_url}")
    print(f"Ollama 模型: {ollama_model}")

    # 1. 列出现有的 Schema
    list_existing_schema()

    # 2. 自动清理现有数据
    print("\n自动清理现有数据类...")
    clean_existing_schema()

    # 3. 创建新的 Schema
    test_create_schema()

    # 4. 再次列出 Schema 确认创建结果
    print("\n" + "=" * 60)
    print("创建结果确认:")
    list_existing_schema()

    print("\nSchema 创建完成!")
    print("\n下一步:")
    print("   1. 运行 03_data_import.py 导入示例数据")
    print("   2. 运行 04_basic_query.py 学习查询操作")
    print("   3. 运行 05_vector_search.py 体验向量搜索")

if __name__ == "__main__":
    main()
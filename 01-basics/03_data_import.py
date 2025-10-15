import requests
import json
import os
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class WeaviateClient:
    def __init__(self):
        self.weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        self.headers = {"Content-Type": "application/json"}

    def create_object(self, class_name, data_object):
        """创建单个对象"""
        url = f"{self.weaviate_url}/v1/objects"
        payload = {
            "class": class_name,
            "properties": data_object
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response

    def batch_create_objects(self, objects):
        """批量创建对象"""
        url = f"{self.weaviate_url}/v1/batch/objects"
        payload = {"objects": objects}
        response = requests.post(url, json=payload, headers=self.headers)
        return response

    def get_object_count(self, class_name):
        """获取对象数量"""
        url = f"{self.weaviate_url}/v1/objects"
        params = {"class": class_name, "limit": 1}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('totalResults', 0)
        return 0

    def list_objects(self, class_name, limit=10):
        """列出对象"""
        url = f"{self.weaviate_url}/v1/objects"
        params = {
            "class": class_name,
            "limit": limit,
            "include": ["vector"]
        }
        response = requests.get(url, params=params)
        return response

def generate_movie_data():
    """生成电影测试数据"""
    movies = [
        {
            "title": "肖申克的救赎",
            "description": "一个关于希望和友谊的经典故事，讲述了银行家安迪在肖申克监狱中的生活经历。",
            "year": 1994,
            "genre": "剧情",
            "rating": 9.7
        },
        {
            "title": "盗梦空间",
            "description": "一个关于梦境中的梦境的科幻惊悚片，探索了潜意识和现实的边界。",
            "year": 2010,
            "genre": "科幻",
            "rating": 8.8
        },
        {
            "title": "教父",
            "description": "黑帮家族史诗，讲述了科里昂家族的兴衰历程和美国梦的黑暗面。",
            "year": 1972,
            "genre": "犯罪",
            "rating": 9.2
        },
        {
            "title": "星际穿越",
            "description": "在地球即将毁灭时，一群探险家穿越虫洞寻找人类新家园的科幻冒险。",
            "year": 2014,
            "genre": "科幻",
            "rating": 8.6
        },
        {
            "title": "千与千寻",
            "description": "宫崎骏的动画杰作，讲述了小女孩千寻在神秘世界中的成长冒险。",
            "year": 2001,
            "genre": "动画",
            "rating": 8.6
        },
        {
            "title": "阿甘正传",
            "description": "一个智商不高但心地善良的男人见证了美国历史上重要时刻的励志故事。",
            "year": 1994,
            "genre": "剧情",
            "rating": 8.8
        },
        {
            "title": "黑客帝国",
            "description": "关于虚拟现实和人类反抗机器统治的科幻经典，探讨了什么是真实。",
            "year": 1999,
            "genre": "科幻",
            "rating": 8.7
        },
        {
            "title": "泰坦尼克号",
            "description": "以泰坦尼克号沉船为背景的爱情悲剧，展现了阶级差异和人性光辉。",
            "year": 1997,
            "genre": "爱情",
            "rating": 7.8
        }
    ]
    return movies

def generate_article_data():
    """生成文章测试数据"""
    base_date = datetime.now() - timedelta(days=365)

    articles = [
        {
            "title": "人工智能技术发展趋势分析",
            "content": "人工智能技术正在快速发展，从机器学习到深度学习，再到大语言模型，AI正在改变我们的生活方式。本文分析了当前AI技术的发展趋势和未来展望。",
            "author": "张三",
            "publishDate": (base_date + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "category": "科技"
        },
        {
            "title": "量子计算突破性进展",
            "content": "量子计算领域最近取得了重大突破，研究人员成功实现了更稳定的量子比特。这一进展将为密码学、药物研发等领域带来革命性变化。",
            "author": "李四",
            "publishDate": (base_date + timedelta(days=60)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "category": "科技"
        },
        {
            "title": "可持续能源解决方案",
            "content": "随着气候变化问题日益严重，可持续能源成为全球关注的焦点。太阳能、风能等清洁能源技术的不断进步为解决能源危机提供了新的可能。",
            "author": "王五",
            "publishDate": (base_date + timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "category": "环保"
        },
        {
            "title": "远程工作的未来",
            "content": "疫情改变了人们的工作方式，远程工作从临时措施变成了新常态。本文探讨了远程工作对企业和员工的影响，以及未来工作模式的可能变化。",
            "author": "赵六",
            "publishDate": (base_date + timedelta(days=120)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "category": "商业"
        },
        {
            "title": "区块链技术在金融领域的应用",
            "content": "区块链技术不仅仅是加密货币的基础，它在金融领域有着广泛的应用前景。从跨境支付到智能合约，区块链正在重塑金融服务。",
            "author": "钱七",
            "publishDate": (base_date + timedelta(days=150)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "category": "金融"
        },
        {
            "title": "健康生活方式指南",
            "content": "保持健康的生活方式对现代人来说越来越重要。本文提供了关于饮食、运动、睡眠等方面的实用建议，帮助读者建立健康的生活习惯。",
            "author": "孙八",
            "publishDate": (base_date + timedelta(days=180)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "category": "健康"
        }
    ]
    return articles

def import_movies(client):
    """导入电影数据"""
    print("\n导入电影数据...")
    movies = generate_movie_data()

    success_count = 0
    for movie in movies:
        response = client.create_object("Movie", movie)
        if response.status_code == 200:
            success_count += 1
            print(f"   [OK] 导入: {movie['title']}")
        else:
            print(f"   [X] 失败: {movie['title']} - {response.status_code}")

    print(f"\n电影导入完成: {success_count}/{len(movies)} 成功")
    return success_count

def import_articles(client):
    """导入文章数据"""
    print("\n导入文章数据...")
    articles = generate_article_data()

    success_count = 0
    for article in articles:
        response = client.create_object("Article", article)
        if response.status_code == 200:
            success_count += 1
            print(f"   [OK] 导入: {article['title']}")
        else:
            print(f"   [X] 失败: {article['title']} - {response.status_code}")
            if response.text:
                print(f"     错误: {response.text}")

    print(f"\n文章导入完成: {success_count}/{len(articles)} 成功")
    return success_count

def verify_import(client):
    """验证导入结果"""
    print("\n验证导入结果...")

    # 检查电影数据
    movie_count = client.get_object_count("Movie")
    print(f"\n电影数据总数: {movie_count}")

    if movie_count > 0:
        response = client.list_objects("Movie", limit=3)
        if response.status_code == 200:
            data = response.json()
            objects = data.get('objects', [])
            print("示例电影数据:")
            for obj in objects:
                props = obj.get('properties', {})
                print(f"   - {props.get('title', 'N/A')} ({props.get('year', 'N/A')}) - {props.get('genre', 'N/A')}")

    # 检查文章数据
    article_count = client.get_object_count("Article")
    print(f"\n文章数据总数: {article_count}")

    if article_count > 0:
        response = client.list_objects("Article", limit=3)
        if response.status_code == 200:
            data = response.json()
            objects = data.get('objects', [])
            print("示例文章数据:")
            for obj in objects:
                props = obj.get('properties', {})
                print(f"   - {props.get('title', 'N/A')} - {props.get('author', 'N/A')} - {props.get('category', 'N/A')}")

def main():
    """主函数"""
    print("=" * 60)
    print("Weaviate 数据导入测试")
    print("=" * 60)

    # 显示配置信息
    weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    print(f"Weaviate URL: {weaviate_url}")

    # 创建客户端
    client = WeaviateClient()

    # 1. 导入电影数据
    movie_success = import_movies(client)

    # 2. 导入文章数据
    article_success = import_articles(client)

    # 3. 验证导入结果
    verify_import(client)

    # 4. 总结
    print("\n" + "=" * 60)
    print("数据导入总结:")
    print(f"电影数据: {movie_success} 条")
    print(f"文章数据: {article_success} 条")
    print(f"总计: {movie_success + article_success} 条数据")

    if movie_success > 0 and article_success > 0:
        print("\n数据导入成功!")
        print("\n下一步:")
        print("   1. 运行 04_basic_query.py 学习基础查询")
        print("   2. 运行 05_vector_search.py 体验向量搜索")
        print("   3. 尝试不同的查询方式和过滤条件")
    else:
        print("\n数据导入遇到问题，请检查错误信息")

if __name__ == "__main__":
    main()
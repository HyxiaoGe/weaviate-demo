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

    def graphql_query(self, query):
        """GraphQL查询"""
        response = requests.post(
            f"{self.weaviate_url}/v1/graphql",
            json={"query": query},
            headers=self.headers
        )
        return response

    def get_objects_rest(self, class_name, limit=5, where_clause=None):
        """REST查询对象"""
        url = f"{self.weaviate_url}/v1/objects"
        params = {"class": class_name, "limit": limit}

        if where_clause:
            params["where"] = where_clause

        response = requests.get(url, params=params)
        return response

def demo_correct_counting(client):
    """演示正确的计数方法"""
    print("\n=== 正确的数据统计 ===")

    # 使用GraphQL聚合查询
    query = """
    {
      Aggregate {
        Movie {
          meta {
            count
          }
        }
        Article {
          meta {
            count
          }
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        data = result.get('data', {})
        aggregate = data.get('Aggregate', {})

        movie_data = aggregate.get('Movie', [])
        article_data = aggregate.get('Article', [])

        movie_count = movie_data[0].get('meta', {}).get('count', 0) if movie_data else 0
        article_count = article_data[0].get('meta', {}).get('count', 0) if article_data else 0

        print(f"   电影总数: {movie_count}")
        print(f"   文章总数: {article_count}")
        print(f"   数据总计: {movie_count + article_count}")

        return movie_count, article_count
    else:
        print(f"   [X] 查询失败: {response.status_code}")
        return 0, 0

def demo_movie_queries(client):
    """演示电影查询"""
    print("\n=== 电影查询演示 ===")

    # 1. 查询所有电影（前5条，去重）
    print("\n1. 查询电影数据（前5条）:")
    query = """
    {
      Get {
        Movie(limit: 5) {
          title
          year
          genre
          rating
          description
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部电影:")
        for movie in movies:
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")
            print(f"     类型: {movie.get('genre', 'N/A')} | 评分: {movie.get('rating', 'N/A')}")
            print(f"     简介: {movie.get('description', 'N/A')[:60]}...")
            print()

    # 2. 查询科幻电影
    print("2. 查询科幻电影:")
    query = """
    {
      Get {
        Movie(where: {
          path: ["genre"]
          operator: Equal
          valueText: "科幻"
        }) {
          title
          year
          rating
          genre
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部科幻电影:")
        for movie in movies:
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 评分: {movie.get('rating', 'N/A')}")

    # 3. 查询高评分电影
    print("\n3. 查询高评分电影（评分 > 9.0）:")
    query = """
    {
      Get {
        Movie(where: {
          path: ["rating"]
          operator: GreaterThan
          valueNumber: 9.0
        }) {
          title
          year
          rating
          genre
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部高评分电影:")
        for movie in movies:
            print(f"   - {movie.get('title', 'N/A')} - 评分: {movie.get('rating', 'N/A')}")

    # 4. 查询2000年后的电影
    print("\n4. 查询2000年后的电影:")
    query = """
    {
      Get {
        Movie(where: {
          path: ["year"]
          operator: GreaterThan
          valueInt: 2000
        }) {
          title
          year
          rating
          genre
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部2000年后的电影:")
        for movie in movies:
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")

    # 5. 查询高评分的科幻电影
    print("\n5. 查询高评分的科幻电影:")
    query = """
    {
      Get {
        Movie(where: {
          operator: And
          operands: [
            {
              path: ["genre"]
              operator: Equal
              valueText: "科幻"
            },
            {
              path: ["rating"]
              operator: GreaterThan
              valueNumber: 8.5
            }
          ]
        }) {
          title
          year
          rating
          genre
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部高评分科幻电影:")
        for movie in movies:
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 评分: {movie.get('rating', 'N/A')}")

def demo_article_queries(client):
    """演示文章查询"""
    print("\n=== 文章查询演示 ===")

    # 1. 查询科技类文章
    print("\n1. 查询科技类文章:")
    query = """
    {
      Get {
        Article(where: {
          path: ["category"]
          operator: Equal
          valueText: "科技"
        }) {
          title
          author
          category
          publishDate
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        articles = result.get('data', {}).get('Get', {}).get('Article', [])

        print(f"   找到 {len(articles)} 篇科技文章:")
        for article in articles:
            print(f"   - {article.get('title', 'N/A')}")
            print(f"     作者: {article.get('author', 'N/A')} | 分类: {article.get('category', 'N/A')}")

def demo_sorting_queries(client):
    """演示排序查询"""
    print("\n=== 排序查询演示 ===")

    # 1. 按评分降序
    print("\n1. 按评分降序查询电影（前3名）:")
    query = """
    {
      Get {
        Movie(sort: [{path: "rating", order: desc}], limit: 3) {
          title
          year
          rating
          genre
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        for i, movie in enumerate(movies, 1):
            print(f"   {i}. {movie.get('title', 'N/A')} - 评分: {movie.get('rating', 'N/A')}")

    # 2. 按年份升序
    print("\n2. 按年份升序查询电影（最早的3部）:")
    query = """
    {
      Get {
        Movie(sort: [{path: "year", order: asc}], limit: 3) {
          title
          year
          rating
          genre
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        for i, movie in enumerate(movies, 1):
            print(f"   {i}. {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")

def main():
    """主函数"""
    print("=" * 60)
    print("Weaviate 基础查询测试")
    print("=" * 60)

    # 显示配置信息
    weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    print(f"Weaviate URL: {weaviate_url}")

    # 创建客户端
    client = WeaviateClient()

    # 1. 正确的数据统计
    movie_count, article_count = demo_correct_counting(client)

    # 2. 电影查询演示
    demo_movie_queries(client)

    # 3. 文章查询演示
    demo_article_queries(client)

    # 4. 排序查询演示
    demo_sorting_queries(client)

    # 总结
    print("\n" + "=" * 60)

    print("\n下一步:")
    print("   1. 运行 05_vector_search.py 体验向量搜索")
    print("   2. 学习更复杂的GraphQL查询")
    print("   3. 体验Weaviate的语义搜索能力")

if __name__ == "__main__":
    main()
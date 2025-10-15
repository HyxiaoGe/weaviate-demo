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

def demo_semantic_search(client):
    """演示语义搜索"""
    print("\n=== 语义搜索演示 ===")

    # 1. 搜索"关于希望的电影"
    print("\n1. 语义搜索: '关于希望的电影'")
    query = """
    {
      Get {
        Movie(
          nearText: {
            concepts: ["希望", "勇气", "坚持"]
            distance: 0.8
          },
          limit: 3
        ) {
          title
          year
          genre
          rating
          description
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部相关电影:")
        for movie in movies:
            distance = movie.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")
            print(f"     相似度: {distance:.3f} | 类型: {movie.get('genre', 'N/A')}")
            print(f"     简介: {movie.get('description', 'N/A')[:60]}...")

    # 2. 搜索"关于人工智能的文章"
    print("\n2. 语义搜索: '关于人工智能的文章'")
    query = """
    {
      Get {
        Article(
          nearText: {
            concepts: ["人工智能", "AI技术", "机器学习"]
            distance: 0.7
          },
          limit: 3
        ) {
          title
          author
          category
          content
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        articles = result.get('data', {}).get('Get', {}).get('Article', [])

        print(f"   找到 {len(articles)} 篇相关文章:")
        for article in articles:
            distance = article.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {article.get('title', 'N/A')}")
            print(f"     相似度: {distance:.3f} | 作者: {article.get('author', 'N/A')}")
            print(f"     内容: {article.get('content', 'N/A')[:80]}...")

    # 3. 搜索"关于未来科技的科幻电影"
    print("\n3. 语义搜索: '关于未来科技的科幻电影'")
    query = """
    {
      Get {
        Movie(
          nearText: {
            concepts: ["未来", "科技", "虚拟现实", "人工智能"]
            distance: 0.75
          },
          limit: 3
        ) {
          title
          year
          genre
          description
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部相关电影:")
        for movie in movies:
            distance = movie.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")
            print(f"     相似度: {distance:.3f} | 类型: {movie.get('genre', 'N/A')}")
            print(f"     简介: {movie.get('description', 'N/A')[:80]}...")

def demo_hybrid_search(client):
    """演示混合搜索"""
    print("\n=== 混合搜索演示 ===")

    # 1. 搜索包含"教父"或相关的电影
    print("\n1. 混合搜索: 关键词 '黑帮' + 语义 '家族'")
    query = """
    {
      Get {
        Movie(
          where: {
            operator: Or
            operands: [
              {
                path: ["title"]
                operator: Like
                valueText: "*教父*"
              }
            ]
          },
          nearText: {
            concepts: ["家族", "权力", "犯罪"]
            distance: 0.8
          },
          limit: 3
        ) {
          title
          year
          genre
          rating
          description
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部相关电影:")
        for movie in movies:
            distance = movie.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")
            print(f"     相似度: {distance:.3f} | 评分: {movie.get('rating', 'N/A')}")

    # 2. 搜索高评分的动画电影
    print("\n2. 混合搜索: 条件过滤 + 语义搜索")
    query = """
    {
      Get {
        Movie(
          where: {
            operator: And
            operands: [
              {
                path: ["rating"]
                operator: GreaterThan
                valueNumber: 8.5
              },
              {
                path: ["genre"]
                operator: Equal
                valueText: "动画"
              }
            ]
          },
          nearText: {
            concepts: ["冒险", "成长", "魔法"]
            distance: 0.7
          },
          limit: 3
        ) {
          title
          year
          genre
          rating
          description
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部相关电影:")
        for movie in movies:
            distance = movie.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")
            print(f"   评分: {movie.get('rating', 'N/A')} | 相似度: {distance:.3f}")
            print(f"   简介: {movie.get('description', 'N/A')[:60]}...")

def demo_similarity_threshold(client):
    """演示相似度阈值控制"""
    print("\n=== 相似度阈值控制演示 ===")

    # 1. 严格的相似度搜索
    print("\n1. 严格搜索: 相似度阈值 0.3 (高度相关)")
    query = """
    {
      Get {
        Movie(
          nearText: {
            concepts: ["监狱", "自由", "救赎"]
            distance: 0.3
          },
          limit: 5
        ) {
          title
          year
          genre
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部高度相关的电影:")
        for movie in movies:
            distance = movie.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 相似度: {distance:.3f}")

    # 2. 宽松的相似度搜索
    print("\n2. 宽松搜索: 相似度阈值 0.9 (更多相关结果)")
    query = """
    {
      Get {
        Movie(
          nearText: {
            concepts: ["监狱", "自由", "救赎"]
            distance: 0.9
          },
          limit: 5
        ) {
          title
          year
          genre
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部相关电影:")
        for movie in movies:
            distance = movie.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 相似度: {distance:.3f}")

def demo_cross_type_search(client):
    """演示跨类型搜索"""
    print("\n=== 跨类型搜索演示 ===")

    # 1. 在电影和文章中搜索相同概念
    print("\n1. 跨类型搜索: '科技发展' 相关内容")

    # 搜索电影
    print("\n   相关电影:")
    movie_query = """
    {
      Get {
        Movie(
          nearText: {
            concepts: ["科技", "未来", "创新"]
            distance: 0.8
          },
          limit: 2
        ) {
          title
          year
          genre
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(movie_query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])
        for movie in movies:
            distance = movie.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 相似度: {distance:.3f}")

    # 搜索文章
    print("\n   相关文章:")
    article_query = """
    {
      Get {
        Article(
          nearText: {
            concepts: ["科技", "未来", "创新"]
            distance: 0.8
          },
          limit: 2
        ) {
          title
          author
          category
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(article_query)
    if response.status_code == 200:
        result = response.json()
        articles = result.get('data', {}).get('Get', {}).get('Article', [])
        for article in articles:
            distance = article.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {article.get('title', 'N/A')} - {article.get('author', 'N/A')} - 相似度: {distance:.3f}")

def demo_advanced_search(client):
    """演示高级搜索技巧"""
    print("\n=== 高级搜索技巧演示 ===")

    # 1. 搜索相似电影并排除某些类型
    print("\n1. 排除特定类型的搜索: 寻找类似《黑客帝国》但不是科幻的电影")
    query = """
    {
      Get {
        Movie(
          nearText: {
            concepts: ["虚拟现实", "黑客", "程序", "现实世界"]
            distance: 0.7
          },
          where: {
            path: ["genre"]
            operator: NotEqual
            valueText: "科幻"
          },
          limit: 3
        ) {
          title
          year
          genre
          description
          _additional {
            distance
          }
        }
      }
    }
    """

    response = client.graphql_query(query)
    if response.status_code == 200:
        result = response.json()
        movies = result.get('data', {}).get('Get', {}).get('Movie', [])

        print(f"   找到 {len(movies)} 部相关电影:")
        for movie in movies:
            distance = movie.get('_additional', {}).get('distance', 'N/A')
            print(f"   - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")
            print(f"     类型: {movie.get('genre', 'N/A')} | 相似度: {distance:.3f}")

def main():
    """主函数"""
    print("=" * 60)
    print("Weaviate 向量搜索测试")
    print("=" * 60)

    # 显示配置信息
    weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    ollama_model = os.getenv("OLLAMA_MODEL", "bge-m3")
    print(f"Weaviate URL: {weaviate_url}")
    print(f"向量化模型: {ollama_model}")

    # 创建客户端
    client = WeaviateClient()

    print("\n向量搜索是 Weaviate 的核心功能!")
    print("它可以根据语义相似度而不是关键词匹配来搜索内容。")

    # 1. 语义搜索演示
    demo_semantic_search(client)

    # 2. 混合搜索演示
    demo_hybrid_search(client)

    # 3. 相似度阈值控制
    demo_similarity_threshold(client)

    # 4. 跨类型搜索
    demo_cross_type_search(client)

    # 5. 高级搜索技巧
    demo_advanced_search(client)

    # 总结
    print("\n" + "=" * 60)
    print("向量搜索测试完成!")
    print("\n学到的向量搜索技巧:")
    print("   1. 语义搜索 - 基于概念和含义搜索")
    print("   2. 混合搜索 - 关键词 + 语义搜索")
    print("   3. 相似度控制 - 调整搜索精度")
    print("   4. 跨类型搜索 - 在不同数据类型中搜索")
    print("   5. 高级技巧 - 排除、组合条件等")

    print("\nWeaviate 向量搜索的优势:")
    print("   - 理解语义，而不仅仅是关键词")
    print("   - 支持多语言搜索")
    print("   - 处理拼写错误和变体")
    print("   - 找到概念上相关的内容")

    print("\n恭喜! 你已经掌握了 Weaviate 的基础操作!")
    print("\n下一步学习方向:")
    print("   1. 进阶功能: 批量操作、聚合查询")
    print("   2. 实战项目: 语义搜索引擎、问答系统")
    print("   3. 性能优化: 索引调优、缓存策略")

if __name__ == "__main__":
    main()